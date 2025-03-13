from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.app.controller.simulate_controller import router
from backend.app.controller import simulate_controller

app = FastAPI(title="Credit Simulator API", description="API for credit simulation", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from backend.app.controller.simulate_controller_v2 import router as simulate_v2_router, sqs_service

app.include_router(simulate_v2_router)

app.include_router(router)
app.include_router(simulate_controller.router, prefix="/v2")

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
