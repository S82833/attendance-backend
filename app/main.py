from fastapi import FastAPI, File, UploadFile, Form
from app.firestore_client import save_attendance, get_all_attendances
from app.r2_uploader import upload_image_to_r2
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime, timezone
from datetime import timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://asistencia.talentedgeperu.com"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/attendances/")
async def create_attendance(
    uid: str = Form(...),
    lat: float = Form(...),
    lng: float = Form(...),
    image: UploadFile = File(...)
):
    try:
        image_url = await upload_image_to_r2(image, uid)

        save_attendance(
            uid=uid,
            image_url=image_url,
            timestamp=datetime.now(timezone.utc) - timedelta(hours=5),
            location={"lat": lat, "lng": lng}
        )

        return {"status": "ok", "image_url": image_url}

    except Exception as e:
        return JSONResponse(status_code=500, content={
            "status": "error",
            "message": str(e)
        })
    

@app.get("/attendances/")
def list_attendances():
    try:
        attendances = get_all_attendances()
        return {"attendances": attendances}
    except Exception as e:
        return JSONResponse(status_code=500, content={
            "status": "error",
            "message": str(e)
        })