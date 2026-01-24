from fastapi import FastAPI, UploadFile, HTTPException
from project import pdf_to_json


app = FastAPI()


@app.get("/")
def greet():
    return "Hello to Job finder"


@app.post("/uploadfile")
async def upload_file_output(file: UploadFile):  # UploadFile changes pdf to binary
    if file.content_type != "application/pdf":  # check if file is pdf
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type {file.content_type.split('/')[1]}. Please upload in Pdf format",
        )  # raising error 400 if file type is in valid, displaying, file type by user
    reader = await file.read()  # reads file
    try:
        result = pdf_to_json(reader)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing pdf: {e}"
        )  # incase of any exception raise 500 and exception namae

    return result
