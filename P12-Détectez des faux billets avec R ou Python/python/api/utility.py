import joblib
import pandas as pd
import numpy as np

def _load_model(path):
    try:
        model = joblib.load(path)

    except Exception as e:                       
        raise RuntimeError(f"Modèle non disponible: {e}") from e 

    return model

def _predict_bill(df: pd.DataFrame, model):
    """Predict by using the loaded model

    Args:
        df (pd.DataFrame): df with only feature columns
        model (LogisticRegression): loaded model

    Returns:
        tuple: (labels, predictions, proba_true, proba_false)
    """
    DECISION_THRESHOLD = 0.7636

    proba = model.predict_proba(df)
    proba_false = proba[:, 0] # the probability of a bill being fake
    proba_true = proba[:, 1]
    predictions = np.where(proba_false >= DECISION_THRESHOLD, False, True)

    label_map = {True: 'Real', False: 'Fake'}
    labels = [label_map[bool(p)] for p in predictions]

    return (labels, predictions, proba_true, proba_false)

def _make_result(tuple):
    return {
        "predictions": [
            {
                "index": index,
                "prediction": label,
                "is_genuine": bool(pred),
                "proba_real": float(prob_r),
                "proba_fake": float(prob_f)
            }
            for index, (label, pred, prob_r, prob_f) in enumerate(zip(tuple[0], tuple[1], tuple[2], tuple[3]))
        ]
    }