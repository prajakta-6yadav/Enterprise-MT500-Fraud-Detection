import os
import pandas as pd

from generator.mt500_generator import (
    MT500Generator
)

from parser.mt500_feature_engineering import (
    MT500FeatureEngineering
)

from models.mt500_fraud_detection_model import (
    MT500FraudDetectionModel
)

from validator.mt500_validator import (
    MT500Validator
)

from rules_engine import (
    RulesEngine
)

from models.federated_model import (
    FederatedNode,
    FederatedAggregator
)

from alerts.realtime_alerts import (
    RealtimeAlertEngine
)

from email_alert import (
    EnterpriseEmailAlert
)

from models.deep_learning_model import (
    MT500DeepLearningModel
)

# -----------------------------------
# Generate Enterprise Datasets
# -----------------------------------

generator = MT500Generator()

generator.generate_dataset()

print(
    "\nEnterprise MT500 datasets generated successfully."
)

# -----------------------------------
# Feature Engineering
# -----------------------------------

feature_engineering = (
    MT500FeatureEngineering()
)

raw_path = "Data/raw"

processed_path = "Data/processed"

os.makedirs(
    processed_path,
    exist_ok=True
)

for file_name in os.listdir(raw_path):

    if file_name.endswith(".csv"):

        file_path = (
            f"{raw_path}/{file_name}"
        )

        df = pd.read_csv(file_path)

        # -----------------------------------
        # VALIDATION ENGINE
        # -----------------------------------

        validation_results = []

        validator = MT500Validator()

        for _, row in df.iterrows():

            transaction = row.to_dict()

            validation_result = (
                validator.validate_mt500(
                    transaction
                )
            )

            errors = validation_result["errors"]

            validation_results.append(
                " | ".join(errors)
            )

        df["validation_errors"] = (
            validation_results
        )

        df["is_valid_mt500"] = (
            df["validation_errors"] == ""
        )

        processed_df = (
            feature_engineering
            .create_features(df)
        )

        processed_file_path = (
            f"{processed_path}/processed_{file_name}"
        )

        processed_df.to_csv(
            processed_file_path,
            index=False
        )

        print(
            f"{processed_file_path} saved successfully"
        )

print(
    "\nEnterprise MT500 feature engineering completed."
)

# -----------------------------------
# Model Training
# -----------------------------------

model = MT500FraudDetectionModel()

training_dataset = (
    "Data/processed/"
    "processed_mt500_ALPHUS33AXXX.csv"
)

model.train(
    training_dataset
)

print(
    "\nEnterprise MT500 fraud detection training completed."
)

# -----------------------------------
# Load Saved Model
# -----------------------------------

model.load_model()
rules_engine = RulesEngine()

deep_learning_engine = (
    MT500DeepLearningModel()
)

# -----------------------------------
# Single Transaction Inference
# -----------------------------------

sample_transaction = pd.read_csv(
    training_dataset
)

sample_transaction = (
    sample_transaction.iloc[[0]]
)

result = (
    model.predict_transaction(
        sample_transaction
    )
)

print("\nInference Result:")

print(result)

rules_result = (
    rules_engine.evaluate_transaction(
        sample_transaction
    )
)

print("\nRules Engine Result:")

print(rules_result)

# --------------------------------
# Deep Learning Detection
# --------------------------------

deep_learning_result = (
    deep_learning_engine
    .detect_anomalies(
        processed_file_path
    )
)

print(
    "\nDeep Learning Result:"
)

print(
    deep_learning_result[:5]
)

# -----------------------------------
# Realtime Fraud Alert Engine
# -----------------------------------

alert_engine = (
    RealtimeAlertEngine()
)

alert = (
    alert_engine.generate_alert(
        sample_transaction.iloc[0],
        result,
        rules_result
    )
)

print("\nFinal Alert:")

print(alert)

# -----------------------------------
# Enterprise Email Alert
# -----------------------------------

email_engine = EnterpriseEmailAlert(

    sender_email="prajaktay525@gmail.com",

    sender_password="evqn rjei vaqu butd",

    receiver_email="prajaktay525@gmail.com"

)

email_engine.send_fraud_alert(
    alert
)

# -----------------------------------
# Federated Learning Simulation
# -----------------------------------

aggregator = FederatedAggregator()

for file_name in os.listdir(processed_path):

    if file_name.endswith(".csv"):

        file_path = (
            f"{processed_path}/{file_name}"
        )

        federated_df = pd.read_csv(
            file_path
        )

        bank_name = (
            file_name.replace(
                "processed_",
                ""
            ).replace(
                ".csv",
                ""
            )
        )

        node = FederatedNode(
            bank_name
        )

        local_model = (
            node.train_local_model(
                federated_df
            )
        )

        if local_model is not None:

            aggregator.collect_model(
                local_model
            )

aggregator.aggregate()