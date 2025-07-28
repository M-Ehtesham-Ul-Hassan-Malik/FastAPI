from fastapi import FastAPI, Path, HTTPException, Query
import json
from typing import Literal


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

@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort by: id, last_visit, height, or weight"),
    order: Literal['asc', 'desc'] = Query('asc', description="Sort order: asc or desc")
):
    valid_fields = ['id', 'last_visit', 'height', 'weight']

    data = load_patient_data()  # dict

    reverse = True if order == 'desc' else False

    if sort_by == 'id':
        # Sort by the dictionary keys
        sorted_data = dict(sorted(data.items(), key=lambda x: x[0], reverse=reverse))
    else:
        # Sort by a field inside each patient
        sorted_data = dict(
            sorted(
                data.items(),
                key=lambda x: x[1].get(sort_by, ""),
                reverse=reverse
            )
        )

    return {"sorted_by": sort_by, "order": order, "data": sorted_data}