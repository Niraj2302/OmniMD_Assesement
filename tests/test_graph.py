import pytest
import asyncio
from unittest.mock import MagicMock, patch
from agents.graph import app_graph


@pytest.mark.asyncio
async def test_workflow_high_score_path():
    with patch("agents.graph.get_pipe") as mock_get:
        mock_instance = MagicMock()
        mock_instance.return_value = [
            {"generated_text": '{"score": 90, "rationale": "Excellent lead", "next_action": "Call"}'}]
        mock_get.return_value = mock_instance

        with patch("agents.graph.gather_linkedin_signal.delay") as mock_li, \
                patch("agents.graph.gather_intent_signal.delay") as mock_in, \
                patch("agents.graph.retrieve_text") as mock_text, \
                patch("agents.graph.retrieve_ocr") as mock_ocr:
            mock_li.return_value.get.return_value = {"linkedin": "profile data"}
            mock_in.return_value.get.return_value = {"intent": "high"}
            mock_text.return_value = "CRM history"
            mock_ocr.return_value = "Business card data"

            inputs = {"prospect_id": "prospect_123"}
            final_state = await app_graph.ainvoke(inputs)

            assert final_state["score"] == 90
            assert final_state.get("needs_human_review", False) is False
            assert "Excellent" in final_state["rationale"]


@pytest.mark.asyncio
async def test_workflow_uncertain_review_path():
    with patch("agents.graph.get_pipe") as mock_get:
        mock_instance = MagicMock()
        mock_instance.return_value = [
            {"generated_text": '{"score": 50, "rationale": "Average lead", "next_action": "Nurture"}'}]
        mock_get.return_value = mock_instance

        with patch("agents.graph.gather_linkedin_signal.delay") as mock_li, \
                patch("agents.graph.gather_intent_signal.delay") as mock_in, \
                patch("agents.graph.retrieve_text") as mock_text, \
                patch("agents.graph.retrieve_ocr") as mock_ocr:
            mock_li.return_value.get.return_value = {"linkedin": "partial"}
            mock_in.return_value.get.return_value = {"intent": "low"}
            mock_text.return_value = ""
            mock_ocr.return_value = ""

            inputs = {"prospect_id": "prospect_456"}
            final_state = await app_graph.ainvoke(inputs)

            assert final_state["score"] == 50
            assert final_state["needs_human_review"] is True
            assert "FLAGGED" in final_state["rationale"]


@pytest.mark.asyncio
async def test_workflow_parsing_failure_fallback():
    with patch("agents.graph.get_pipe") as mock_get:
        mock_instance = MagicMock()
        mock_instance.return_value = [{"generated_text": "invalid non-json string"}]
        mock_get.return_value = mock_instance

        with patch("agents.graph.gather_linkedin_signal.delay"), \
                patch("agents.graph.gather_intent_signal.delay"), \
                patch("agents.graph.retrieve_text"), \
                patch("agents.graph.retrieve_ocr"):
            inputs = {"prospect_id": "prospect_err"}
            final_state = await app_graph.ainvoke(inputs)

            assert final_state["score"] == 50
            assert final_state["needs_human_review"] is True