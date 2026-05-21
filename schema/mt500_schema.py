# --------------------------------------------------
# MT500 ENTERPRISE SEQUENCE SCHEMA
# --------------------------------------------------

MT500_SCHEMA = {

    # --------------------------------------------------
    # SEQUENCE A
    # GENERAL INFORMATION
    # --------------------------------------------------

    "A": {

        "name":
            "General Information",

        "mandatory":
            True,

        "start":
            ":16R:GENL",

        "end":
            ":16S:GENL",

        "fields": [

            "20",
            "23G",
            "98A"

        ]

    },

    # --------------------------------------------------
    # SEQUENCE B
    # TRADE DETAILS
    # --------------------------------------------------

    "B": {

        "name":
            "Trade Details",

        "mandatory":
            True,

        "start":
            ":16R:TRADDET",

        "end":
            ":16S:TRADDET",

        "fields": [

            "35B",
            "90A",
            "36B",
            "19A",
            "22F"

        ]

    },

    # --------------------------------------------------
    # SEQUENCE B1
    # FINANCIAL INSTRUMENT
    # --------------------------------------------------

    "B1": {

        "name":
            "Financial Instrument",

        "mandatory":
            False,

        "start":
            ":16R:FIAC",

        "end":
            ":16S:FIAC",

        "fields": [

            "95P",
            "97A"

        ]

    },

    # --------------------------------------------------
    # SEQUENCE C
    # NARRATIVE INFORMATION
    # --------------------------------------------------

    "C": {

        "name":
            "Narrative Information",

        "mandatory":
            False,

        "start":
            ":16R:TEXT",

        "end":
            ":16S:TEXT",

        "fields": [

            "70E"

        ]

    }

}