from fastapi import FastAPI, Response, Request
from utils.converters.jsonToPdf import generate_pdf_from_json_data
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/")
def index():
    return {"details": "Hello, World!"}


@app.post("/converter/json-to-pdf")
async def convertetJsonToPdf(request: Request):
    data = await request.json()
    pdf = generate_pdf_from_json_data(data)
    print(pdf)
    return StreamingResponse(pdf, media_type="application/pdf")
