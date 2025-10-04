from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Union

app = FastAPI()

class RPC(BaseModel):
    jsonrpc: str
    id: Union[int, str, None] = None
    method: str
    params: Union[dict, None] = None

TOOLS = {
    "tools": [
        {
            "name": "listFiles",
            "description": "List files under a path in the repo.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path or empty for root"}
                }
            },
        },
        {
            "name": "readFile",
            "description": "Read UTF-8 file content (256KB cap).",
            "inputSchema": {
                "type": "object",
                "required": ["path"],
                "properties": {"path": {"type": "string"}}
            },
        },
    ]
}

@app.post("/mcp")
async def mcp(req: Request):
    body = await req.json()
    rpc = RPC(**body)

    if rpc.method == "tools/list":
        return {"jsonrpc": "2.0", "id": rpc.id, "result": TOOLS}

    return {
        "jsonrpc": "2.0",
        "id": rpc.id,
        "error": {"code": -32601, "message": "Unknown method"}
    }