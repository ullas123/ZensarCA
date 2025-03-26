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
        html_file.write("<html><head><title>Email Comparison Report</title></head><body>")
        html_file.write("<h1>Email Comparison Report</h1>")
        
        html_file.write("<h2>Email ID found in both files:</h2><ul>")
        for email in emails_in_both:
            html_file.write(f"<li>{email}</li>")
        html_file.write("</ul>")
        
        html_file.write("<h2>Email ID found in new file but not in old file:</h2><ul>")
        for email in emails_only_in_new:
            html_file.write(f"<li>{email}</li>")
        html_file.write("</ul>")
        
        html_file.write("<h2>Email ID found in old file but not in new file:</h2><ul>")
        for email in emails_only_in_old:
            html_file.write(f"<li>{email}</li>")
        html_file.write("</ul>")
        
        html_file.write("<h2>Email ID found in both files AND count > 1 in new file:</h2><ul>")
        for email in emails_in_both:
            if count_new[email] > 1:
                html_file.write(f"<li>{email}: {count_new[email]} times</li>")
        html_file.write("</ul>")
        
        html_file.write("<h2>Email ID found in both files AND count > 1 in old file:</h2><ul>")
        for email in emails_in_both:
            if count_old[email] > 1:
                html_file.write(f"<li>{email}: {count_old[email]} times</li>")
        html_file.write("</ul>")
        
        html_file.write("<h2>Summary:</h2>")
        html_file.write(f"<p>Total email count in new file: {len(emails_new)}</p>")
        html_file.write(f"<p>Total email count in old file: {len(emails_old)}</p>")
        html_file.write(f"<p>Total unique email count in new file: {len(set_new)}</p>")
        html_file.write(f"<p>Total unique email count in old file: {len(set_old)}</p>")
        
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
