import pytest
from unittest.mock import patch, MagicMock
from agents.graph import app_graph


@pytest.mark.asyncio
async def test_workflow_execution():
    initial_state = {
        "prospect_id": "1",
        "event_trigger": "manual",
        "gathered_signals": {},
        "retrieved_context": [],
        "needs_human_review": False
    }

    with patch("agents.graph.get_pipe") as mock_get_pipe:
        mock_pipe_instance = MagicMock()
        mock_pipe_instance.return_value = [
            {"generated_text": '{"score": 90, "rationale": "High intent", "next_action": "Call"}'}
        ]
        mock_get_pipe.return_value = mock_pipe_instance

        final_state = await app_graph.ainvoke(initial_state)

    assert final_state["score"] == 90
    assert "High intent" in final_state["rationale"]