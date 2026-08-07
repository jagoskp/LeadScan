from fastapi import FastAPI

app = FastAPI(
    title="LeadScan AI Engine Service",
    description="Background intelligence, embedding and verification service.",
    version="0.1.0",
)


@app.get("/health", status_code=200)
async def health_check() -> dict[str, str]:
    return {"status": "healthy", "service": "ai-engine"}
