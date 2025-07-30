import streamlit as st
import requests

# Set Streamlit page config
st.set_page_config(page_title="Insurance Category Predictor", page_icon="🔍")

st.title("🩺 Insurance Category Predictor")
st.markdown("Enter your details below to predict your insurance category.")

# Input fields
age = st.number_input("Age", min_value=1, max_value=120, step=1)
weight = st.number_input("Weight (kg)", min_value=1.0, step=0.1)
height = st.number_input("Height (meters)", min_value=0.5, max_value=2.5, step=0.01)
income_lpa = st.number_input("Income (LPA)", min_value=0.1, step=0.1)

smoker = st.radio("Are you a smoker?", ("Yes", "No"))
city = st.text_input("City").strip().title()

occupation = st.selectbox(
    "Occupation",
    ['retired', 'freelancer', 'student', 'government_job',
     'business_owner', 'unemployed', 'private_job']
)

# Predict button
if st.button("🔍 Predict"):
    # Validate required inputs
    if not city:
        st.warning("Please enter your city.")
    else:
        payload = {
            "age": age,
            "weight": weight,
            "height": height,
            "income_lpa": income_lpa,
            "smoker": smoker == "Yes",
            "city": city,
            "occupation": occupation
        }

        try:
            # Call FastAPI endpoint
            response = requests.post("http://127.0.0.1:8000/predict", json=payload)
            if response.status_code == 200:
                category = response.json().get("predicted_category")
                st.success(f"🎯 Predicted Insurance Category: **{category}**")
            else:
                st.error(f"❌ Server returned status code {response.status_code}.")
        except requests.exceptions.ConnectionError:
            st.error("🚫 Could not connect to the FastAPI backend. Make sure it's running.")
        except Exception as e:
            st.error(f"🚨 Unexpected error: {e}")
