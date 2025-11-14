from fastapi import FastAPI, Request, Header, HTTPException
import os
import httpx

app = FastAPI()

LITELLM_BACKEND = os.getenv("LITELLM_BACKEND", "https://real-litellm-backend.local")
# Or your model loader logic if local

SECRET_KEY = os.getenv("LITELLM_SECRET_KEY")  # set in Coolify env, never in frontend

@app.post("/v1/{path:path}")
async def proxy(path: str, request: Request, authorization: str | None = Header(None)):
    # Basic domain/auth checks can be done by Coolify Traefik allowed origins; keep server-simple
    if SECRET_KEY is None:
        raise HTTPException(500, "Server not configured")
    payload = await request.body()
    headers = {"Authorization": f"Bearer {SECRET_KEY}", "Content-Type": request.headers.get("content-type", "application/json")}
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{LITELLM_BACKEND}/v1/{path}", content=payload, headers=headers, timeout=120)
    return resp.json()
