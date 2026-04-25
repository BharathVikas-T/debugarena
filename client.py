import httpx
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class DebugAction:
    fixed_code: str
    explanation: str = ""

    def to_dict(self):
        return asdict(self)


class DebugArenaClient:
    """Async HTTP client. Works in Colab and locally."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.replace("ws://", "http://").replace("wss://", "https://")
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=30.0)
        return self

    async def __aexit__(self, *args):
        if self._client:
            await self._client.aclose()

    async def reset(self) -> dict:
        resp = await self._client.post("/reset", json={})
        resp.raise_for_status()
        data = resp.json()
        return data.get("observation", data)

    async def step(self, action: DebugAction) -> dict:
        resp = await self._client.post("/step", json=action.to_dict())
        resp.raise_for_status()
        return resp.json()

    async def state(self) -> dict:
        resp = await self._client.get("/state")
        resp.raise_for_status()
        return resp.json()


class SyncDebugArenaClient:
    """Sync version — use inside TRL reward functions."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.replace("ws://", "http://")
        self._client = httpx.Client(base_url=self.base_url, timeout=30.0)

    def reset(self) -> dict:
        resp = self._client.post("/reset", json={})
        resp.raise_for_status()
        data = resp.json()
        return data.get("observation", data)

    def step(self, action: DebugAction) -> dict:
        resp = self._client.post("/step", json=action.to_dict())
        resp.raise_for_status()
        return resp.json()

    def state(self) -> dict:
        resp = self._client.get("/state")
        resp.raise_for_status()
        return resp.json()

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


if __name__ == "__main__":
    import asyncio

    async def smoke_test():
        print("=" * 50)
        print("DebugArena — Smoke Test")
        print("=" * 50)

        async with DebugArenaClient("http://localhost:8000") as env:
            obs = await env.reset()
            print(f"\n Bug: {obs.get('feedback', '')[:70]}")
            print(f" Code:\n{obs.get('buggy_code', '')}")
            print(f" Error: {obs.get('error_message') or 'none'}")
            print(f" Tests: {obs.get('tests_passed', 0)}/{obs.get('tests_total', 0)} passing")

            print("\n--- Attempt 1: submitting buggy code unchanged ---")
            result = await env.step(DebugAction(
                fixed_code=obs.get("buggy_code", ""),
                explanation="no change"
            ))
            obs2 = result.get("observation", {})
            print(f" Reward: {result.get('reward')}")
            print(f" Feedback: {obs2.get('feedback', '')[:70]}")

            state = await env.state()
            print(f"\n State: episode={state.get('episode_id')}, bug={state.get('bug_id')}, difficulty={state.get('difficulty')}")

        print("\n✅ Smoke test passed! Server is running correctly.")

    asyncio.run(smoke_test())