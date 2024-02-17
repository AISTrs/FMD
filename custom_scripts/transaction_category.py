import os

import pandas as pd
import psycopg2

from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.environ.get('DB_NAME'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    host=os.environ.get('DB_HOST'),
    port=os.environ.get('DB_PORT')
)

cur = conn.cursor()

excel_file_path = '/Users/uk/Downloads/AIS Ledger Workbook.xlsx'

xls = pd.ExcelFile(excel_file_path)

sheet_names = xls.sheet_names

budget = set('Leadership')
purpose = set()

for sheet_name in sheet_names:
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

    try:
        for index, row in df.iterrows():
            budget.add(row['Budget'])
            purpose.add(row['Purpose'])
    except:
        pass

budget_list = list(budget)
purpose_list = list(purpose)

for b in budget_list:
    cur.execute("INSERT INTO transaction_category (category, value) VALUES ('Budget', %s) ON CONFLICT DO NOTHING", (b,))

# Insert distinct purpose values into transaction_category table
for p in purpose_list:
    cur.execute("INSERT INTO transaction_category (category, value) VALUES ('Purpose', %s) ON CONFLICT DO NOTHING",
                (p,))

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
