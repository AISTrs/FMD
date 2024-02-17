import uuid

from dotenv import load_dotenv
from utils.utilitymethods import *

load_dotenv()

conn = get_connection()
cur = conn.cursor()
excel_file_path = '/Users/uk/Downloads/AIS Ledger Workbook.xlsx'
sheet_name = 'Venmo Ledger'
fiscal_id = get_fiscal_id(cur, semester="Spring 24")

batch_id = get_max_batch_number(cur, "venmo_ledger") + 1
validate_batch_number(cur, "venmo_ledger", batch_id)

print("Batch ID :", batch_id)
print("Fiscal ID : ", fiscal_id)

transaction_category_df = get_transaction_category(cur)

df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

print(f"Processing sheet: {sheet_name}")

columns = df.columns.tolist()

columns.remove("ID")

for index, row in df.iterrows():
    query_condition = f"category == 'Purpose'"
    if not pd.isna(row['Purpose']):
        query_condition += f" and value == '{row['Purpose']}'"

    purpose_id = int(transaction_category_df.query(query_condition)['id'].values[0])

    query_condition = f"category == 'Budget'"
    if not pd.isna(row['Budget']):
        query_condition += f" and value == '{row['Budget']}'"

    budget_id = int(transaction_category_df.query(query_condition)['id'].values[0])

    uid = str(uuid.uuid4())
    transaction_type = 'credit' if row['Amount (total)'] >= 0 else 'debit'
    fees = 0 if pd.isna(row['Amount (fee)']) else row['Amount (fee)']
    amount = abs(row['Amount (total)']) - fees

    query = """
        INSERT INTO venmo_ledger (Date, Type, Status, Note, From_user, To_user, total_amount, tip_amount, tax_amount, fee_amount, net_amount, tax_rate, tax_exempt, funding_source, funding_destination, budget_id, purpose_id, opening_balance, closing_balance,transaction_type, fiscal_id, transaction_id, batch_id )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    values = (
        row['Date'], row['Type'], row['Status'], row['Note'], row['From'], row['To'],
        abs(row['Amount (total)']), row['Amount (tip)'], row['Amount (tax)'], row['Amount (fee)'],
        amount, row['Tax Rate'], bool(row['Tax Exempt']), row['Funding Source'], row['Destination'],
        budget_id, purpose_id, row['Beginning Balance'], row['Ending Balance'], transaction_type,
        fiscal_id, uid, batch_id
    )
    cur.execute(query, values)

print(f"Processing sheet: {sheet_name} complete!")

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
