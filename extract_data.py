import re
import csv

def extract_emails_to_csv(input_txt_file, output_csv_file):
    # Read the text file
    with open(input_txt_file, 'r') as file:
        text = file.read()

    # Use regex to find all email addresses enclosed in <>
    emails = re.findall(r'<(.*?)>', text)

    # Write the emails to a CSV in a single row
    with open(output_csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(emails)

# Example usage
extract_emails_to_csv('input.txt', 'output.csv')
