from fastapi import FastAPI, Path, HTTPException
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

@app.get("/patient/{patient_id}")
def get_patient(patient_id: str = Path(..., description="The ID of the patient you want to retrieve", example="PT-001")):
    
    # load all the patients
    data = load_patient_data()
    
    # find the patient
    if patient_id in data:
        return data[patient_id]
    else:
        # return {"message": "Patient not found"}
        raise HTTPException(status_code=404, detail="Patient not found")
    

