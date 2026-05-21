from datetime import datetime


class RealtimeAlertEngine:

    def __init__(self):

        print(
            "Enterprise Realtime Alert Engine Initialized"
        )

    def generate_alert(
        self,
        transaction,
        ml_result,
        rules_result
    ):

        final_risk = max(

            ml_result.get(
                "risk_score",
                0
            ),

            rules_result.get(
                "risk_score",
                0
            )
        )

        if final_risk >= 80:

            severity = "CRITICAL"

        elif final_risk >= 50:

            severity = "HIGH"

        elif final_risk >= 30:

            severity = "MEDIUM"

        else:

            severity = "LOW"

        alert = {

            "timestamp": str(
                datetime.now()
            ),

            "transaction_reference":
            transaction.get(
                "transaction_reference",
                "UNKNOWN"
            ),

            "sender":
            transaction.get(
                "sender_bic",
                "UNKNOWN"
            ),

            "receiver":
            transaction.get(
                "receiver_bic",
                "UNKNOWN"
            ),

            "amount":
            transaction.get(
                "transaction_amount",
                0
            ),

            "severity":
            severity,

            "risk_score":
            final_risk,

            "status":
            "ACTIVE"
        }

        print("\nRealtime Alert Generated")

        print(alert)

        return alert