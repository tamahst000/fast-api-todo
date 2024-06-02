from urls import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app=app, port=8888)

# $ poetry run uvicorn run:app --reload --port 8888

# http://admin:fastapi@127.0.0.1:8888/get