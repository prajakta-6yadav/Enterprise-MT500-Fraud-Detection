OUTPUT_DIR = "Data/raw"

ROWS_PER_BANK = 20000

FRAUD_PERCENTAGE = 0.03


VALID_PRIORITIES = [
    "N",
    "U",
    "S"
]

DEFAULT_DELIVERY_MONITORING = "3"

DEFAULT_OBSOLESCENCE_PERIOD = "003"


BANKS = [

    {
        "name": "Alpha Bank",
        "bic": "ALPHUS33AXXX",
        "country": "US"
    },

    {
        "name": "Beta Bank",
        "bic": "BETAGB2LXXXX",
        "country": "GB"
    },

    {
        "name": "Gamma Bank",
        "bic": "GAMMDEFFAXXX",
        "country": "DE"
    },

    {
        "name": "Mu Bank",
        "bic": "MUBKAEADXXXX",
        "country": "AE"
    },

    {
        "name": "Sigma Bank",
        "bic": "SIGMFRPPAXXX",
        "country": "FR"
    }
]


CURRENCIES = [
    "USD",
    "EUR",
    "GBP",
    "CHF",
    "JPY",
    "SGD"
]


SECURITY_TYPES = [
    "BOND",
    "EQUITY",
    "TREASURY",
    "ETF"
]


SECURITY_NAMES = [
    "US TREASURY BOND",
    "GERMAN GOV BOND",
    "JAPAN TREASURY BILL",
    "GLOBAL EQUITY ETF",
    "CORPORATE CREDIT BOND"
]


COUNTRIES = [
    "US",
    "GB",
    "DE",
    "FR",
    "AE",
    "SG",
    "JP"
]


HIGH_RISK_COUNTRIES = [
    "IR",
    "KP",
    "SY"
]


FRAUD_TYPES = [

    "near_duplicate_trade",

    "amount_structuring",

    "slightly_modified_bic",

    "settlement_delay",

    "cross_border_spike",

    "high_frequency_small_trades",

    "security_price_mismatch",

    "unusual_security_mix",

    "priority_abuse",

    "suspicious_counterparty",
    
    "invalid_qualifier",

    "missing_sequence",

    "invalid_currency",

    "invalid_date"
]

MESSAGE_TYPES = [
    "MT500"
]

SANCTIONED_BICS = [
    "SANCBK00AXXX",
    "BADBIC00XXXX"
]


INVALID_ISINS = [
    "INVALID123456",
    "FAKEISIN0001"
]


DUPLICATE_REFERENCE = "TRX99999999"


MODEL_RANDOM_STATE = 42

TEST_SIZE = 0.20

RANDOM_FOREST_ESTIMATORS = 200