from typing import TypedDict, Annotated, List, Dict, Any
import operator

class ProspectState(TypedDict):
    prospect_id: str
    event_trigger: str
    gathered_signals: Annotated[Dict[str, Any], operator.ior]
    retrieved_context: Annotated[List[str], operator.add]
    score: int
    rationale: str
    next_action: str
    needs_human_review: bool