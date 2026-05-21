# --------------------------------------------------
# MT500 FIELD DEFINITIONS
# --------------------------------------------------

MT500_FIELDS = {

    # --------------------------------------------------
    # GENERAL INFORMATION SEQUENCE
    # --------------------------------------------------

    "20": {

        "name":
            "Transaction Reference Number",

        "mandatory":
            True,

        "format":
            "16x",

        "sequence":
            "GENL",

        "validators":
            ["reference"]

    },

    "23G": {

        "name":
            "Function of the Message",

        "mandatory":
            True,

        "format":
            "4!c",

        "allowed_values":
            [

                "NEWM",
                "CANC",
                "REPL"

            ],

        "sequence":
            "GENL"

    },

    "98A": {

        "name":
            "Date/Time",

        "mandatory":
            True,

        "format":
            "8!n",

        "qualifiers":
            [

                "TRAD",
                "SETT",
                "ESET",
                "VALU"

            ],

        "validators":
            ["date"],

        "sequence":
            "GENL"

    },

    # --------------------------------------------------
    # TRADE DETAILS SEQUENCE
    # --------------------------------------------------

    "35B": {

        "name":
            "Financial Instrument",

        "mandatory":
            True,

        "format":
            "ISIN1!e12!c",

        "validators":
            ["isin"],

        "sequence":
            "TRADDET"

    },

    "90A": {

        "name":
            "Price",

        "mandatory":
            True,

        "format":
            "4!c//4!c/15d",

        "qualifiers":
            [

                "DEAL",
                "MRKT"

            ],

        "validators":
            ["price"],

        "sequence":
            "TRADDET"

    },

    "36B": {

        "name":
            "Quantity of Financial Instrument",

        "mandatory":
            True,

        "format":
            "4!c//4!c/15d",

        "qualifiers":
            [

                "SETT",
                "PSTA"

            ],

        "validators":
            ["quantity"],

        "sequence":
            "TRADDET"

    },

    "19A": {

        "name":
            "Amount",

        "mandatory":
            True,

        "format":
            "4!c//3!a15d",

        "qualifiers":
            [

                "SETT",
                "RESU"

            ],

        "validators":
            [

                "currency",
                "amount"

            ],

        "sequence":
            "TRADDET"

    },

    "22F": {

        "name":
            "Indicator",

        "mandatory":
            False,

        "format":
            "4!c//4!c",

        "qualifiers":
            [

                "SETR",
                "STCO"

            ],

        "sequence":
            "TRADDET"

    },

    # --------------------------------------------------
    # FINANCIAL INSTITUTION ACCOUNT SEQUENCE
    # --------------------------------------------------

    "95P": {

        "name":
            "Party",

        "mandatory":
            False,

        "format":
            "4!c//4!a2!a2!c[3!c]",

        "qualifiers":
            [

                "BUYR",
                "SELL",
                "ACOW",
                "PSET"

            ],

        "validators":
            ["bic"],

        "sequence":
            "FIAC"

    },

    "97A": {

        "name":
            "Account",

        "mandatory":
            False,

        "format":
            "4!c//35x",

        "qualifiers":
            [

                "SAFE",
                "CASH"

            ],

        "sequence":
            "FIAC"

    },

    # --------------------------------------------------
    # NARRATIVE SEQUENCE
    # --------------------------------------------------

    "70E": {

        "name":
            "Narrative",

        "mandatory":
            False,

        "format":
            "4!c//10*35x",

        "qualifiers":
            [

                "SPRO",
                "PACO"

            ],

        "sequence":
            "TEXT"

    }

}

# --------------------------------------------------
# MT500 SEQUENCES
# --------------------------------------------------

MT500_SEQUENCES = {

    "GENL": [

        "20",
        "23G",
        "98A"

    ],

    "TRADDET": [

        "35B",
        "90A",
        "36B",
        "19A",
        "22F"

    ],

    "FIAC": [

        "95P",
        "97A"

    ],

    "TEXT": [

        "70E"

    ]

}

# --------------------------------------------------
# FRAUD SENSITIVE FIELDS
# --------------------------------------------------

FRAUD_SENSITIVE_FIELDS = [

    "95P",
    "19A",
    "98A",
    "22F",
    "35B",
    "97A"

]