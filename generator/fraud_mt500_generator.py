import random

from config.mt500_config import (
    FRAUD_TYPES,
    SANCTIONED_BICS,
    INVALID_ISINS,
    HIGH_RISK_COUNTRIES,
    DUPLICATE_REFERENCE
)


class FraudMT500Generator:

    def __init__(self):

        self.fraud_types = FRAUD_TYPES

    def apply_fraud(self, transaction):

        fraud_type = random.choice(self.fraud_types)

        transaction["fraud_type"] = fraud_type

        # -----------------------------------
        # Spoofed Sender BIC
        # -----------------------------------

        if fraud_type == "spoofed_sender_bic":

            transaction["sender_bic"] = "FAKEBICXXXX"

        # -----------------------------------
        # Large Security Amount
        # -----------------------------------

        elif fraud_type == "large_security_amount":

            transaction["amount"] *= 50

            transaction["risk_level"] = "HIGH"

        # -----------------------------------
        # Cross Border Layering
        # -----------------------------------

        elif fraud_type == "cross_border_layering":

            transaction["country"] = random.choice(
                HIGH_RISK_COUNTRIES
            )

            transaction["risk_level"] = "HIGH"

        # -----------------------------------
        # Invalid ISIN
        # -----------------------------------

        elif fraud_type == "invalid_isin":

            transaction["isin"] = random.choice(
                INVALID_ISINS
            )

        # -----------------------------------
        # Duplicate Transaction Reference
        # -----------------------------------

        elif fraud_type == "duplicate_transaction_reference":

            transaction["transaction_reference"] = (
                DUPLICATE_REFERENCE
            )

        # -----------------------------------
        # High Frequency Trading Pattern
        # -----------------------------------

        elif fraud_type == "high_frequency_trading_pattern":

            transaction["quantity"] *= 100

            transaction["risk_level"] = "HIGH"

        # -----------------------------------
        # Suspicious Security
        # -----------------------------------

        elif fraud_type == "suspicious_security":

            transaction["security_name"] = (
                "UNKNOWN OFFSHORE FUND"
            )

            transaction["risk_level"] = "HIGH"

        # -----------------------------------
        # Rapid Settlement Pattern
        # -----------------------------------

        elif fraud_type == "rapid_settlement_pattern":

            transaction["settlement_priority"] = "URGENT"

        # -----------------------------------
        # Sanctioned Receiver
        # -----------------------------------

        elif fraud_type == "sanctioned_receiver":

            transaction["receiver_bic"] = random.choice(
                SANCTIONED_BICS
            )

            transaction["risk_level"] = "HIGH"

        # -----------------------------------
        # Weekend Trade Activity
        # -----------------------------------

        elif fraud_type == "weekend_trade_activity":

            transaction["trade_day"] = "SUNDAY"

                # -----------------------------------
        # Invalid Qualifier Fraud
        # -----------------------------------

        elif fraud_type == "invalid_qualifier":

            transaction[
                "invalid_qualifier"
            ] = "XXXX"

            transaction[
                "risk_level"
            ] = "HIGH"

        # -----------------------------------
        # Missing Mandatory Sequence
        # -----------------------------------

        elif fraud_type == "missing_sequence":

            transaction[
                "missing_sequence"
            ] = "TRADDET"

            transaction[
                "risk_level"
            ] = "HIGH"

        # -----------------------------------
        # Invalid Currency Format
        # -----------------------------------

        elif fraud_type == "invalid_currency":

            transaction[
                "currency"
            ] = "US"

            transaction[
                "risk_level"
            ] = "HIGH"

        # -----------------------------------
        # Invalid Date Format
        # -----------------------------------

        elif fraud_type == "invalid_date":

            transaction[
                "trade_date"
            ] = "20-05-2026"

            transaction[
                "risk_level"
            ] = "HIGH"     

        transaction["fraud_flag"] = 1

        return transaction