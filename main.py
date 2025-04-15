import uvicorn


def run_server():
    uvicorn.run(app="api.app:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run_server()
