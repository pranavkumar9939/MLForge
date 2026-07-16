from app.services.model_training.model_selector import select_model

model_info = select_model("Binary Classification")

print(model_info)