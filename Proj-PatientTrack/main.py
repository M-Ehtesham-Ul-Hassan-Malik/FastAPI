from fastapi import FastAPI, Path, HTTPException, Query
import json 
from fastapi.responses import JSONResponse
from typing import Literal
from pydantic import BaseModel, Field
from typing import Annotated, Optional

app = FastAPI()

class Patient(BaseModel):

    id: Annotated[str, Field(..., description="The ID of the patient", example="PT-001")]
    name: Annotated[str, Field(..., description="The name of the patient", example="John Doe")]
    age: Annotated[int, Field(..., description="The age of the patient", example=30, gt=0, lt=120)]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description="The gender of the patient", example="male")]
    contact: Annotated[str, Field(..., description="The contact number of the patient", example="0345-1234567")]
    diagnosis: Annotated[str, Field(..., description="The diagnosis of the patient", example="Migraine")]
    last_visit: Annotated[str, Field(...,description="The last visit date of the patient", example="2022-01-01")]
    height: Annotated[float, Field(...,gt=0, description="The height of the patient in cms", example=170.5)]
    weight: Annotated[float, Field(...,gt=0, description="The weight of the patient in kgs", example=70.2)]
    city: Annotated[str, Field(..., description="The city of the patient", example="Lahore")]
    verdict: Annotated[str, Field(..., description="The verdict of the patient", example="Advised stress management and regular sleep")]

    # "name": "Sana Tariq",
    # "age": 34,
    # "gender": "Female",
    # "contact": "0345-1122334",
    # "diagnosis": "Migraine",
    # "last_visit": "2025-07-25",
    # "height": 165,
    # "weight": 60,
    # "city": "Faisalabad",
    # "verdict": "Advised stress management and regular sleep"

class UpdatePatient(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None)]
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(default=None)]
    contact: Annotated[Optional[str], Field(default=None)]
    diagnosis: Annotated[Optional[str], Field(default=None)]
    last_visit: Annotated[Optional[str], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None)]
    weight: Annotated[Optional[float], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    verdict: Annotated[Optional[str], Field(default=None)]


def load_patient_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    
    return data


def save_patient_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)


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



@app.post("/add")
def add_patient(patient: Patient):

    # load existing data
    data = load_patient_data()
    
    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")
    
    # add the new patient
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save the data
    save_patient_data(data)

    return JSONResponse(status_code=201, content={"message": "Patient added successfully"})


# update
@app.put("/update/{patient_id}")
def update_patient(patient_id: str, update_patient: UpdatePatient):

    # load data
    data = load_patient_data()

    # check if patient id already exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient does not exists")
    
    # update the patient
    existing_patient_info = data[patient_id]

    updated_patient_info =  update_patient.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        if value is not None:
            existing_patient_info[key] = value

    
    existing_patient_info['id'] = patient_id
    patient_pydantic_object = Patient(**existing_patient_info)

    existing_patient_info = patient_pydantic_object.model_dump(exclude=['id'])

    # add this dict into data
    data[patient_id] = existing_patient_info

    # save the data
    save_patient_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient updated successfully"})














