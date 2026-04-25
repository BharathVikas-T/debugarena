"""
DebugArena — server/environment.py
=====================================
The brain of the environment.

What happens each episode:
  1. reset()  → pick a random buggy program, return it to the agent
  2. step()   → agent sends a fix → run it in a sandbox → check tests → return reward
  3. state()  → return metadata about this episode

The sandbox:
  We use Python's exec() with a restricted scope.
  The agent's code runs in isolation — it cannot import os, sys, etc.
  This is safe enough for a hackathon. (Production would use Docker.)
"""

import random
from openenv.core.env_server import Environment
from models import DebugAction, DebugObservation, DebugState
from bugs import BUGS


class DebugArenaEnvironment(Environment):
    """
    DebugArena: an RL environment where an agent learns to fix buggy Python code.

    Reward signal:
      +1.0  per test that passes (normalized by total tests)
      +2.0  bonus if ALL tests pass (full solve)
      -0.1  small penalty per failed attempt (encourages efficiency)
      -0.3  if the fixed code crashes with an error

    Episode ends when:
      - All tests pass (success), OR
      - Agent runs out of attempts (max 5 per episode)
    """

    MAX_ATTEMPTS = 5

    def __init__(self):
        self.current_bug = None
        self.attempt_count = 0
        self.episode_id = 0
        self.best_tests_passed = 0
        self.done = False

    # ──────────────────────────────────────────────────────────
    # reset() — start a new episode with a fresh bug
    # ──────────────────────────────────────────────────────────
    def reset(self) -> DebugObservation:
        self.current_bug = random.choice(BUGS)
        self.attempt_count = 0
        self.episode_id += 1
        self.best_tests_passed = 0
        self.done = False

        # Run the buggy code first so the agent sees the error immediately
        error_msg, test_results, tests_passed = self._run_tests(
            self.current_bug["buggy_code"]
        )

        return DebugObservation(
            buggy_code=self.current_bug["buggy_code"],
            error_message=error_msg,
            test_results=test_results,
            tests_passed=tests_passed,
            tests_total=len(self.current_bug["tests"]),
            attempts_remaining=self.MAX_ATTEMPTS,
            solved=False,
            feedback=(
                f"New bug: '{self.current_bug['name']}' "
                f"[{self.current_bug['difficulty']}] — "
                f"Hint: {self.current_bug['hint']}"
            ),
            reward=0.0,
            done=False
        )

    # ──────────────────────────────────────────────────────────
    # step() — agent proposes a fix, we test it
    # ──────────────────────────────────────────────────────────
    def step(self, action: DebugAction):
        self.attempt_count += 1

        # Run the agent's fix through all tests
        error_msg, test_results, tests_passed = self._run_tests(action.fixed_code)

        total_tests = len(self.current_bug["tests"])
        solved = (tests_passed == total_tests)
        crashed = bool(error_msg and "Error" in error_msg)
        self.best_tests_passed = max(self.best_tests_passed, tests_passed)

        # ── Multiple reward functions (per hackathon guide) ───
        reward, reward_breakdown = self._compute_total_reward(
            action.fixed_code, tests_passed, total_tests, crashed
        )

        # ── Human-readable feedback ───────────────────────────
        if solved:
            feedback = f"✅ SOLVED! All {total_tests} tests pass. Reward breakdown: {reward_breakdown}"
        elif crashed:
            feedback = f"❌ Code crashed: {error_msg[:100]}. Breakdown: {reward_breakdown}"
        else:
            feedback = (
                f"Passed {tests_passed}/{total_tests} tests. "
                f"{self.MAX_ATTEMPTS - self.attempt_count} attempts left. "
                f"Breakdown: {reward_breakdown}"
            )

        attempts_remaining = self.MAX_ATTEMPTS - self.attempt_count
        episode_done = solved or (attempts_remaining <= 0)
        self.done = episode_done

        obs = DebugObservation(
            buggy_code=self.current_bug["buggy_code"],
            error_message=error_msg,
            test_results=test_results,
            tests_passed=tests_passed,
            tests_total=total_tests,
            attempts_remaining=attempts_remaining,
            solved=solved,
            feedback=feedback,
            reward=reward,
            done=episode_done
        )

        return obs

    # ──────────────────────────────────────────────────────────
    # state() — metadata for the training loop
    # ──────────────────────────────────────────────────────────
    @property
    def state(self) -> DebugState:
        return DebugState(
            episode_id=self.episode_id,
            bug_id=self.current_bug["id"] if self.current_bug else "none",
            bug_category=self.current_bug["category"] if self.current_bug else "none",
            difficulty=self.current_bug["difficulty"] if self.current_bug else "none",
            step_count=self.attempt_count,
            best_tests_passed=self.best_tests_passed
        )

    # ──────────────────────────────────────────────────────────
    # _run_tests() — execute code in sandbox, run each test
    # ──────────────────────────────────────────────────────────
    # ──────────────────────────────────────────────────────────
    # MULTIPLE REWARD FUNCTIONS (as required by hackathon guide)
    # ──────────────────────────────────────────────────────────

    def _reward_tests_passing(self, tests_passed, total_tests):
        """Reward 1: proportion of tests passing."""
        return round((tests_passed / total_tests) * 1.0, 3)

    def _reward_full_solve(self, tests_passed, total_tests):
        """Reward 2: bonus for solving ALL tests — incentivises complete fixes."""
        return 2.0 if tests_passed == total_tests else 0.0

    def _reward_format_compliance(self, code):
        """Reward 3: does the code look like a valid Python function?
        Penalises empty submissions or non-function responses."""
        if not code or not code.strip():
            return -0.5
        has_def = any(line.strip().startswith("def ") for line in code.split("\n"))
        return 0.2 if has_def else -0.3

    def _reward_no_hacking(self, code):
        """Reward 4: anti-reward-hacking check.
        Penalises use of forbidden globals, imports, or shortcuts
        that could game the environment without actually fixing the bug."""
        FORBIDDEN = [
            "import os", "import sys", "import subprocess",
            "__globals__", "globals()", "locals()",
            "open(", "exec(", "eval(",
            "builtins", "__import__",
            "exit(", "quit(",
        ]
        code_lower = code.lower()
        for pattern in FORBIDDEN:
            if pattern.lower() in code_lower:
                return -1.0  # heavy penalty for attempted hacking
        return 0.1  # small bonus for clean code

    def _compute_total_reward(self, code, tests_passed, total_tests, crashed):
        """Combine all reward signals into one total score."""
        r1 = self._reward_tests_passing(tests_passed, total_tests)
        r2 = self._reward_full_solve(tests_passed, total_tests)
        r3 = self._reward_format_compliance(code)
        r4 = self._reward_no_hacking(code)
        crash_penalty = -0.3 if crashed else 0.0

        total = r1 + r2 + r3 + r4 + crash_penalty
        return round(total, 3), {
            "tests_passing": r1,
            "full_solve_bonus": r2,
            "format_compliance": r3,
            "anti_hacking": r4,
            "crash_penalty": crash_penalty,
        }

    def _run_tests(self, code: str):
        """
        Run `code` in a HARDENED sandbox, then call the function
        with each test input and check the output.

        Anti-hacking measures:
          - Forbidden imports blocked (os, sys, subprocess, etc.)
          - No access to __globals__ or builtins manipulation
          - Timeout via signal would go here in production
          - Each test runs independently so one crash doesn't block others

        Returns:
            error_message : str
            test_results  : list of "PASS/FAIL: ..." strings
            tests_passed  : int
        """
        test_results = []
        tests_passed = 0
        error_message = ""

        # ── Anti-hacking: check for forbidden patterns BEFORE exec ──
        FORBIDDEN_IMPORTS = ["os", "sys", "subprocess", "socket", "builtins"]
        for forbidden in FORBIDDEN_IMPORTS:
            if f"import {forbidden}" in code:
                return (
                    f"SecurityError: import of '{forbidden}' is not allowed.",
                    [f"BLOCKED: Forbidden import detected — '{forbidden}'"],
                    0
                )

        # ── Restricted sandbox — no access to real builtins ──────────
        SAFE_BUILTINS = {
            "abs": abs, "all": all, "any": any, "bin": bin,
            "bool": bool, "chr": chr, "dict": dict, "dir": dir,
            "divmod": divmod, "enumerate": enumerate, "filter": filter,
            "float": float, "format": format, "frozenset": frozenset,
            "getattr": getattr, "hasattr": hasattr, "hash": hash,
            "hex": hex, "int": int, "isinstance": isinstance,
            "issubclass": issubclass, "iter": iter, "len": len,
            "list": list, "map": map, "max": max, "min": min,
            "next": next, "oct": oct, "ord": ord, "pow": pow,
            "print": print, "range": range, "repr": repr,
            "reversed": reversed, "round": round, "set": set,
            "slice": slice, "sorted": sorted, "str": str,
            "sum": sum, "tuple": tuple, "type": type, "zip": zip,
            "None": None, "True": True, "False": False,
        }
        sandbox = {"__builtins__": SAFE_BUILTINS}

        # ── Compile and execute ───────────────────────────────────────
        try:
            exec(compile(code, "<agent_fix>", "exec"), sandbox)
        except SyntaxError as e:
            return f"SyntaxError: {e}", [f"SYNTAX ERROR: {e}"], 0
        except Exception as e:
            return f"RuntimeError during load: {e}", [f"LOAD ERROR: {e}"], 0

        # ── Find the function name ────────────────────────────────────
        func_name = None
        for line in code.strip().split("\n"):
            stripped = line.strip()
            if stripped.startswith("def "):
                func_name = stripped.split("(")[0].replace("def ", "").strip()
                break

        if not func_name or func_name not in sandbox:
            return "Could not find function definition.", ["ERROR: No function found"], 0

        func = sandbox[func_name]

        # ── Run each test independently ───────────────────────────────
        for i, test in enumerate(self.current_bug["tests"]):
            inp = test["input"]
            expected = test["expected"]
            try:
                result = func(*inp) if isinstance(inp, tuple) else func(inp)
                if result == expected:
                    tests_passed += 1
                    test_results.append(f"PASS: test_{i+1} — got {result!r}")
                else:
                    test_results.append(
                        f"FAIL: test_{i+1} — expected {expected!r}, got {result!r}"
                    )
            except RecursionError:
                test_results.append(f"ERROR: test_{i+1} — RecursionError (infinite loop?)")
                error_message = "RecursionError: possible infinite recursion"
            except Exception as e:
                test_results.append(f"ERROR: test_{i+1} — {type(e).__name__}: {e}")
                error_message = f"{type(e).__name__}: {e}"

        return error_message, test_results, tests_passed