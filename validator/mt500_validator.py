import re


class MT500Validator:

    def __init__(self):

        print(
            "Enterprise MT500 Validator Initialized"
        )

    # ------------------------------------------------
    # MAIN VALIDATION ENGINE
    # ------------------------------------------------

    def validate_mt500(self, transaction):

        errors = []

        # --------------------------------------------
        # BIC VALIDATION
        # --------------------------------------------

        bic_pattern = r"^[A-Z0-9]{8}([A-Z0-9]{3})?$"

        sender_bic = transaction.get(
            "sender_bic",
            ""
        )

        receiver_bic = transaction.get(
            "receiver_bic",
            ""
        )

        if not re.match(
            bic_pattern,
            sender_bic
        ):

            errors.append(
                "Invalid Sender BIC"
            )

        if not re.match(
            bic_pattern,
            receiver_bic
        ):

            errors.append(
                "Invalid Receiver BIC"
            )

        # --------------------------------------------
        # ISIN VALIDATION
        # --------------------------------------------

        isin = transaction.get(
            "isin",
            ""
        )

        isin_pattern = r"^[A-Z]{2}[A-Z0-9]{10}$"

        if not re.match(
            isin_pattern,
            isin
        ):

            errors.append(
                "Invalid ISIN"
            )

        # --------------------------------------------
        # CURRENCY VALIDATION
        # --------------------------------------------

        valid_currencies = [

            "USD",
            "EUR",
            "GBP",
            "JPY",
            "INR"

        ]

        if transaction.get(
            "currency"
        ) not in valid_currencies:

            errors.append(
                "Invalid Currency"
            )

        # --------------------------------------------
        # AMOUNT VALIDATION
        # --------------------------------------------

        amount = transaction.get(
            "amount",
            0
        )

        if amount <= 0:

            errors.append(
                "Invalid Amount"
            )

        if amount > 5000000:

            errors.append(
                "Suspicious High Amount"
            )

        # --------------------------------------------
        # TRADE DATE VALIDATION
        # --------------------------------------------

        trade_date = transaction.get(
            "trade_date",
            ""
        )

        date_pattern = r"^\d{4}-\d{2}-\d{2}$"

        if not re.match(
            date_pattern,
            trade_date
        ):

            errors.append(
                "Invalid Trade Date"
            )

        # --------------------------------------------
        # MESSAGE TYPE VALIDATION
        # --------------------------------------------

        if transaction.get(
            "message_type"
        ) != "MT500":

            errors.append(
                "Invalid Message Type"
            )

        # --------------------------------------------
        # FRAUD DECISION
        # --------------------------------------------

        if len(errors) == 0:

            return {

                "is_valid": True,

                "errors": []
            }

        return {

            "is_valid": False,

            "errors": errors
        }