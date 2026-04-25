"""
DebugArena — models.py
========================
Defines the "contract" of the environment.
Every action the agent takes and every observation it receives
must match these dataclasses exactly.

OpenEnv requires: Action, Observation, State
"""

"""
DebugArena — models.py
========================
Defines the "contract" of the environment.
Every action the agent takes and every observation it receives
must match these dataclasses exactly.

OpenEnv requires:
  - Action     inherits from openenv Action
  - Observation inherits from openenv Observation
    (reward and done are BUILT INTO Observation — do not add them separately)
  - State      inherits from openenv State
"""

from typing import Optional
from openenv.core.env_server import Action, Observation, State


# ─────────────────────────────────────────────────────────────
# ACTION — what the agent sends to the environment each step
# ─────────────────────────────────────────────────────────────
class DebugAction(Action):
    """
    The agent's proposed fix for the buggy code.

    Example:
        action = DebugAction(
            fixed_code="def add(a, b):\n    return a + b",
            explanation="Changed subtraction to addition"
        )
    """
    fixed_code: str          # the agent's corrected Python function
    explanation: str = ""    # optional: why the agent made this fix


# ─────────────────────────────────────────────────────────────
# OBSERVATION — what the agent sees after each step
# NOTE: reward and done are inherited from OpenEnv's Observation
#       base class — do NOT redefine them here
# ─────────────────────────────────────────────────────────────
class DebugObservation(Observation):
    """
    Everything the agent needs to understand the current state.

    Inherited from Observation base:
      reward  : float  — score for this step (set in environment.py)
      done    : bool   — is the episode over? (set in environment.py)

    Custom fields:
      buggy_code, error_message, test_results, etc.
    """
    buggy_code: str             # the original broken function
    error_message: str = ""     # what Python said when it ran
    test_results: list[str] = []  # ["PASS: test_1", "FAIL: test_2", ...]
    tests_passed: int = 0       # number of tests passing right now
    tests_total: int = 0        # total number of tests
    attempts_remaining: int = 5 # how many more tries the agent gets
    solved: bool = False        # True if ALL tests pass
    feedback: str = ""          # plain English hint to guide the agent


# ─────────────────────────────────────────────────────────────
# STATE — metadata about the current episode
# ─────────────────────────────────────────────────────────────
class DebugState(State):
    """
    Episode-level metadata. Used by the training loop
    to track progress across many episodes.
    """
    episode_id: int = 0
    bug_id: str = "none"
    bug_category: str = "none"
    difficulty: str = "none"
    step_count: int = 0
    best_tests_passed: int = 0
