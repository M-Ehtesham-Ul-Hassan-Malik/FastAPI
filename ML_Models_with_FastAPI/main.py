from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pandas as pd
import pickle

# Load model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

app = FastAPI()

# Cities
tier_1_cities = [
    "Karachi", "Lahore", "Islamabad", "Rawalpindi", "Faisalabad", "Multan", "Peshawar"
]

tier_2_cities = [
    "Quetta", "Hyderabad", "Sialkot", "Gujranwala", "Sargodha", "Bahawalpur", "Sukkur",
    "Larkana", "Abbottabad", "Mardan", "Mirpur", "Muzaffarabad", "Dera Ghazi Khan", "Rahim Yar Khan",
    "Okara", "Kasur", "Sheikhupura", "Chiniot", "Gujrat", "Jhelum", "Turbat", "Nawabshah",
    "Mingora", "Khuzdar", "Dera Ismail Khan", "Gilgit", "Skardu", "Mansehra", "Bannu",
    "Swabi", "Jamshoro", "Attock", "Thatta", "Charsadda", "Kohat", "Tando Adam", "Jacobabad",
    "Vehari", "Khanewal", "Kotli", "Tando Allahyar", "Nowshera", "Haripur", "Shikarpur"
]

# Input model
class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the user')]
    weight: Annotated[float, Field(..., gt=0, description='Weight in kg')]
    height: Annotated[float, Field(..., gt=0, lt=2.5, description='Height in meters')]
    income_lpa: Annotated[float, Field(..., gt=0, description='Income in LPA')]
    smoker: Annotated[bool, Field(..., description='Is the user a smoker?')]
    city: Annotated[str, Field(..., description='City name')]
    occupation: Annotated[
        Literal[
            'retired', 'freelancer', 'student', 'government_job',
            'business_owner', 'unemployed', 'private_job'
        ],
        Field(..., description='User occupation')
    ]

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        return "low"

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3


@app.post('/predict')
def predict_premium(data: UserInput):
    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }])

    prediction = model.predict(input_df)[0]
    return JSONResponse(status_code=200, content={'predicted_category': prediction})
