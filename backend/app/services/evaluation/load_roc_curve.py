import json 
import os

def load_roc_curve(model_directory):

    file_path = os.path.join(
        model_directory,
        "roc_curve.json"
    )

    if not os.path.exists(file_path):
        return None
    with open(file_path) as f:
        return json.load(f)