from fastapi import FastAPI, BackgroundTasks, HTTPException
from api.models import EventPayload
from agents.graph import app_graph

app = FastAPI(title="Sales B2B MAS")
results_db = {}


async def run_workflow(prospect_id: str, event_trigger: str):
    initial_state = {
        "prospect_id": prospect_id,
        "event_trigger": event_trigger,
        "gathered_signals": {},
        "retrieved_context": [],
        "needs_human_review": False
    }

    final_state = await app_graph.ainvoke(initial_state)

    results_db[prospect_id] = {
        "status": "completed",
        "score": final_state.get("score"),
        "rationale": final_state.get("rationale"),
        "next_action": final_state.get("next_action")
    }


@app.post("/events/ingest")
async def ingest_event(payload: EventPayload, background_tasks: BackgroundTasks):
    results_db[payload.prospect_id] = {"status": "processing"}
    background_tasks.add_task(run_workflow, payload.prospect_id, payload.event_trigger)
    return {"status": "accepted"}


@app.get("/prospects/{prospect_id}")
async def get_prospect(prospect_id: str):
    result = results_db.get(prospect_id)
    if not result:
        raise HTTPException(status_code=404, detail="ID not found")
    return result