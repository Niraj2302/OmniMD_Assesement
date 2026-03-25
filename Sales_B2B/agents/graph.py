import torch
import json
import re
import asyncio
from transformers import pipeline
from langgraph.graph import StateGraph, END
from agents.state import ProspectState
from workers.tasks import gather_linkedin_signal, gather_intent_signal
from rag.text_pipeline import retrieve_text
from rag.ocr_pipeline import retrieve_ocr
from celery import group

_pipe = None


def get_pipe():
    global _pipe
    if _pipe is None:
        _pipe = pipeline(
            "text-generation",
            model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            device_map="auto",
            torch_dtype=torch.bfloat16
        )
    return _pipe


def extract_json(text):
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception:
        pass
    return {"score": 0, "rationale": "Parsing failed", "next_action": "Review"}


async def signal_node(state: ProspectState):
    job = group(
        gather_linkedin_signal.s(state["prospect_id"]),
        gather_intent_signal.s(state["prospect_id"])
    )
    res = job.apply_async().get()  # Use .get() for consistency in state
    merged = {k: v for d in res for k, v in d.items()}
    return {"gathered_signals": merged}


async def rag_node(state: ProspectState):
    t = await retrieve_text(state["prospect_id"])
    o = await retrieve_ocr(state["prospect_id"])
    return {"retrieved_context": t + o}


async def score_node(state: ProspectState):
    pipe = get_pipe()
    prompt = f"Evaluate lead {state['prospect_id']}. Signals: {state['gathered_signals']}"

    def call_llm():
        return pipe(prompt, max_new_tokens=50)[0]["generated_text"]

    out = await asyncio.to_thread(call_llm)
    parsed = extract_json(out)
    return {
        "score": parsed.get("score", 0),
        "rationale": parsed.get("rationale", "N/A"),
        "next_action": parsed.get("next_action", "Ignore")
    }


workflow = StateGraph(ProspectState)
workflow.add_node("gather_signals", signal_node)
workflow.add_node("retrieve_context", rag_node)
workflow.add_node("score_prospect", score_node)
workflow.set_entry_point("gather_signals")
workflow.add_edge("gather_signals", "retrieve_context")
workflow.add_edge("retrieve_context", "score_prospect")
workflow.add_edge("score_prospect", END)
app_graph = workflow.compile()