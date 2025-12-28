import re
import pdfplumber
import pytesseract
from pdf2image import convert_from_path


def extract_resume_text(pdf_path):
    """
    Extract text from resume PDF:
    1️⃣ Try digital text extraction (pdfplumber)
    2️⃣ Fallback to OCR only if text is insufficient
    """

    text = ""

    # ==========================
    # 1️⃣ Try pdfplumber first
    # ==========================
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"[pdfplumber error] {pdf_path}: {e}")

    # ==========================
    # 2️⃣ OCR fallback (only if needed)
    # ==========================
    if len(text.strip()) < 50:
        print(f"🔍 OCR fallback triggered for: {pdf_path}")

        try:
            images = convert_from_path(pdf_path)
            for img in images:
                ocr_text = pytesseract.image_to_string(img)
                if ocr_text:
                    text += ocr_text + "\n"

        except Exception as e:
            print(f"[OCR error] {pdf_path}: {e}")

    return text.strip()


def clean_resume_text(text):
    """
    Clean resume text before embedding:
    - Normalize spaces
    - Remove junk characters
    """

    if not text:
        return ""

    # Convert to lowercase for consistency
    text = text.lower()

    # Remove multiple spaces/newlines
    text = re.sub(r'\s+', ' ', text)

    # Remove non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    # Remove repeated symbols
    text = re.sub(r'[•●▪■◆]+', ' ', text)

    return text.strip()
