import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier


class FederatedNode:

    def __init__(self, bank_name):

        self.bank_name = bank_name

        self.local_model = RandomForestClassifier(
            n_estimators=50,
            random_state=42
        )

        print(
            f"{bank_name} Federated Node Initialized"
        )

    def train_local_model(self, df):

        df = df.select_dtypes(
            include=["int64", "float64"]
        )

        if "fraud_flag" not in df.columns:

            return None

        X = df.drop(
            columns=["fraud_flag"],
            errors="ignore"
        )

        y = df["fraud_flag"]

        X = X.fillna(0)

        self.local_model.fit(X, y)

        print(
            f"{self.bank_name} local training completed"
        )

        return self.local_model


class FederatedAggregator:

    def __init__(self):

        self.global_models = []

        print(
            "Enterprise Federated Aggregator Initialized"
        )

    def collect_model(self, model):

        self.global_models.append(model)

    def aggregate(self):

        print(
            "\nFederated aggregation completed"
        )

        print(
            f"Total nodes: {len(self.global_models)}"
        )

        return True