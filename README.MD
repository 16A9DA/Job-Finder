### Job Finder


## Description
This project is a PDF parsing and information extraction tool that converts PDF files (including scanned/image-based PDFs) into structured JSON data. It uses OCR (Optical Character Recognition) via Tesseract to handle scanned documents and AI model such llama3 by using prompt to extract key information like names, email addresses, phone numbers, job titles, and countries.

FastAPI is used to receive uploaded files from users in main.py. Since, file is changed to bytes by Uploadfile type of FastApi.
The pdf_to_json() function is using io.BytesIO() to treat the the bytes input from Uploadfile as file. 

The tool is particularly useful for processing resumes/CVs, to generate profile. The profile information can be used to 
find jobs for the user using Machine Learning, user will be represent with available jobs.

mlmodel.py trains a machine learning model to predict job positions based on user skills and retrieve relevant job information such as company, job description, and salary. It uses preprocessing for dataset/cleaning dataset .TF-IDF vectorization for text processing and a Multi-Layer Perceptron (MLP) Classifier for prediction.

## Features
- Extracts text from both text-based and image-based PDFs upload by user using FastApi
- Uses OCR (Tesseract) for scanned documents
- Extracts: Name,Email,Location,Job,Education,skills
- Outputs structured JSON data that will be represented as profile
- Skills from profile of user given to ML model to provide available jobs


```mermaid
flowchart TD
    A["Upload PDF"] --> B["UploadFile (bytes in FastAPI)"]
    B --> C["io.BytesIO (treat bytes as file)"]
    C --> D["PdfReader / OCR (extract text)"]
    D --> E["AI MODEL to structure information / pdf_to_json()"]
    E --> F["JSON → User Profile "]
    F --> G["Skills from Profile (ML) -> Jobs"]
```

## Requirements

```bash
pip install -r requirement.txt
```

```bash
brew install ollama
```

```bash
ollama pull llama3
```

