from fastapi import FastAPI
import json

app = FastAPI()

def load_patient_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    
    return data

@app.get("/")
def hello():
    return {"message": "Patient Tract API"}

@app.get("/about")
def about():
    return {"message":"A fully functional API for patient record tracking."}


@app.get("/view")
def view():
    data = load_patient_data()
    return data

