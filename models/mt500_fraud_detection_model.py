import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    accuracy_score,
    confusion_matrix
)
from sklearn.preprocessing import LabelEncoder


class MT500FraudDetectionModel:

    def __init__(self):

        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            class_weight="balanced"
        )

        self.label_encoders = {}

        self.feature_columns = []

        print(
            "MT500 Fraud Detection Model Initialized"
        )

    # -----------------------------------
    # Preprocessing
    # -----------------------------------

    def preprocess_data(self, df):

        categorical_columns = [

            "sender_bic",
            "receiver_bic",
            "currency",
            "country",
            "security_type",
            "security_name",
            "isin",
            "message_type"

        ]

        for column in categorical_columns:

            if column in df.columns:

                encoder = LabelEncoder()

                df[column] = encoder.fit_transform(
                    df[column].astype(str)
                )

                self.label_encoders[column] = encoder

        return df

    # -----------------------------------
    # Training
    # -----------------------------------

    def train(self, dataset_path):

        df = pd.read_csv(dataset_path)

        df = self.preprocess_data(df)

        X = df.drop(
            columns=[
                "fraud_flag",
                "fraud_type",
                "transaction_reference",
                "trade_date",
                "settlement_date",
                "swift_message",
                "risk_level",
                "swift_priority"
            ],
            errors="ignore"
        )

        # keep only numeric columns
        X = X.select_dtypes(
            include=["int64", "float64"]
        )

        y = df["fraud_flag"]

        X = X.fillna(0)

        # save feature names
        self.feature_columns = X.columns.tolist()

        X_train, X_test, y_train, y_test = train_test_split(

            X,
            y,

            test_size=0.2,

            random_state=42,

            stratify=y
        )

        self.model.fit(
            X_train,
            y_train
        )

        predictions = self.model.predict(
            X_test
        )

        fraud_probabilities = (
            self.model.predict_proba(X_test)
        )

        risk_scores = (
            fraud_probabilities[:, 1] * 100
        )

        print("\nSample Risk Scores:")
        print(risk_scores[:10])

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        print("\nModel Accuracy:")
        print(accuracy)

        print("\nClassification Report:\n")

        print(
            classification_report(
                y_test,
                predictions
            )
        )

        print("\nConfusion Matrix:\n")

        print(
            confusion_matrix(
                y_test,
                predictions
            )
        )

        joblib.dump(
            {
                "model": self.model,
                "feature_columns": self.feature_columns
            },
            "artifacts/mt500_model.pkl"
        )

        print(
            "\nModel saved successfully in artifacts folder."
        )

        return self.model

    # -----------------------------------
    # Load Model
    # -----------------------------------

    def load_model(self):

        saved_objects = joblib.load(
            "artifacts/mt500_model.pkl"
        )

        self.model = saved_objects["model"]

        self.feature_columns = (
            saved_objects["feature_columns"]
        )

        print(
            "\nSaved MT500 model loaded successfully."
        )

        return self.model

    # -----------------------------------
    # Prediction
    # -----------------------------------

    def predict_transaction(self, transaction_features):

        transaction_features = transaction_features.drop(
            columns=[
                "fraud_flag",
                "fraud_type",
                "transaction_reference",
                "trade_date",
                "settlement_date",
                "swift_message",
                "risk_level",
                "swift_priority"
            ],
            errors="ignore"
        )

        transaction_features = self.preprocess_data(
            transaction_features
        )

        # keep only training columns
        transaction_features = (
            transaction_features[
                self.feature_columns
            ]
        )

        transaction_features = (
            transaction_features.fillna(0)
        )

        prediction = self.model.predict(
            transaction_features
        )

        probability = (
            self.model.predict_proba(
                transaction_features
            )
        )

        risk_score = (
            probability[:, 1] * 100
        )

        fraud_reasons = []

        transaction = transaction_features.iloc[0]

        if "transaction_amount" in transaction.index:

            if transaction["transaction_amount"] > 900000:

                fraud_reasons.append(
                    "High transaction amount"
                )

        if "country" in transaction.index:

            if transaction["country"] in [1, 2, 3]:

                fraud_reasons.append(
                    "High risk country"
                )

        if "swift_priority" in transaction.index:

            if transaction["swift_priority"] == 1:

                fraud_reasons.append(
                    "High priority SWIFT message"
                )

        if risk_score[0] > 80:

            fraud_reasons.append(
                "Very high fraud probability"
            )

        if len(fraud_reasons) == 0:

            fraud_reasons.append(
                "No major fraud indicators"
            )


        print("\nPrediction:", prediction[0])

        print("Risk Score:", risk_score[0])

        if risk_score[0] >= 80:

            alert = "HIGH RISK FRAUD ALERT"

        elif risk_score[0] >= 50:

            alert = "MEDIUM RISK"

        else:

            alert = "LOW RISK"

        print(
            "Alert Level:",
            alert
        )

        print(
            "Fraud Reasons:",
            fraud_reasons
        )

        return {

            "prediction": int(prediction[0]),

            "risk_score": float(risk_score[0]),

            "alert_level": alert,

            "fraud_reasons": fraud_reasons
        }