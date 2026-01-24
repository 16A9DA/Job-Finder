import json
import io
from pypdf import PdfReader
from pdf2image import convert_from_bytes
import pytesseract
from pydantic import BaseModel
from ollama import chat


class Profile(BaseModel):  # Structure of information that will be output in main.py
    Name: str
    Email: str
    Phone_Number: str
    Location: str
    Job: list[str]
    Education: str
    skills: list[str]


# in main function only file and functuon pdftojsson
#  as the it has all the funciton inside // for initial testing
def main():
    pdf = "RayyanAhmedCv.pdf"  # name of pdf_file
    pdf_to_json(pdf)


def extracted_pdf(pdf):  # function used to convert pdf to text

    extracted_text = ""
    try:

        reader = PdfReader(
            io.BytesIO(pdf)
        )  # treat bytes as a file as requirement of FastApi UploadFile type it in main from Fastapi
        for pages in reader.pages:
            extracted_text += (
                pages.extract_text() or ""
            )  # loops through every page and extracts text if no text then empty string
    except Exception as e:
        print("No extraction", e)

    if not extracted_text.strip():  # if extract is empty in case pdf is image
        images = convert_from_bytes(pdf)
        for img in images:
            extracted_text += pytesseract.image_to_string(
                img
            )  # pytesseract.image_to_string is a function that reads img and converts to string

    return extracted_text


def ai_model(text):
    prompt = f"""
    You are given resume text extracted from a PDF.
    Extract the following fields strictly in JSON format:
    You are an information extraction system.
    You should not add any newline character

    - Do NOT add explanations
    - Do NOT add markdown
    - Do NOT add extra text
    - Text should be clean

    - Name
    - Email
    -Phone Number
    - Location
    - Job (from experience)
    - Education (Highest education type)
    - Skills (list)
    Resume text:
    {text} """
    # llama3 is the Ai model
    response = chat(
        model="llama3",
        messages=[
            {"role": "user", "content": prompt}  # role and prompt given as content
        ],
        format=Profile.model_json_schema(),  # Generate json schema from the class / so Ai can follow
    )
    # as output will be ["name"]["info"] which would be in raw text/string form
    # jsonloads() used for converting strings into json
    raw = response["message"]["content"]  #
    return json.loads(raw)


def pdf_to_json(
    pdf,
):  # conversion, takes pdf file and outputs json file using llama3 model
    text = extracted_pdf(pdf)
    data = ai_model(text)

    return data


if __name__ == "__main__":
    main()
