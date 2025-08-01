import pickle
import pandas as pd

# import the ml model
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)


# ML Flow for model version
MODEL_VERSION = '1.0.0'

def predict_output(input_df: dict):

    input_df = pd.DataFrame([input_df])
    output = model.predict(input_df)[0]
    
    # Get confidence scores for all classes
    if hasattr(model, "predict_proba"):
        confidence_scores = model.predict_proba(input_df)[0]
        class_labels = model.classes_
        confidences = dict(zip(class_labels, confidence_scores))
    else:
        confidences = None  # Model does not support probability prediction

    return {
        "prediction": output,
        "confidences": confidences
    }