import json
import re
import io
from pypdf import PdfReader
from pdf2image import convert_from_bytes
import pytesseract



# in main function only file and functuon pdftojsson
#  as the it has all the funciton inside
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


def extract_name(text):
    first_line = text.strip().split("\n")[0]  # get first line
    name = " ".join(
        first_line.split()[:2]
    ).title()  # take first 2 words and makes it in title
    return name


def regex(text):
    # checks for pattern in a document which will be used later
    # list of jobs and countries as they can be determined
    result = {}  # the regex result that is a dict
    result["name"] = [extract_name(text).title()]  # take first name, apply title (just incase)
    jobs = [
        "Software Engineer",
        "Web Developer",
        "Data Analyst",
        "Data Scientist",
        "Project Manager",
        "Product Manager",
        "Business Analyst",
        "Graphic Designer",
        "UX Designer",
        "UI Designer",
        "Accountant",
        "Consultant",
        "Teacher",
        "Professor",
        "Researcher",
        "Marketing Manager",
        "Sales Manager",
        "HR Manager",
        "Financial Analyst",
        "Civil Engineer",
        "Mechanical Engineer",
        "Electrical Engineer",
        "Doctor",
        "Nurse",
        "Lawyer",
        "Attorney",
        "Architect",
        "Chef",
        "Pilot",
        "Journalist",
        "Writer",
        "Photographer",
        "Machine Learning Engineer",
        "Customer Service",
    ]

    countries = [
        "USA",
        "United States",
        "Canada",
        "UK",
        "United Kingdom",
        "India",
        "Pakistan",
        "Germany",
        "France",
        "Australia",
        "Brazil",
        "China",
        "Japan",
        "Mexico",
        "Russia",
        "South Africa",
        "Italy",
        "Spain",
        "Argentina",
        "Egypt",
        "Saudi Arabia",
        "Turkey",
        "Sweden",
        "Norway",
        "Netherlands",
        "Belgium",
        "Switzerland",
        "New Zealand",
        "Thailand",
        "Malaysia",
        "Singapore",
        "Hungary",
    ]
    patterns = {
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone_number": r"\+?\d[\d\s\-\((\)]{9,14}\d",
        "job": r"\b(?:{})\b".format("|".join(jobs)),
        "country": r"\b(?:{})\b".format(
            "|".join(countries)
        ),  # pattern of the the info need
    }
    # loops through pattern key and items
    for key, pattern in patterns.items():
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        matches = [m.lower() for m in matches]
        result[key] = list(set(matches))
    return result


def pdf_to_json(
    pdf
):  # conversion, takes pdf file and outputs json file uses regex function
    text = extracted_pdf(pdf)
    data = regex(text)

    # with open(output_file, "w", encoding="UTF-8") as output_file:
    #     json.dump(
    #         data, output_file, ensure_ascii=False, indent=2
    #     )  # puts all data in json

    # # print(f"Data saved to {json_path}")
    return data


if __name__ == "__main__":
    main()
