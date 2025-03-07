from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from app.routes import router
import uvicorn

app = FastAPI(title="Credit Simulator API", description="API for credit simulation", version="1.0")

app.include_router(router)

@app.get("/health")
def health():
    """
    Checks the health status of the application.

    Returns:
        dict: A dictionary containing the application status.
    """
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
