import os
import json
import asyncio
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from google import genai
from google.genai import types

app = FastAPI(title="Dream11 Anti-Jinx Chaos Engine")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client() if GEMINI_API_KEY else None

class LiveTelemetryPacket(BaseModel):
    source_feed: str
    ball_identifier: str
    event_type: str
    raw_payload: str

    @validator("raw_payload")
    def filter_adversarial_injections(cls, value):
        if not value or len(value.strip()) < 5:
            raise ValueError("Telemetry packet payload corrupted.")
        forbidden_tokens = ["ignore previous instructions", "system override", "force system override"]
        if any(token in value.lower() for token in forbidden_tokens):
            raise ValueError("Adversarial payload token isolated.")
        return value

class ChaosHedgeSchema(BaseModel):
    anxiety_sentiment_context: str = Field(description="1-sentence analysis of the superstitious panic levels.")
    anti_jinx_roster_hedge: str = Field(description="2 counter-intuitive player choices to capitalize on public panic.")
    chaos_coaching_tip: str = Field(description="A tactical strategy for modifying a live fantasy lineup under pressure.")

LOCAL_MATHEMATICAL_FALLBACK = {
    "anxiety_sentiment_context": "[FALLBACK MODE] Peak traffic event loop active. Switched to edge memory.",
    "anti_jinx_roster_hedge": "[FALLBACK MODE] Public panic at 94%. Swap out reactive top-order bats for steady death-over bowlers.",
    "chaos_coaching_tip": "[FALLBACK MODE] Pivot your captain selection to the primary death-over specialist immediately."
}

async def compute_anti_jinx_hedges(clean_logs: str) -> dict:
    if not client:
        raise HTTPException(status_code=500, detail="Gemini API Key missing.")
    prompt = f"Extract psychological pressure trends and compute a contrarian strategy:\n{clean_logs}"
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ChaosHedgeSchema,
            temperature=0.3
        ),
    )
    return json.loads(response.text)

@app.get("/api/insights")
async def get_match_insights():
    execution_timer_start = time.time()
    try:
        if not os.path.exists("live_match_feed.json"):
            return {"engine_status": "Stalled", "data": LOCAL_MATHEMATICAL_FALLBACK}
        with open("live_match_feed.json", "r") as f:
            ingested_json_feed = json.load(f)
        
        processed_clean_packets = []
        isolated_adversarial_count = 0
        for packet in ingested_json_feed:
            try:
                processed_clean_packets.append(LiveTelemetryPacket(**packet))
            except ValueError:
                isolated_adversarial_count += 1
                continue
        if not processed_clean_packets:
            return {"engine_status": "CRITICAL_SAFETY_STOP", "data": LOCAL_MATHEMATICAL_FALLBACK}
        
        compiled_string_payload = "\n".join([f"[{p.source_feed}] Ball {p.ball_identifier}: {p.raw_payload}" for p in processed_clean_packets])
        
        try:
            analytical_insights = await asyncio.wait_for(compute_anti_jinx_hedges(compiled_string_payload), timeout=3.0)
            latency = (time.time() - execution_timer_start) * 1000
            return {"engine_status": "HEALTHY_SECURE_NODE", "pipeline_latency_ms": f"{latency:.2f}ms", "data": analytical_insights}
        except asyncio.TimeoutError:
            latency = (time.time() - execution_timer_start) * 1000
            return {"engine_status": "CIRCUIT_BREAKER_ACTIVE", "pipeline_latency_ms": f"{latency:.2f}ms", "data": LOCAL_MATHEMATICAL_FALLBACK}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
