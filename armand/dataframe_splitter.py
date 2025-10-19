import pandas as pd
from sklearn.model_selection import train_test_split

def split_dataframe(df: pd.DataFrame, target_df: pd.DataFrame, random_state: int = 42) -> dict:
    # First split: Separate the test set from the rest
    x_train_val, x_test, y_train_val, y_test = train_test_split(
        df, target_df,
        test_size=0.2,
        random_state=random_state,
        stratify=target_df
    )

    # Second split: Separate the training and validation sets
    x_train, x_val, y_train, y_val = train_test_split(
        x_train_val, y_train_val,
        test_size=0.25, # 25% of 80 = 20
        random_state=random_state,
        stratify=y_train_val
    )

    return {
        "x": {
            "train": x_train,
            "validate": x_val,
            "test": x_test
		}, 
        "y": {
            "train": y_train,
            "validate": y_val,
            "test": y_test
		}
	}