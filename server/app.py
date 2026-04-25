"""
DebugArena — server/app.py
============================
FastAPI server that wraps the environment.
OpenEnv handles all the routing automatically —
you just need to register your environment here.

To run locally:
    cd debug_arena
    uvicorn server.app:app --host 0.0.0.0 --port 8000 --reload

Or use the OpenEnv CLI:
    openenv serve server.app:app --port 8000
"""

from openenv.core.env_server import create_app
from server.environment import DebugArenaEnvironment
from models import DebugAction, DebugObservation, DebugState

# OpenEnv's create_app() builds the full FastAPI app for you.
# It registers:
#   POST /reset  → calls environment.reset()
#   POST /step   → calls environment.step(action)
#   GET  /state  → calls environment.state
#   GET  /       → web UI for manual testing
app = create_app(
    env=DebugArenaEnvironment,
    action_cls=DebugAction,
    observation_cls=DebugObservation,
    env_name="DebugArena",
)
