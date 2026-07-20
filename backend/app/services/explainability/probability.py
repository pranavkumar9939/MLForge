import numpy as np

def get_prediction_probabilities(
    model,
    input_data,
    label_encoder = None
):

    if not hasattr(model, "predict_proba"):
        return []

    probabilities = []

    probabilities = model.predict_proba(input_data)[0]

    classes = model.classes_

    if label_encoder is not None:

        classes = label_encoder.inverse_transform(classes)

    result = []

    for cls, prob in zip(classes, probabilities):

        result.append(
            {
                "class": str(cls),
                "probability": round(float(prob * 100), 2)
            }
        )

    result.sort(
        key = lambda x: x["probability"],
        reverse = True
    )

    return result