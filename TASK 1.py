
import os
from pdf2image import convert_from_path
import pytesseract


def convert_pdf_to_text(pdf_path, output_txt_path, poppler_path=None):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"The file {pdf_path} does not exist.")

    if os.name == 'nt':
        pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR"
        if not os.path.exists(pytesseract.pytesseract.tesseract_cmd):
            raise FileNotFoundError("Tesseract OCR executable not found at the specified path.")

    try:
        images = convert_from_path(pdf_path, poppler_path=poppler_path)
        print(f"PDF converted to {len(images)} image(s).")
    except Exception as e:
        raise RuntimeError(f"Error during PDF to image conversion: {e}")

    extracted_text = []
    for page_num, image in enumerate(images, start=1):
        try:

            page_text = pytesseract.image_to_string(image, config='--psm 6')
            print(f"Extracted text for page {page_num}:\n{page_text[:100]}...")
            extracted_text.append(f"--- Page {page_num} ---\n{page_text}\n")
        except Exception as e:
            print(f"Error processing page {page_num}: {e}")

    try:
        with open(output_txt_path, 'w', encoding='utf-8') as output_file:
            output_file.writelines(extracted_text)
            print(f"Text extracted and saved to {output_txt_path}")
    except Exception as e:
        raise RuntimeError(f"Error writing to output file: {e}")


if __name__ == "_main_":
    pdf_path = r"C:\\Users\\Yuvayash\\Downloads\\numbers image .pdf"
    output_txt_path = r"C:\\Users\\Yuvayash\\OneDrive\\Desktop\\New Text Document.txt"
    poppler_path = r"C:\\Users\\Yuvayash\\Downloads\\poppler-24.08.0\\Library\\bin"

    try:
        convert_pdf_to_text(pdf_path, output_txt_path, poppler_path=poppler_path)
    except Exception as e:
        print(f"An error occurred: {e}")