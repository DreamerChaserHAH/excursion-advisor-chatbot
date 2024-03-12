
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import FastAPI, Form
import os

load_dotenv()

app = FastAPI()
uri = os.getenv("URI")

class RequestEntity(BaseModel):
    city: str
    country: str
    place: str
    budget: int
    date: str
    adventurous: bool

client = MongoClient(uri, server_api=ServerApi('1'))

def ping_mongodb():
    try:
        client.admin.command('ping')
        return True
    except:
        return False

@app.get("/status")
def get_status_check():
    return {"Request Type": "GET", "API Working Status": "Up and Running!", "Mongo Status" : ping_mongodb()}

@app.post("/status")
def post_status_check():
    return {"Request Type": "POST", "API Working Status": "Up and Running!", "Mongo Status": ping_mongodb()}

@app.post("/get_data")
async def get_data(city: str = Form(...), country: str = Form(...), place: str = Form(...), budget: int = Form(...), date: str = Form(...), adventurous: bool = Form(...)):
    request = RequestEntity(city=city, country=country, place=place, budget=budget, date=date, adventurous=adventurous)
    return {"Request Type": "POST", "City": request.city, "Country": request.country, "Place": request.place, "Budget": request.budget, "Date": request.date, "Adventurous": request.adventurous}
