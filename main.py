from fastapi import FastAPI, UploadFile, HTTPException
from project import pdf_to_json
from mlmodel import predict_data, load_ml_model

tfid, tfd_MLP, X_train_tfid, X_train, df = load_ml_model()

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
        predict = predict_data(
            result["skills"], tfid, tfd_MLP, X_train_tfid, X_train, df
        )  # take result and predict
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing pdf: {e}"
        )  # incase of any exception raise 500 and exception namae
    # response with user profile and job
    response = {"Profile": result, "Job": predict}
    return response
