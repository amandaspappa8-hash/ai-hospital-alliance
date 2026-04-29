from app.api.clinical_orders import router as clinical_orders_router
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.api.clinical_route import router as clinical_route_router
from fastapi.responses import Response, JSONResponse
import urllib.request
import urllib.error

app = FastAPI(title="AI Hospital Alliance API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TOKENS = {}

DEMO_USERS = {
    "admin": {
        "password": "admin123",
        "role": "Admin",
        "name": "System Admin",
    },
    "doctor": {
        "password": "doctor123",
        "role": "Doctor",
        "name": "Dr. Mohamed",
    },
    "radiology": {
        "password": "radio123",
        "role": "Radiology",
        "name": "Radiology User",
    },
}


class LoginInput(BaseModel):
    username: str
    password: str


@app.get("/")
def root():
    return {"status": "ok", "service": "ai-hospital-alliance-api"}


@app.get("/patients")
def get_patients():
    return [
        {
            "id": "P-1001",
            "name": "Mohamed Ali",
            "department": "Cardiology",
            "status": "In care",
        },
        {
            "id": "P-1002",
            "name": "Sara Hassan",
            "department": "Radiology",
            "status": "Waiting",
        },
        {
            "id": "P-1003",
            "name": "Omar Salem",
            "department": "ER",
            "status": "Discharged",
        },
    ]


@app.get("/reports")
def get_reports():
    return [
        {
            "id": "R-7711",
            "title": "CT Head",
            "patient": "Patient A",
            "type": "Radiology",
            "status": "in-review",
        },
        {
            "id": "R-7709",
            "title": "CBC Panel",
            "patient": "Patient C",
            "type": "Lab",
            "status": "pending",
        },
        {
            "id": "R-7701",
            "title": "Discharge Summary",
            "patient": "Emily Brown",
            "type": "Discharge",
            "status": "completed",
        },
        {
            "id": "R-7688",
            "title": "ER Triage",
            "patient": "Patient B",
            "type": "ER",
            "status": "pending",
        },
    ]


@app.get("/appointments")
def get_appointments():
    return [
        {
            "id": "A-1021",
            "patient": "Sara Ali",
            "department": "Cardiology",
            "doctor": "Dr. Kareem",
            "time": "09:00",
            "status": "scheduled",
        },
        {
            "id": "A-1022",
            "patient": "John Smith",
            "department": "Neurology",
            "doctor": "Dr. Nasser",
            "time": "10:30",
            "status": "checked-in",
        },
        {
            "id": "A-1023",
            "patient": "Mira Omar",
            "department": "Radiology",
            "doctor": "Dr. Lina",
            "time": "12:00",
            "status": "completed",
        },
        {
            "id": "A-1024",
            "patient": "Patient D",
            "department": "ER",
            "doctor": "Dr. Adel",
            "time": "14:15",
            "status": "cancelled",
        },
    ]


@app.post("/auth/login")
def login(data: LoginInput):
    user = DEMO_USERS.get(data.username)
    if not user or user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = f"demo-token-{data.username}"
    TOKENS[token] = {
        "username": data.username,
        "name": user["name"],
        "role": user["role"],
    }

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": TOKENS[token],
    }


@app.get("/auth/me")
def me(token: str):
    user = TOKENS.get(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user


NOTES = {
    "P-1001": [
        {"id": 1, "text": "Chest pain under observation"},
        {"id": 2, "text": "ECG scheduled"},
    ],
    "P-1002": [
        {"id": 1, "text": "Waiting for CT scan"},
    ],
}


@app.get("/notes/{patient_id}")
def get_notes(patient_id: str):
    return NOTES.get(patient_id, [])


class NoteInput(BaseModel):
    text: str


@app.post("/notes/{patient_id}")
def add_note(patient_id: str, data: NoteInput):
    arr = NOTES.setdefault(patient_id, [])
    note = {
        "id": len(arr) + 1,
        "text": data.text,
    }
    arr.append(note)
    return note


REPORTS_BY_PATIENT = {
    "P-1001": [
        {
            "id": "R-100",
            "title": "ECG Report",
            "type": "Cardiology",
            "status": "completed",
        },
        {"id": "R-101", "title": "Blood Panel", "type": "Lab", "status": "pending"},
    ],
    "P-1002": [
        {"id": "R-102", "title": "CT Scan", "type": "Radiology", "status": "in-review"},
    ],
}


@app.get("/reports/{patient_id}")
def get_patient_reports(patient_id: str):
    return REPORTS_BY_PATIENT.get(patient_id, [])


ORDERS = {}


class OrderInput(BaseModel):
    type: str
    department: str
    note: str = ""


@app.get("/orders/{patient_id}")
def get_orders(patient_id: str):
    return ORDERS.get(patient_id, [])


@app.post("/orders/{patient_id}")
def add_order(patient_id: str, data: OrderInput):
    arr = ORDERS.setdefault(patient_id, [])
    order = {
        "id": len(arr) + 1,
        "type": data.type,
        "department": data.department,
        "note": data.note,
        "status": "pending",
    }
    arr.append(order)
    return order


app.include_router(clinical_route_router)

app.include_router(clinical_orders_router)


@app.get("/pacs/studies")
def pacs_studies():
    url = "http://127.0.0.1:8042/dicom-web/studies"
    try:
        with urllib.request.urlopen(url) as r:
            body = r.read()
            content_type = r.headers.get("Content-Type", "application/dicom+json")
            return Response(content=body, media_type=content_type)
    except urllib.error.HTTPError as e:
        return JSONResponse(
            status_code=502, content={"error": f"Orthanc HTTP error: {e.code}"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=502, content={"error": f"Failed to reach Orthanc: {str(e)}"}
        )
