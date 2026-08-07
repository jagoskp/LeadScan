from fastapi import FastAPI

app = FastAPI(
    title="LeadScan OCR Engine Service",
    description="Business card and document image text extraction engine (PaddleOCR + Tesseract).",
    version="0.1.0",
)


@app.get("/health", status_code=200)
async def health_check() -> dict[str, str]:
    return {"status": "healthy", "service": "ocr-engine"}
