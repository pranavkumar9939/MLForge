from sklearn.metrics import (
    accuracy_score, 
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from app.services.evaluation.performance_interpreter import interpret_score
from app.services.evaluation.overall_assessment import generate_overall_assessment
from app.services.evaluation.improvement_engine import generate_improvement_suggestions


def evaluate_model(training_result):
    """
    Evaluate the trained machine learning model.
    """

    # y_test = training_result["y_test"]
    # predictions = training_result["predictions"]
    # model_name = training_result["model_name"]
    problem_type = training_result["problem_type"]

    EVALUATORS = {
        "Binary Classification": evaluate_binary_classification
    }

    evaluator = EVALUATORS.get(problem_type)

    if evaluator is None:
        raise ValueError(
            f"Evaluation for '{problem_type}' is not implemented."
        )

    return evaluator(training_result)


def evaluate_binary_classification(training_result):
    

    y_test = training_result["y_test"]
    predictions = training_result["predictions"]
    model_name = training_result["model_name"]
    problem_type = training_result["problem_type"]
            
    
    accuracy = accuracy_score(
        y_test,
        predictions
    )
    
    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )
    
    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )
    
    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )
    
    cm = confusion_matrix(
        y_test,
        predictions
    )
    
    classification_report_dict = classification_report(
        y_test,
        predictions,
        output_dict=True
    )
    
    accuracy_info = interpret_score(
        accuracy,
        "Accuracy"
    )
    
    precision_info = interpret_score(
        precision,
        "Precision"
    )
    
    recall_info = interpret_score(
        recall,
        "Recall"
    )
    
    f1_info = interpret_score(
        f1,
        "F1 Score"
    )
    
    evaluation_result = {
    
        "model_name": model_name,
    
        "problem_type": problem_type,
    
        "accuracy": accuracy_info,
    
        "precision": precision_info,
    
        "recall": recall_info,
    
        "f1_score": f1_info,
    
        "confusion_matrix": cm.tolist(),
    
        "classification_report": classification_report_dict,
    
        "summary": {
            "total_predictions": len(predictions),
            "correct_predictions": int((predictions == y_test).sum())
        }
    }
    
    evaluation_result["overall_assessment"] = generate_overall_assessment(evaluation_result)
    
    evaluation_result["improvement_suggestions"] = generate_improvement_suggestions(evaluation_result)

    return evaluation_result