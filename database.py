import sqlite3

# -----------------------------------
# Create Database Connection
# -----------------------------------

connection = sqlite3.connect(
    "fraud_cases.db",
    check_same_thread=False
)

cursor = connection.cursor()

# -----------------------------------
# Create Fraud Cases Table
# -----------------------------------

cursor.execute(

    """
    CREATE TABLE IF NOT EXISTS fraud_cases (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        transaction_reference TEXT,

        fraud_type TEXT,

        risk_level TEXT,

        analyst_notes TEXT,

        case_status TEXT
    )
    """
)

connection.commit()

print(
    "Fraud case database initialized."
)