import joblib
import os
import json


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    )
)

MODEL_DIR = os.path.join(BASE_DIR, "saved_models")

os.makedirs(MODEL_DIR, exist_ok=True)

def save_model(
        model,
        pipeline,
        label_encoder,
        feature_names,
        metadata,
        dataset_name,
        model_name,
        evaluation,
        roc_curve,
        confusion_matrix,
        background_data,

        tuned = False,
        best_params = None,
        best_cv_score = None
):

    dataset_folder = os.path.join(MODEL_DIR, dataset_name)
    model_folder = os.path.join(dataset_folder, model_name)

    os.makedirs(model_folder, exist_ok = True)
    
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    model_path = os.path.join(model_folder, "model.pkl")
    pipeline_path = os.path.join(model_folder, "pipeline.pkl")
    label_encoder_path = os.path.join(model_folder, "label_encoder.pkl")
    feature_names_path = os.path.join(model_folder, "feature_names.json")
    metadata_path = os.path.join(model_folder, "metadata.json")
    evaluation_path = os.path.join(model_folder, "evaluation.json")
    background_data_path = os.path.join(model_folder, "background_data.pkl")
    roc_curve_path = os.path.join(model_folder, "roc_curve.json")
    confusion_matrix_path = os.path.join(model_folder, "confusion_matrix.json")
    hyperparameter_tuning_path = os.path.join(model_folder, "hyperparameter_tuning.json")

    joblib.dump(model, model_path)
    joblib.dump(pipeline, pipeline_path)
    joblib.dump(background_data, background_data_path)

    if label_encoder is not None:
        joblib.dump(label_encoder, label_encoder_path)

    with open(feature_names_path, "w") as f:
        json.dump(feature_names, f, indent=4)

    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=4)

    with open(evaluation_path, "w") as f:
        json.dump(evaluation, f, indent=4)

    with open(roc_curve_path, "w") as f:
        json.dump(roc_curve, f, indent=4 )

    with open(confusion_matrix_path, "w") as f:
        json.dump(confusion_matrix, f)

    tuning_data = {
        "tuned": tuned,
        "best_params": best_params or {},
        "best_cv_score": best_cv_score
    }

    with open(hyperparameter_tuning_path, "w") as f:
        json.dump(tuning_data, f, indent = 4)

