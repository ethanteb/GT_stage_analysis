#-------------------------------------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------------------------------------

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix)
import pandas as pd
import numpy as np
from ..data.data_loading import GRAND_TOURS

#-------------------------------------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------------------------------------

GRAND_TOURS_MAP = {"GIRO": 0, "TOUR": 1, "VUELTA": 2}
NUMERIC_COLUMNS = [
    "stage_number",
    "distance_km",
    "gradient_final_km",
    "vertical_metres",
    "profile_score",
    "race_ranking",
    "avg_temperature_c"
    ]
FEATURE_NAMES = NUMERIC_COLUMNS + ["race"]

#-------------------------------------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------------------------------------



#-------------------------------------------------------------------------------------------------------------
# Random Forest modelling class
#-------------------------------------------------------------------------------------------------------------

class RandomForest:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.X_train: pd.DataFrame | None = None
        self.X_test: pd.DataFrame | None = None
        self.y_train: pd.Series | None = None
        self.y_test: pd.Series | None = None
        self.y_pred: pd.Series | None = None
        self.model: RandomForestClassifier | None = None
        self.conf_matrix:  np.ndarray | None = None
        self.feature_importances: np.ndarray | None = None

    def train_test_split(self, test_size :float = 0.2, random_state :int = 42):
        X = self.data[FEATURE_NAMES].copy()
        y = self.data['break_success']

        X[NUMERIC_COLUMNS] = X[NUMERIC_COLUMNS].apply(pd.to_numeric, errors="coerce")
        X[NUMERIC_COLUMNS] = X[NUMERIC_COLUMNS].fillna(X[NUMERIC_COLUMNS].median())

        X['race'] = X['race'].map(GRAND_TOURS_MAP)
        if X["race"].isna().any():
            raise ValueError("Unknown race value found")

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)

    def _check_data_split(self):
        if any(x is None for x in (self.X_train, self.X_test, self.y_train, self.y_test)):
            raise ValueError("Data has not be split into training and testing sets properly")
        
    def _check_model_trained(self):
        if self.model is None:
            raise ValueError("Model has not been trained, call .train_model()")
        if not isinstance(self.model, RandomForestClassifier):
            raise TypeError("Model is of wrong type")

    def train_model(self, n_estimators: int = 100, random_state: int = 42):
        self._check_data_split
        self.model = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
        self.model.fit(self.X_train, self.y_train)

    def predict(self):
        self._check_data_split
        self._check_model_trained
        self.y_pred = self.model.predict(self.X_test)

    def eval(self):
        self._check_data_split
        self._check_model_trained
        if self.y_pred is None:
            raise ValueError("Run .predict() before evaulation")
        
        accuracy = accuracy_score(self.y_test, self.y_pred)
        print(f'Accuracy score: {accuracy * 100:.2f}%')

        self.conf_matrix = confusion_matrix(self.y_test, self.y_pred)
        self.feature_importances = self.model.feature_importances_
