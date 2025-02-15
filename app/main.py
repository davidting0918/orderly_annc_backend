import logging
import os
from argparse import ArgumentParser
from logging.handlers import TimedRotatingFileHandler
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi import FastAPI

from app.auth.routes import router as auth_router
from app.chat_info.routes import router as chat_info_router
from app.config.setting import settings as s
from app.tickets.routes import router as tickets_router
from app.users.routes import router as users_router

cp = os.path.dirname(os.path.realpath(__file__))
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:8000",
]

def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = TimedRotatingFileHandler(
        f"{cp}/logs/main.log",
        when="midnight",
        interval=1,
    )

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

app = FastAPI()

# Apply CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = setup_logger("main")

@app.middleware("http")
async def log_requests(request, call_next):
    auth_key = request.headers.get("X-API-KEY", "No API Key")
    params = request.query_params
    client_ip = request.client.host if request.client else "Unknown IP"
    logger.info(f"Request received: {request.method} - {request.url.path} - {params} - {auth_key} - {client_ip}")
    response = await call_next(request)
    logger.info(f"Response sent: {response.status_code}")
    return response

# Include routers
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(chat_info_router, prefix="/chats", tags=["Chats"])
app.include_router(tickets_router, prefix="/tickets", tags=["Tickets"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

if __name__ == "__main__":
    args = ArgumentParser("Run the FastAPI server for announcement system")
    args.add_argument("--test", action="store_true", help="Run the server in test mode", default=False)
    args = args.parse_args()

    s.is_test = args.test  # Ensure test mode is set correctly
    uvicorn.run(app, host="0.0.0.0", port=8000)
