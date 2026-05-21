import pandas as pd
import numpy as np


class MT500FeatureEngineering:

    def __init__(self):

        print(
            "MT500 Feature Engineering "
            "Engine Initialized"
        )

    def create_features(self, df):

        # -----------------------------------
        # Amount Features
        # -----------------------------------

        df["log_amount"] = np.log1p(df["amount"])

        df["high_amount_flag"] = (
            df["amount"] > 5000000
        ).astype(int)

        # -----------------------------------
        # Quantity Features
        # -----------------------------------

        df["high_quantity_flag"] = (
            df["quantity"] > 3000
        ).astype(int)

        # -----------------------------------
        # Compliance Features
        # -----------------------------------

        df["low_compliance_flag"] = (
            df["compliance_score"] < 70
        ).astype(int)

        # -----------------------------------
        # Cross Border Features
        # -----------------------------------

        df["cross_border_flag"] = (
            df["country"] != "US"
        ).astype(int)

        # -----------------------------------
        # Risk Features
        # -----------------------------------

        df["high_risk_flag"] = (
            df["risk_level"] == "HIGH"
        ).astype(int)

        # -----------------------------------
        # Settlement Delay
        # -----------------------------------

        df["trade_date"] = pd.to_datetime(
            df["trade_date"],
            errors="coerce",
            format="mixed"
        )

        df["settlement_date"] = pd.to_datetime(
            df["settlement_date"],
            errors="coerce",
            format="mixed"
        )

        df["settlement_delay"] = (
            df["settlement_date"]
            - df["trade_date"]
        ).dt.days

        # -----------------------------------
        # Weekend Trading
        # -----------------------------------

        df["trade_weekday"] = (
            df["trade_date"]
            .dt.weekday
        )

        df["weekend_trade_flag"] = (
            df["trade_weekday"] >= 5
        ).astype(int)

        # -----------------------------------
        # Duplicate Transaction Feature
        # -----------------------------------

        df["duplicate_reference_flag"] = (
            df
            .duplicated(
                subset=["transaction_reference"]
            )
            .astype(int)
        )

        # -----------------------------------
        # Suspicious Security Feature
        # -----------------------------------

        suspicious_keywords = [
            "OFFSHORE",
            "UNKNOWN",
            "SHELL"
        ]

        df["suspicious_security_flag"] = (
            df["security_name"]
            .str.upper()
            .apply(
                lambda x: int(
                    any(
                        keyword in x
                        for keyword
                        in suspicious_keywords
                    )
                )
            )
        )

        print(
            "Enterprise MT500 features "
            "created successfully"
        )

        return df