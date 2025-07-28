from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello World! my first FastAPI application"}


@app.get("/about")
def about():
    return {"message": "I am a Software Engineering student at FAST NUCES, Karachi, passionate about AI, machine learning, and innovative software solutions. Skilled in Python, Java, TypeScript, and frameworks like TensorFlow and Scikit-learn, I enjoy building AI-driven applications and solving complex problems. "}

