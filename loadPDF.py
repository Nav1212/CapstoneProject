import PyPDF2
import pyodbc
import os
import re
import array as arr
import hashlib



# Get a list of PDF files from the "PDFHOLDER" folder
pdf_folder = "PDFHOLDER"
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]

# Azure SQL Database connection information
server = "queens-ece-capstone-server.database.windows.net"
database = "demo"
username = "netid_18ns27"
password = "catcatcat123!"
driver = "{ODBC Driver 17 for SQL Server}"

# Connect to the Azure SQL Database
connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()
count=0

for pdf_filename in pdf_files:
    # Extract the PatientKey from the file name
    patient_key = int(re.search(r'(\d+)', pdf_filename).group(0))

    # Read the PDF file and convert it into a binary format (BLOB)
    pdf_filepath = os.path.join(pdf_folder, pdf_filename)
    with open(pdf_filepath, "rb") as pdf_file:
        pdf_blob = pdf_file.read()

    # Hash the PDF using SHA256 and add the '0x' prefix
    pdf_hash = hashlib.sha256(pdf_blob).hexdigest()
    encrypted_pdf = '0x' + pdf_hash

    # Call the stored procedure to update the patient table and insert the unencrypted and encrypted PDF data into the DAG table
    cursor.execute("EXEC [dbo].[InsertAndUpdatePDFs] ?, ?, ?", (patient_key, encrypted_pdf, pdf_blob))

# Commit the changes and close the database connection
conn.commit()
conn.close()
