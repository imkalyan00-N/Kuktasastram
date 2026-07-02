from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
from datetime import datetime

app = FastAPI()

# Mount static folder for HTML/CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load Kukkuta Sastram Data
with open("kukkuta_data.json", "r", encoding="utf-8") as f:
    sastram_data = json.load(f)

class PredictRequest(BaseModel):
    date: str
    time_slot: int
    punju_1: str
    punju_2: str

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.post("/predict")
def predict_winner(req: PredictRequest):
    # July 2 to July 10, 2026 falls under Krishna Paksham (Cheekati)
    paksham = "Cheekati"
    
    # Get Day of the week from Date
    dt = datetime.strptime(req.date, "%Y-%m-%d")
    day_name = dt.strftime("%A")
    
    # Fetch Direction
    direction = sastram_data["directions"].get(paksham, {}).get(day_name, "నైరుతి (South-West)")
    
    # Fetch Rules for that day
    day_rules = sastram_data["vanthulu"].get(paksham, {}).get(day_name, [])
    
    if not day_rules or req.time_slot > len(day_rules):
        return {
            "winner": "Data Loading...", 
            "direction": f"వదిలే దిక్కు: {direction}", 
            "reasoning": "Ee roju ki inka rules add cheyaledu bro."
        }
        
    rule = day_rules[req.time_slot - 1]
    
    # Matching Logic
    winner_text = "Draw / Evari balam clear ga ledu"
    if req.punju_1 == rule["winner"] and req.punju_2 in rule["defeats"]:
        winner_text = f"🔥 {req.punju_1} గెలుస్తుంది! 🔥"
    elif req.punju_2 == rule["winner"] and req.punju_1 in rule["defeats"]:
        winner_text = f"🔥 {req.punju_2} గెలుస్తుంది! 🔥"
    elif req.punju_1 == rule["winner"]:
        winner_text = f"✨ {req.punju_1} కి బలం ఎక్కువ ఉంది."
    elif req.punju_2 == rule["winner"]:
        winner_text = f"✨ {req.punju_2} కి బలం ఎక్కువ ఉంది."
        
    return {
        "winner": winner_text,
        "direction": f"🧭 వదిలే దిక్కు: {direction}",
        "reasoning": f"సమయం ప్రకారం ఇప్పుడు **{rule['winner']}** కి పవర్ ఉంది."
    }
