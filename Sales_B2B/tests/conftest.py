import sys
import pytest
import asyncio
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(autouse=True)
def mock_external_deps():
    with patch("transformers.pipeline") as mock_pipe:
        mock_pipe.return_value = lambda *args, **kwargs: [
            {"generated_text": '{"score": 90, "rationale": "Strong", "next_action": "Call"}'}
        ]

        from workers.celery_app import app as celery_app
        celery_app.conf.update(
            task_always_eager=True,
            task_eager_propagates=True,
            broker_url="memory://",
            result_backend="rpc://"
        )
        yield