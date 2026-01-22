### Job Finder

#### Description
Imp: The project is not completed. In the process
Extract pdf from user which generates user profiles and uses NLP/ML to find user jobs.

## Description

This project is a PDF parsing and information extraction tool that converts PDF files (including scanned/image-based PDFs) into structured JSON data. It uses OCR (Optical Character Recognition) via Tesseract to handle scanned documents and regular expressions to extract key information like names, email addresses, phone numbers, job titles, and countries.

FastApi used to take file from user in main.py file. Since, file is changed to bytes by Uploadfile type of FastApi.
The pdf_to_json() function is using io.BytesIO() to treat the the bytes input from Uploadfile as file. 

The tool is particularly useful for processing resumes/CVs, to generate profile. The profile information can be used to 
find jobs for the user using Machine Learning, user will be represent with available jobs.

## Features
- Extracts text from both text-based and image-based PDFs upload by user using FastApi
- Uses OCR (Tesseract) for scanned documents
- Extracts: Name, Email, Phone Number, Job Title, Country
- Outputs structured JSON data that will be represented as profile
- Handles various PDF formats and encodings


```mermaid
flowchart TD
    A["Upload PDF"] --> B["UploadFile (bytes in FastAPI)"]
    B --> C["io.BytesIO (treat bytes as file)"]
    C --> D["PdfReader / OCR (extract text)"]
    D --> E["Regex / pdf_to_json()"]
    E --> F["JSON → User Profile → ML Job Matching"]

## Requirements
```bash
pip install -r requirement.txt
