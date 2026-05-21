from schema.mt500_schema import (
    MT500_SCHEMA
)

# --------------------------------------------------
# BUILD MT500 SEQUENCE
# --------------------------------------------------

def build_sequence(

    sequence_name,

    transaction,

    field_data

):

    sequence = MT500_SCHEMA[
        sequence_name
    ]

    lines = []

    # -----------------------------------------
    # START SEQUENCE
    # -----------------------------------------

    lines.append(
        sequence["start"]
    )

    # -----------------------------------------
    # BUILD FIELDS
    # -----------------------------------------

    for field in sequence["fields"]:

        if field == "20":

            lines.append(
                f":20:"
                f"{transaction['transaction_reference']}"
            )

        elif field == "23G":

            lines.append(
                ":23G:NEWM"
            )

        elif field == "98A":

            lines.append(

                f":98A::TRAD//"
                f"{transaction['trade_date'].replace('-', '')}"

            )

        elif field == "35B":

            lines.append(

                f":35B:ISIN "
                f"{transaction['isin']}"

            )

            lines.append(
                transaction["security_name"]
            )

        elif field == "90A":

            lines.append(

                f":90A::DEAL//ACTU/"
                f"{transaction['price']}"

            )

        elif field == "36B":

            lines.append(

                f":36B::SETT//UNIT/"
                f"{transaction['quantity']}"

            )

        elif field == "19A":

            lines.append(

                f":19A::SETT//"
                f"{transaction['currency']}"
                f"{transaction['amount']}"

            )

        elif field == "22F":

            qualifier = "SETR"

            if transaction.get(
                "swift_message_modifier"
            ) == "INVALID_QUALIFIER":

                qualifier = "WRNG"

            lines.append(
                f":22F::{qualifier}//TRAD"
            )

        elif field == "95P":

            lines.append(

                f":95P::BUYR//"
                f"{transaction['sender_bic']}"

            )

            lines.append(

                f":95P::SELL//"
                f"{transaction['receiver_bic']}"

            )

        elif field == "97A":

            lines.append(
                ":97A::SAFE//SAFEACCOUNT01"
            )

        elif field == "70E":

            lines.append(

                ":70E::SPRO//"
                "Synthetic MT500 Message"

            )

    # -----------------------------------------
    # END SEQUENCE
    # -----------------------------------------

    lines.append(
        sequence["end"]
    )

    return lines