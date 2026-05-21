import pandas as pd

HIGH_RISK_COUNTRIES = [

    "IR",
    "KP",
    "SY",
    "AF"

]

HIGH_RISK_CURRENCIES = [

    "XAU",
    "XAG"

]


class RulesEngine:

    def __init__(self):

        print(
            "Enterprise Rules Engine Initialized"
        )

    def evaluate_transaction(
        self,
        transaction
    ):

        risk_score = 0

        fraud_reasons = []

        # -----------------------------------
        # High Amount
        # -----------------------------------

        amount = transaction.get(
            "transaction_amount",
            0
        )

        if amount > 900000:

            risk_score += 35

            fraud_reasons.append(
                "High transaction amount"
            )

        # -----------------------------------
        # High Risk Country
        # -----------------------------------

        country = str(
            transaction.get(
                "country",
                ""
            )
        )        

        if country in HIGH_RISK_COUNTRIES:

            risk_score += 25

            fraud_reasons.append(
                "High risk country"
            )

        # -----------------------------------
        # High Risk Currency
        # -----------------------------------

        currency = str(
            transaction.get(
                "currency",
                ""
            )
        )

        if currency in HIGH_RISK_CURRENCIES:

            risk_score += 20

            fraud_reasons.append(
                "High risk currency"
            )

        # -----------------------------------
        # Weekend Trading
        # -----------------------------------

        weekday = int(
            transaction.get(
                "trade_weekday",
                pd.Series([0])
            ).iloc[0]
        )

        if weekday in [5, 6]:

            risk_score += 10

            fraud_reasons.append(
                "Weekend trading activity"
            )

        # -----------------------------------
        # SWIFT Priority
        # -----------------------------------

        priority = str(
            transaction.get(
                "swift_priority",
                ""
            )
        )

        if priority == "U":

            risk_score += 15

            fraud_reasons.append(
                "Urgent SWIFT message"
            )

        # -----------------------------------
        # Final Alert
        # -----------------------------------

        if risk_score >= 70:

            alert = "HIGH RISK"

        elif risk_score >= 40:

            alert = "MEDIUM RISK"

        else:

            alert = "LOW RISK"

        return {

            "risk_score": risk_score,

            "alert_level": alert,

            "fraud_reasons": fraud_reasons
        }