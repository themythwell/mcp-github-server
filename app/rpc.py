from typing import Any, Callable, Dict, Optional, Tuple
from pydantic import BaseModel, ValidationError

class SimpleRPC:
    def __init__(self) -> None:
        self._methods: Dict[str, Tuple[Callable[..., Any], Optional[type[BaseModel]]]] = {}

    def register(self, name: str, func: Callable[..., Any], params_model: Optional[type[BaseModel]] = None) -> None:
        self._methods[name] = (func, params_model)

    async def dispatch(self, payload: dict) -> dict:
        jsonrpc = payload.get("jsonrpc")
        req_id = payload.get("id")
        method = payload.get("method")
        params = payload.get("params", {})

        if jsonrpc != "2.0":
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": "Invalid Request"}}
        if method not in self._methods:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

        func, ParamsModel = self._methods[method]
        try:
            params_obj = ParamsModel(**params) if ParamsModel else params
        except ValidationError as e:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": "Invalid params", "data": e.errors()}}

        try:
            result = await func(params_obj)  # handlers are async
            # Normalize Pydantic models to dicts
            if isinstance(result, list) and result and isinstance(result[0], BaseModel):
                result = [r.model_dump() for r in result]
            elif isinstance(result, BaseModel):
                result = result.model_dump()
            return {"jsonrpc": "2.0", "id": req_id, "result": result}
        except Exception as e:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32000, "message": str(e)}}

rpc = SimpleRPC()

# --- registrations ---
from app.models.github import ListReposParams  # noqa: E402
from app.tools.github_tools import list_repos as gh_list_repos  # noqa: E402
rpc.register("tools.listRepos", gh_list_repos, params_model=ListReposParams)
