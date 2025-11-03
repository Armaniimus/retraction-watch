import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from typing import Tuple
from sklearn.feature_selection import SelectKBest, chi2

@dataclass
class DataSplitsBase:
    """Bevat de train, validate, en test sets."""
    train: pd.DataFrame | pd.Series
    val: pd.DataFrame | pd.Series
    test: pd.DataFrame | pd.Series

@dataclass
class X_split(DataSplitsBase):
    pass

@dataclass
class y_split(DataSplitsBase):
    pass 


def split_dataframe(df: pd.DataFrame, target_df: pd.DataFrame, random_state: int = 42) -> Tuple[X_split, y_split]:
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

	# 3. Maak de objecten aan
	x = X_split(train=x_train, test=x_test, val=x_val)
	y = y_split(train=y_train, test=y_test, val=y_val)

	# 4. Retourneer het hoofd-object
	return x, y

def select_features(split_x, split_y, k_best_features = 195):
	selector = SelectKBest(chi2, k=k_best_features)
	selector.set_output(transform="pandas")

	x_train = selector.fit_transform(split_x.train, split_y.train)
	selected_features = selector.get_feature_names_out()
	x_test = split_x.test[selected_features]
	x_val = split_x.val[selected_features]
		
	x_out = X_split(train=x_train, test=x_test, val=x_val)
	return x_out
    