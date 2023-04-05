from fastapi import FastAPI

app = FastAPI()

@app.route('/')
def hello():
    print("Hello world")

if __name__ == "__main__":
    app.run()