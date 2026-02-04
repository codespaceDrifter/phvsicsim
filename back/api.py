from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

# Paths
ROOT = Path(__file__).parent.parent
LOGS_DIR = ROOT / "logs"
DIST_DIR = ROOT / "front" / "dist"


# --- Recording Endpoints ---

@app.get("/recordings/{name}/{chunk}")
async def get_recording(name: str, chunk: str):
    recording_path = LOGS_DIR / name / f"{chunk}.bin"

    print(f"Serving: {recording_path}")

    if not recording_path.exists():
        return JSONResponse({"error": "Not found"}, status_code=404)

    return FileResponse(recording_path, media_type="application/octet-stream")


@app.get("/health")
async def health():
    return {"status": "ok"}


# --- Worlds List (for frontend) ---

@app.get("/worlds")
async def list_worlds():
    """List all available worlds (recordings)."""
    worlds = [d.name for d in LOGS_DIR.iterdir() if d.is_dir()]
    return {"worlds": worlds}


# --- Serve built frontend (must be after API routes) ---

app.mount("/assets", StaticFiles(directory=DIST_DIR / "assets"), name="assets")


@app.get("/")
async def index():
    return FileResponse(DIST_DIR / "index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
