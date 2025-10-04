import os
import httpx
from .errors import Unauthorized, NotFound, RateLimited

API = "https://api.github.com"

class GitHubClient:
    def __init__(self, token: str | None = None, timeout: float = 20.0):
        token = token or os.getenv("GITHUB_TOKEN")
        if not token:
            raise Unauthorized("GITHUB_TOKEN missing")
        self._client = httpx.AsyncClient(
            base_url=API,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
            },
            timeout=timeout,
        )

    async def _get(self, path: str, **params):
        r = await self._client.get(path, params=params)
        if r.status_code == 401:
            raise Unauthorized(r.text)
        if r.status_code == 404:
            raise NotFound(path)
        if r.status_code == 403 and r.headers.get("X-RateLimit-Remaining") == "0":
            raise RateLimited(r.headers.get("X-RateLimit-Reset"))
        r.raise_for_status()
        return r.json()

    async def list_repos(
        self,
        visibility: str = "all",
        affiliation: str = "owner,collaborator,organization_member",
        per_page: int = 100,
    ):
        page, out = 1, []
        while True:
            batch = await self._get(
                "/user/repos",
                visibility=visibility,
                affiliation=affiliation,
                per_page=per_page,
                page=page,
            )
            out.extend(batch)
            if len(batch) < per_page:
                break
            page += 1
        return out

    async def aclose(self):
        await self._client.aclose()
