from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.rpc import rpc  # expects your dispatcher object with .dispatch(...)

app = FastAPI()

@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/rpc")
async def rpc_endpoint(req: Request):
    payload = await req.json()
    # Delegate to your JSON-RPC dispatcher; it should return a dict JSON-RPC response
    resp = await rpc.dispatch(payload)
    return JSONResponse(resp)
