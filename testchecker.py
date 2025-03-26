import argparse
from collections import Counter
from email_validator import validate_email, EmailNotValidError
import re
import datetime

def extract_emails(lines):
    """Extracts and validates email addresses from structured file lines."""
    email_pattern = r'1003EML([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    emails = []
    
    for line in lines:
        match = re.search(email_pattern, line)
        if match:
            email = match.group(1)
            try:
                valid = validate_email(email, check_deliverability=False)
                emails.append(valid.email)
            except EmailNotValidError:
                continue  # Skip invalid emails
    
    return emails

def compare_emails(file1, file2):
    """Compares email occurrences between two files and writes output to an HTML file."""
    emails_old = extract_emails(read_file(file1))
    emails_new = extract_emails(read_file(file2))
    
    set_old = set(emails_old)
    set_new = set(emails_new)
    
    count_old = Counter(emails_old)
    count_new = Counter(emails_new)
    
    emails_in_both = set_old & set_new
    emails_only_in_new = set_new - set_old
    emails_only_in_old = set_old - set_new
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"email_comparison_{timestamp}.html"
    
    with open(output_filename, "w", encoding="utf-8") as html_file:
        html_file.write("<html><head><title>Email Comparison Report</title>")
        html_file.write("<style>")
        html_file.write("body { font-family: Arial, sans-serif; font-size: 14px; }")
        html_file.write("table { width: 100%; border-collapse: collapse; }")
        html_file.write("th, td { border: 1px solid black; padding: 8px; text-align: left; }")
        html_file.write("th { background-color: lightcyan; }")
        html_file.write("</style>")
        html_file.write("</head><body>")
        html_file.write("<h1>Email Comparison Report</h1>")
        
        # Summary Table
        html_file.write("<h2>Summary</h2>")
        html_file.write("<table>")
        html_file.write("<tr><th>Metric</th><th>Count</th></tr>")
        html_file.write(f"<tr><td>Total email count in new file</td><td>{len(emails_new)}</td></tr>")
        html_file.write(f"<tr><td>Total email count in old file</td><td>{len(emails_old)}</td></tr>")
        html_file.write(f"<tr><td>Total unique email count in new file</td><td>{len(set_new)}</td></tr>")
        html_file.write(f"<tr><td>Total unique email count in old file</td><td>{len(set_old)}</td></tr>")
        html_file.write(f"<tr><td>Emails found in both files</td><td>{len(emails_in_both)}</td></tr>")
        html_file.write(f"<tr><td>Emails only in new file</td><td>{len(emails_only_in_new)}</td></tr>")
        html_file.write(f"<tr><td>Emails only in old file</td><td>{len(emails_only_in_old)}</td></tr>")
        html_file.write("</table>")
        
        # Email Listings in Tables
        def write_email_table(title, emails):
            html_file.write(f"<h2>{title}</h2>")
            html_file.write("<table>")
            html_file.write("<tr><th>Email</th><th>Count in New</th><th>Count in Old</th></tr>")
            for email in emails:
                new_count = count_new[email] if email in count_new else 0
                old_count = count_old[email] if email in count_old else 0
                html_file.write(f"<tr><td>{email}</td><td>{new_count}</td><td>{old_count}</td></tr>")
            html_file.write("</table>")
        
        write_email_table("Email ID found in both files", emails_in_both)
        write_email_table("Email ID found in new file but not in old file", emails_only_in_new)
        write_email_table("Email ID found in old file but not in new file", emails_only_in_old)
        
        html_file.write("</body></html>")
    
    print(f"Comparison report saved as {output_filename}")

def read_file(file_path):
    """Reads a file and returns a list of its lines."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare emails between two structured files.")
    parser.add_argument("file1", help="First file to compare (old file)")
    parser.add_argument("file2", help="Second file to compare (new file)")
    
    args = parser.parse_args()
    compare_emails(args.file1, args.file2)
