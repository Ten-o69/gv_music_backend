import uvicorn

from api.app import app


def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000, limit_max_requests=100000000)


if __name__ == "__main__":
    run_server()
