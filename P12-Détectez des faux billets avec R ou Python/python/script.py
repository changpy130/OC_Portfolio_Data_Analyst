#!/usr/bin/env python3

import pandas as pd
import numpy as np
import joblib
import sys, argparse
from sklearn.linear_model import LogisticRegression

# region Utility
FEATURE_COLUMNS = ['diagonal', 'height_left', 'height_right', 'margin_low', 'margin_up', 'length']

def parse():
    """Parse the arguments from command line

    Returns:
        DataFrame
    """
    parser = argparse.ArgumentParser(
        description="Detection of fake bills"
    )
    # User needs to choose ONE of the options; (required=True): cannot skip it
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--csv", 
        help="Import CSV file"
    )
    group.add_argument(
        "--values",
        help="Input directly 6 values",
        nargs=6,
        type=float,
        metavar=('diagonal', 'height_left', 'height_right', 'margin_low', 'margin_up', 'length')
    )
    args = parser.parse_args()

    if args.csv is not None:
        df = _load_data(args.csv)
        df = _validate_data(df)

    elif args.values is not None:
        bill_dict = {
            'diagonal': args.values[0],
            'height_left': args.values[1],
            'height_right': args.values[2],
            'margin_low': args.values[3],
            'margin_up': args.values[4],
            'length': args.values[5]
        }
        df = _load_data(bill_dict)

    return df

def _load_data(source):
    """
    source can be:
    - a string (path to CSV)
    - a dict or list of values (single bill)
    """
    if isinstance(source, str):
        df = pd.read_csv(
            source, 
            sep=',',
            encoding='utf-8',
            na_values=['..', 'NA', 'N/A', '']
        )
    else:
        df = pd.DataFrame([source])
    
    return df


def _validate_data(df) -> pd.DataFrame:
    """Validate that the DataFrame has the expected columns
    
    Args:
        df (DataFrame)
    
    Returns:
        df: only the rows with <= 1 missing value
    """
    # Check missing columns
    missing_columns = [col for col in FEATURE_COLUMNS if col not in df.columns]
    if missing_columns:
        print(f"❌ Error Missing Columns: {missing_columns}")
        print(f"Expected columns: {FEATURE_COLUMNS}")
        print(f"Received columns: {list(df.columns)}")
        sys.exit(1)

    # Check missing values per row
    missing_per_row = df[FEATURE_COLUMNS].isnull().sum(axis=1)
    
    bad_rows = df[missing_per_row > 1].copy()
    good_rows = df[missing_per_row <= 1].copy()

    if len(bad_rows) > 0:
        print(f"⚠️  {len(bad_rows)} bill(s) skipped (too many missing values):")
        print(bad_rows[['id']].to_string(index=False))

    if len(good_rows) == 0:
        print("❌ No valid bills to predict —> aborting.")
        sys.exit(1)

    return good_rows
    

def load_model(path) -> LogisticRegression:
    try:
        model = joblib.load(path)

    except FileNotFoundError:
        print(f"⚠️ Load model error: can't find file at {path}")
        sys.exit(1)  # 0 = success / not 0 = failure

    return model

def process_data(df):
    """Separate feature columns and id column

    Args:
        df (DataFrame)

    Returns:
        tuple: (df_id, df_features)
    """
    features = df[FEATURE_COLUMNS]

    if 'id' in df.columns:
        ids = df['id']
    else:
        ids = pd.Series(['single_bill'])

    return (ids, features)

# region Main Functions

def predict_bill(df: pd.DataFrame, model: LogisticRegression):
    """Predict by using the loaded model

    Args:
        df (pd.DataFrame): df with only feature columns
        model (LogisticRegression): loaded model

    Returns:
        tuple: (array of predicted result, array of probabilities)
    """
    DECISION_THRESHOLD = 0.7636

    proba = model.predict_proba(df)
    proba_false = proba[:, 0] # the probability of a bill being fake
    predictions = np.where(proba_false >= DECISION_THRESHOLD, False, True)

    return (predictions, proba_false)

def main():
    df = parse()
    model = load_model("is_genuine_model.pkl")

    df_id, df_features = process_data(df)
    predictions, proba = predict_bill(df_features, model)

    result = pd.DataFrame({
        'id': df_id,
        'prediction': predictions,
        'probability_of_being_fake': proba
    })

    result['prediction'] = result['prediction'].map({True: 'Real', False: 'Fake'})
    result.to_csv("predictions_output.csv", index=False)

    print(result) # show in console
    print("✅ Results are saved to predictions_output.csv!")

# region Main
if __name__ == "__main__":
    main()