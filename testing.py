import pyodbc

try:
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=SURFACELAPPY,1433;"
        "DATABASE=mydb;"
        "UID=sa;"
        "PWD=bebo@123;"
    )
    print("✅ Connected successfully to SQL Server!")
except Exception as e:
    print("❌ Connection failed:", e)
