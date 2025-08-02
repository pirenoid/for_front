from fastapi import FastAPI, Query, HTTPException
from typing import Optional, List
from enum import Enum
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin", "Authorization"],
)

persons_db = {
    "1": {
        "id": "1",
        "photoUrl": "https://example.com/photos/1.jpg",
        "relationType": "дедушка",
        "fullName": "Иванов Иван Иванович",
        "age": 75,
        "isPublic": True,
        "canSearchMatches": True,
        "downloadUrl": "/persons/1/download",
        "basicInfo": {
            "lastName": "Иванов",
            "firstName": "Иван",
            "middleName": "Иванович",
            "gender": "MALE",
            "lifeStatus": "DECEASED",
            "birth": {
                "dateType": "EXACT",
                "startDate": "1940-05-15",
                "location": "Москва"
            },
            "death": {
                "dateType": "EXACT",
                "startDate": "2015-03-10",
                "location": "Санкт-Петербург"
            }
        },
        "biography": {
            "content": "Родился в Москве в 1940 году...",
            "media": [
                {
                    "id": "media-1",
                    "url": "https://example.com/media/1.jpg",
                    "type": "IMAGE",
                    "description": "Молодые годы"
                }
            ],
            "lastUpdated": "2023-01-15T10:30:00"
        },
        "events": [
            {
                "id": "event-1",
                "type": "BIRTH",
                "dateInfo": {
                    "dateType": "EXACT",
                    "startDate": "1940-05-15"
                },
                "location": "Москва",
                "isSystem": True
            },
            {
                "id": "event-2",
                "type": "MARRIAGE",
                "dateInfo": {
                    "dateType": "EXACT",
                    "startDate": "1965-07-20"
                },
                "location": "Ленинград",
                "description": "Женился на Петровой Марии"
            }
        ]
    },
    "2": {
        "id": "2",
        "photoUrl": "https://example.com/photos/2.jpg",
        "relationType": "бабушка",
        "fullName": "Иванова Мария Петровна",
        "age": 72,
        "isPublic": True,
        "canSearchMatches": True,
        "downloadUrl": "/persons/2/download",
        "basicInfo": {
            "lastName": "Иванова",
            "firstName": "Мария",
            "middleName": "Петровна",
            "gender": "FEMALE",
            "lifeStatus": "DECEASED",
            "birth": {
                "dateType": "EXACT",
                "startDate": "1945-08-20",
                "location": "Ленинград"
            },
            "death": {
                "dateType": "EXACT",
                "startDate": "2017-11-05",
                "location": "Санкт-Петербург"
            }
        },
        "biography": {
            "content": "Родилась в Ленинграде в 1945 году...",
            "media": [],
            "lastUpdated": "2023-01-16T11:20:00"
        },
        "events": [
            {
                "id": "event-3",
                "type": "BIRTH",
                "dateInfo": {
                    "dateType": "EXACT",
                    "startDate": "1945-08-20"
                },
                "location": "Ленинград",
                "isSystem": True
            }
        ]
    },
    "3": {
        "id": "3",
        "photoUrl": None,
        "relationType": "отец",
        "fullName": "Иванов Сергей Иванович",
        "age": 50,
        "isPublic": False,
        "canSearchMatches": False,
        "downloadUrl": "/persons/3/download",
        "basicInfo": {
            "lastName": "Иванов",
            "firstName": "Сергей",
            "middleName": "Иванович",
            "gender": "MALE",
            "lifeStatus": "ALIVE",
            "birth": {
                "dateType": "EXACT",
                "startDate": "1973-02-10",
                "location": "Ленинград"
            },
            "death": None
        },
        "biography": {
            "content": None,
            "media": [],
            "lastUpdated": "2023-01-10T09:15:00"
        },
        "events": []
    },
    "4": {
        "id": "4",
        "photoUrl": "https://example.com/photos/4.jpg",
        "relationType": "мать",
        "fullName": "Иванова Елена Сергеевна",
        "age": 48,
        "isPublic": False,
        "canSearchMatches": False,
        "downloadUrl": "/persons/4/download",
        "basicInfo": {
            "lastName": "Иванова",
            "firstName": "Елена",
            "middleName": "Сергеевна",
            "maidenName": "Петрова",
            "gender": "FEMALE",
            "lifeStatus": "ALIVE",
            "birth": {
                "dateType": "EXACT",
                "startDate": "1975-06-25",
                "location": "Санкт-Петербург"
            },
            "death": None
        },
        "biography": {
            "content": "Работает врачом в городской больнице.",
            "media": [
                {
                    "id": "media-2",
                    "url": "https://example.com/media/2.jpg",
                    "type": "IMAGE",
                    "description": "На работе"
                }
            ],
            "lastUpdated": "2023-02-01T14:45:00"
        },
        "events": [
            {
                "id": "event-4",
                "type": "EDUCATION",
                "dateInfo": {
                    "dateType": "RANGE",
                    "startDate": "1992-09-01",
                    "endDate": "1998-06-30"
                },
                "location": "Санкт-Петербургский медицинский университет",
                "description": "Окончила с отличием"
            }
        ]
    },
    "5": {
        "id": "5",
        "photoUrl": "https://example.com/photos/5.jpg",
        "relationType": "сын",
        "fullName": "Иванов Алексей Сергеевич",
        "age": 25,
        "isPublic": True,
        "canSearchMatches": True,
        "downloadUrl": "/persons/5/download",
        "basicInfo": {
            "lastName": "Иванов",
            "firstName": "Алексей",
            "middleName": "Сергеевич",
            "gender": "MALE",
            "lifeStatus": "ALIVE",
            "birth": {
                "dateType": "EXACT",
                "startDate": "1998-11-15",
                "location": "Санкт-Петербург"
            },
            "death": None
        },
        "biography": {
            "content": "Учится в аспирантуре.",
            "media": [],
            "lastUpdated": "2023-01-20T16:30:00"
        },
        "events": [
            {
                "id": "event-5",
                "type": "EDUCATION",
                "dateInfo": {
                    "dateType": "RANGE",
                    "startDate": "2016-09-01",
                    "endDate": "2022-06-30"
                },
                "location": "СПбГУ",
                "description": "Бакалавриат и магистратура"
            }
        ]
    }
}

@app.get("/persons")
def list_persons():
    return list(persons_db.values())

@app.post("/persons")
def create_person():
    return persons_db["1"]

@app.get("/persons/{person_id}")
def get_person(person_id: str):
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons_db[person_id]

@app.patch("/persons/{person_id}")
def update_person(person_id: str):
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons_db[person_id]

@app.put("/persons/{person_id}/photo")
def update_photo(person_id: str):
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons_db[person_id]

@app.delete("/persons/{person_id}/photo")
def delete_photo(person_id: str, confirmed: bool = Query(False)):
    if not confirmed:
        raise HTTPException(status_code=400, detail="Confirmation required")
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons_db[person_id]

@app.get("/persons/{person_id}/events")
def get_events(person_id: str, limit: int = 20, offset: int = 0):
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons_db[person_id]["events"][offset:offset+limit]

@app.post("/persons/{person_id}/events")
def create_event(person_id: str):
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")
    return {
        "id": "event-new",
        "type": "OTHER",
        "dateInfo": {
            "dateType": "EXACT",
            "startDate": "2023-01-01"
        }
    }

@app.patch("/persons/{person_id}/events/{event_id}")
def update_event(person_id: str, event_id: str):
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")
    return {
        "id": event_id,
        "type": "OTHER",
        "dateInfo": {
            "dateType": "EXACT",
            "startDate": "2023-01-01"
        }
    }

@app.delete("/persons/{person_id}/events/{event_id}")
def delete_event(person_id: str, event_id: str, confirmed: bool = Query(False)):
    if not confirmed:
        raise HTTPException(status_code=400, detail="Confirmation required")
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")
    return {"status": "deleted"}

@app.put("/persons/{person_id}/biography")
def update_biography(person_id: str):
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons_db[person_id]["biography"]

@app.post("/persons/{person_id}/biography/media")
def add_biography_media(person_id: str):
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")
    return {
        "id": "media-new",
        "url": "https://example.com/media/new.jpg",
        "type": "IMAGE",
        "uploadedAt": "2023-01-01T00:00:00"
    }

@app.delete("/persons/{person_id}/biography/media/{media_id}")
def delete_biography_media(person_id: str, media_id: str, confirmed: bool = Query(False)):
    if not confirmed:
        raise HTTPException(status_code=400, detail="Confirmation required")
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")
    return {"status": "deleted"}

@app.post("/persons/{person_id}/matches")
def search_matches(person_id: str):
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")
    return {"jobId": "job-123"}

@app.post("/persons/{person_id}/archive-search")
def search_archives(person_id: str):
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")
    return {"jobId": "job-456"}

@app.get("/persons/{person_id}/download")
def download_person(person_id: str, format: str = "PDF"):
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")
    return {"message": f"Downloading person {person_id} in {format} format"}


"""dev_login_stub.py
FastAPI‑заглушка ровно под спецификацию Dev Lock Login API v1.0.2

• POST /dev-login — принимает JSON {login, password} и возвращает mock‑JWT.
• Логин/пароль по умолчанию: admin / adimi.
• Токен живёт 3600 сек (1 час) и используется как Bearer‑token на клиенте.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid, time

app = FastAPI(title="Dev Lock Login API", version="1.0.2")

# ---------------------------------------------------------------------------
# Константы (простейшая конфигурация, можно вынести в env‑переменные)
# ---------------------------------------------------------------------------
SECRET_LOGIN = "admin"
SECRET_PASSWORD = "adimi"
TOKEN_TTL = 3600  # secs

# ---------------------------------------------------------------------------
# Pydantic‑модели запроса/ответа (один‑в‑один с OpenAPI)
# ---------------------------------------------------------------------------

class LoginRequest(BaseModel):
    login: str
    password: str

class LoginResponse(BaseModel):
    accessToken: str
    tokenType: str = "Bearer"
    expiresIn: int

# ---------------------------------------------------------------------------
# Вспомогалка: генерируем mock JWT (здесь без подписи, т‑к это лишь заглушка)
# ---------------------------------------------------------------------------

def _issue_jwt() -> str:
    """Собираем строку вида: mock.<uuid>.<expUnix>"""
    exp = int(time.time()) + TOKEN_TTL
    return f"mock.{uuid.uuid4()}.{exp}"

# ---------------------------------------------------------------------------
# /dev-login
# ---------------------------------------------------------------------------

@app.post("/dev-login", response_model=LoginResponse, tags=["Dev Access"], summary="Логин → JWT")
def dev_login(payload: LoginRequest):
    if payload.login != SECRET_LOGIN or payload.password != SECRET_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid login or password")

    return LoginResponse(accessToken=_issue_jwt(), expiresIn=TOKEN_TTL)
