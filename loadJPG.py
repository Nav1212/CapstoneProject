import os
import pyodbc
import re

# Get a list of JPEG files from the "PDFHOLDER" folder
jpeg_folder = "PNGDICOM"
jpeg_files = [f for f in os.listdir(jpeg_folder) if f.endswith('.jpeg')]

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

for jpeg_filename in jpeg_files:
    # Extract the PatientKey from the file name
    patient_key = int(re.search(r'(\d+)', jpeg_filename).group(0))

    # Read the JPEG file and convert it into a binary format (BLOB)
    jpeg_filepath = os.path.join(jpeg_folder, jpeg_filename)
    with open(jpeg_filepath, "rb") as jpeg_file:
        jpeg_blob = jpeg_file.read()

    # Call the stored procedure to insert the JPEG data into the DICOM table
    cursor.execute("EXEC [dbo].[InsertJPEGToDICOM] ?, ?", (patient_key, jpeg_blob))

# Commit the changes and close the database connection
conn.commit()
conn.close()
