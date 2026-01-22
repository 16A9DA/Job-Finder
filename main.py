import shutil
from project import pdf_to_json
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.get("/")
def greet():
    return "Hello to Job finder"


@app.post("/uploadfile")
async def upload_file_output(file: UploadFile):  # UploadFile changes pdf to binary
    if file.content_type != "application/pdf":  # check if file is pdf
        return "File type is not pdf"
    result = await file.read()  # reads file

    return pdf_to_json(result)
