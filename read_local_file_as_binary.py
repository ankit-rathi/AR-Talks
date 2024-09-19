# Path to your PDF file
pdf_file_path = 'path/to/your/file.pdf'

# Read the PDF file as binary
with open(pdf_file_path, 'rb') as file:
    binary_data = file.read()  # This reads the PDF as binary

# Now `binary_data` contains the binary content of the PDF file
print("PDF file read as binary successfully!")
