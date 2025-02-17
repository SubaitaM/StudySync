import pdfplumber
import dateparser
import re

# Regex patterns for date formats
DATE_PATTERNS = [
    r"\b\d{1,2} [A-Za-z]+ \d{4}\b",       # 12 January 2023
    r"\b[A-Za-z]+ \d{1,2}, \d{4}\b",      # January 12, 2023
    r"\b\d{2}/\d{2}/\d{4}\b",             # 12/01/2023 or 01/12/2023
    r"\b\d{2}-\d{2}-\d{4}\b",             # 12-01-2023 or 01-12-2023
    r"\b[A-Za-z]+ \d{1,2}, \d{1,2}:\d{2} (?:am|pm)\b",  # December 21, 9:00 am
]

def infer_year(dates):
    """
    Infers the correct year for midterm and final exam dates based on the semester system.
    
    Args:
        dates (list): List of extracted date strings in YYYY-MM-DD format.
    
    Returns:
        list: List of corrected date strings in YYYY-MM-DD format.
    """
    inferred_dates = []
    
    # Sort extracted dates for proper processing
    dates = sorted(dates)
    
    # Identify a known reference date (Deferred Final Exam)
    deferred_final_exam = None
    for date in dates:
        if "-01-13" in date:  # We know Deferred Final Exam happens in January
            deferred_final_exam = date
            break

    if deferred_final_exam:
        year = int(deferred_final_exam[:4])  # Extract year (e.g., 2024)
        main_final_exam_year = year - 1  # Main Final Exam happened in December of previous year
        semester_start_year = main_final_exam_year  # Semester starts in September of the same year

        for date in dates:
            month = int(date[5:7])  # Extract month
            if month >= 9 and month <= 12:  # If in Fall semester range
                corrected_date = f"{semester_start_year}{date[4:]}"  # Assign inferred year
            else:
                corrected_date = date  # Already correct year
            
            inferred_dates.append(corrected_date)
    
    return sorted(inferred_dates)


def extract_dates_from_pdf(pdf_path):
    extracted_dates = set()
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract text and fix spacing issues
            text = page.extract_text(x_tolerance=2, y_tolerance=2)
            if text:
                text = re.sub(r'(?<=[a-zA-Z])(?=[A-Z])', ' ', text)  # Fix missing spaces

                # Search for dates in text
                for pattern in DATE_PATTERNS:
                    for match in re.findall(pattern, text):
                        parsed_date = dateparser.parse(match)
                        if parsed_date:
                            extracted_dates.add(parsed_date.strftime("%Y-%m-%d"))

            # Extract tables
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    for cell in row:
                        if cell:
                            for pattern in DATE_PATTERNS:
                                for match in re.findall(pattern, cell):
                                    parsed_date = dateparser.parse(match)
                                    if parsed_date:
                                        extracted_dates.add(parsed_date.strftime("%Y-%m-%d"))

    corrected_dates = infer_year(sorted(extracted_dates))
    return corrected_dates


# Run script
if _name_ == "_main_":
    pdf_file_path = "sample.pdf"  # Change to your actual PDF file
    extracted_dates = extract_dates_from_pdf(pdf_file_path)
    print("✅ Corrected Extracted Dates:", extracted_dates)
