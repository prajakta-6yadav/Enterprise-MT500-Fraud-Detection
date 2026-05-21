import random
import pandas as pd

from datetime import datetime, timedelta

from config.mt500_config import *

from generator.fraud_mt500_generator import (
    FraudMT500Generator
)

from generator.sequence_builder import (
    build_sequence
)


class MT500Generator:

    def __init__(self):

        self.fraud_generator = (
            FraudMT500Generator()
        )

    def generate_transaction(self, bank):

        receiver_bank = random.choice(
            [b for b in BANKS if b != bank]
        )

        trade_date = datetime.now() - timedelta(
            days=random.randint(1, 365)
        )

        settlement_date = trade_date + timedelta(
            days=random.randint(1, 5)
        )

        quantity = random.randint(1, 5000)

        price = round(
            random.uniform(100, 10000),
            2
        )

        amount = round(quantity * price, 2)

        risk_level = "LOW"

        fraud_flag = 0

        transaction = {

            "message_type":
                random.choice(MESSAGE_TYPES),

            "transaction_reference":
                f"TRX{random.randint(100000,999999)}",

            "sender_bic":
                bank["bic"],

            "receiver_bic":
                receiver_bank["bic"],

            "trade_date":
                trade_date.strftime("%Y-%m-%d"),

            "settlement_date":
                settlement_date.strftime("%Y-%m-%d"),

            "isin":
                f"US{random.randint(100000000,999999999)}",

            "security_type":
                random.choice(SECURITY_TYPES),

            "security_name":
                random.choice(SECURITY_NAMES),

            "quantity":
                quantity,

            "price":
                price,

            "currency":
                random.choice(CURRENCIES),

            "amount":
                amount,

            "country":
                random.choice(COUNTRIES),

            "swift_priority":
                random.choice(VALID_PRIORITIES),

            "delivery_monitoring":
                DEFAULT_DELIVERY_MONITORING,

            "obsolescence_period":
                DEFAULT_OBSOLESCENCE_PERIOD,

            "compliance_score":
                random.randint(50, 100),

            "risk_level":
                risk_level,

            "fraud_flag":
                fraud_flag
        }

        # ---------------------------------
        # Apply Fraud
        # ---------------------------------

        if random.random() < FRAUD_PERCENTAGE:

            transaction = (
                self.fraud_generator
                .apply_fraud(transaction)
            )

        # ---------------------------------
        # ADVANCED FRAUD SCENARIOS
        # ---------------------------------

        if transaction["fraud_flag"] == 1:

            if transaction["fraud_type"] == "invalid_qualifier":

                transaction[
                    "swift_message_modifier"
                ] = "INVALID_QUALIFIER"

            elif transaction["fraud_type"] == "missing_sequence":

                transaction[
                    "swift_message_modifier"
                ] = "REMOVE_TRADDET"

            elif transaction["fraud_type"] == "invalid_currency":

                transaction[
                    "currency"
                ] = "US"

            elif transaction["fraud_type"] == "invalid_date":

                transaction[
                    "trade_date"
                ] = "20-05-2026"

            transaction["amount"] *= random.uniform(1.8, 3.5)

            transaction["swift_priority"] = "U"

            transaction["country"] = random.choice(
                HIGH_RISK_COUNTRIES
            )

            transaction["risk_level"] = random.choice(
                ["MEDIUM", "HIGH"]
            )

            transaction["price"] *= random.uniform(1.5, 2.5)

        return transaction
    
    def compose_mt500_message(self, transaction):

        message = []

    # --------------------------------------------------
    # SWIFT HEADER
    # --------------------------------------------------

        message.append(
            f"{{1:F01{transaction['sender_bic']}0000000000}}"
        )

        message.append(
            f"{{2:I500{transaction['receiver_bic']}N}}"
        )

        message.append("{4:")

    # --------------------------------------------------
    # DYNAMIC SEQUENCE BUILDING
    # --------------------------------------------------

        sequences = [

            "A",
            "B",
            "B1",
            "C"

        ]

        for sequence_name in sequences:

            sequence_lines = build_sequence(

                sequence_name,

                transaction,

                {}

            )

            message.extend(
                sequence_lines
            )

    # --------------------------------------------------
    # END BLOCK
    # --------------------------------------------------

        message.append("-}")

        return "\n".join(message)

    def generate_dataset(self):

        for bank in BANKS:

            transactions = []

            for _ in range(ROWS_PER_BANK):

                transaction = (
                    self.generate_transaction(bank)
                )

                transactions.append(transaction)

            df = pd.DataFrame(transactions)

            messages = []

            for transaction in transactions:

                swift_message = (
                    self.compose_mt500_message(
                        transaction
                    )
                )

                messages.append(swift_message)

            df["swift_message"] = messages

            file_path = (
                f"Data/raw/"
                f"mt500_{bank['bic']}.csv"
            )

            df.to_csv(file_path, index=False)

            print(
                f"{file_path} generated successfully"
            )


if __name__ == "__main__":

    generator = MT500Generator()

    generator.generate_dataset()

    print(
        "\nEnterprise MT500 datasets "
        "generated successfully."
    )