from fastapi import FastAPI, Query, HTTPException, UploadFile, status, Body
from typing import Optional, List
from enum import Enum
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import uuid

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost",
    "https://drevo.team",
    "http://158.160.148.101/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin", "Authorization"],
)


class DateInfo(BaseModel):
    dateType: str
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    approximateText: Optional[str] = None
    location: Optional[str] = None


class BasicInfo(BaseModel):
    lastName: str
    firstName: str
    middleName: Optional[str] = None
    maidenName: Optional[str] = None
    birthName: Optional[str] = None
    gender: str
    lifeStatus: str
    birth: DateInfo
    death: Optional[DateInfo] = None


class PersonResponse(BaseModel):
    id: str
    photoUrl: Optional[str] = None
    relationType: str
    isPublic: bool
    downloadUrl: str
    basicInfo: BasicInfo


class PersonCreate(BaseModel):
    fromId: str
    relationType: str
    isPublic: bool = False
    basicInfo: BasicInfo


class PersonUpdate(BaseModel):
    relationType: Optional[str] = None
    isPublic: Optional[bool] = None
    basicInfo: Optional[BasicInfo] = None


class MediaItem(BaseModel):
    id: str
    url: str
    type: str
    thumbnailUrl: Optional[str] = None
    description: Optional[str] = None
    uploadedAt: str


class Biography(BaseModel):
    content: Optional[str] = None
    media: List[MediaItem] = None
    lastUpdated: str


class BiographyUpdate(BaseModel):
    content: Optional[str] = None
    mediaIdsToDelete: Optional[List[str]] = None


class Event(BaseModel):
    id: str
    type: str
    dateInfo: DateInfo
    location: Optional[str] = None
    description: Optional[str] = None
    isSystem: bool = False


class EventCreate(BaseModel):
    type: str
    dateInfo: DateInfo
    location: Optional[str] = None
    description: Optional[str] = None


class EventUpdate(BaseModel):
    type: Optional[str] = None
    dateInfo: Optional[DateInfo] = None
    location: Optional[str] = None
    description: Optional[str] = None


persons_db = {
    "1": {
        "id": "1",
        "photoUrl": "https://example.com/photos/1.jpg",
        "relationType": "дедушка",
        "isPublic": False,
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
                    "description": "Молодые годы",
                    "uploadedAt": "2020-01-01T00:00:00"
                }
            ],
            "lastUpdated": "2020-01-01T00:00:00"
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
            }
        ]
    }
}


def generate_id():
    return str(uuid.uuid4())


def get_current_datetime():
    return datetime.now().isoformat()


@app.post("/persons", status_code=status.HTTP_201_CREATED, response_model=PersonResponse)
def create_person(person: PersonCreate):
    person_id = generate_id()

    new_person = {
        "id": person_id,
        "photoUrl": None,
        "relationType": person.relationType,
        "isPublic": person.isPublic,
        "downloadUrl": f"/persons/{person_id}/download",
        "basicInfo": person.basicInfo
    }

    persons_db[person_id] = {
        **new_person,
        "biography": {
            "content": None,
            "media": [],
            "lastUpdated": get_current_datetime()
        },
        "events": []
    }

    return new_person


@app.get("/persons/{person_id}", response_model=PersonResponse)
def get_person(person_id: str):
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")

    person_data = persons_db[person_id]
    return {
        "id": person_data["id"],
        "photoUrl": person_data["photoUrl"],
        "relationType": person_data["relationType"],
        "isPublic": person_data["isPublic"],
        "downloadUrl": person_data["downloadUrl"],
        "basicInfo": person_data["basicInfo"]
    }


@app.patch("/persons/{person_id}", response_model=PersonResponse)
def update_person(person_id: str, person_update: PersonUpdate):
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")

    person = persons_db[person_id]

    if person_update.relationType is not None:
        person["relationType"] = person_update.relationType

    if person_update.isPublic is not None:
        person["isPublic"] = person_update.isPublic

    if person_update.basicInfo is not None:
        person["basicInfo"] = person_update.basicInfo

    return {
        "id": person["id"],
        "photoUrl": person["photoUrl"],
        "relationType": person["relationType"],
        "isPublic": person["isPublic"],
        "downloadUrl": person["downloadUrl"],
        "basicInfo": person["basicInfo"]
    }


@app.put("/persons/{person_id}/photo", response_model=PersonResponse)
def update_photo(person_id: str, photo: UploadFile):
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")

    photo_url = f"https://example.com/photos/{person_id}.jpg"
    persons_db[person_id]["photoUrl"] = photo_url

    person = persons_db[person_id]
    return {
        "id": person["id"],
        "photoUrl": person["photoUrl"],
        "relationType": person["relationType"],
        "isPublic": person["isPublic"],
        "downloadUrl": person["downloadUrl"],
        "basicInfo": person["basicInfo"]
    }


@app.delete("/persons/{person_id}/photo", response_model=PersonResponse)
def delete_photo(person_id: str, confirmed: bool = Query(False)):
    if not confirmed:
        raise HTTPException(status_code=400, detail="Confirmation required")
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")

    persons_db[person_id]["photoUrl"] = None

    person = persons_db[person_id]
    return {
        "id": person["id"],
        "photoUrl": person["photoUrl"],
        "relationType": person["relationType"],
        "isPublic": person["isPublic"],
        "downloadUrl": person["downloadUrl"],
        "basicInfo": person["basicInfo"]
    }


@app.get("/persons/{person_id}/events", response_model=List[Event])
def get_events(person_id: str, limit: int = 20, offset: int = 0):
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons_db[person_id]["events"][offset:offset + limit]


@app.post("/persons/{person_id}/events", status_code=status.HTTP_201_CREATED, response_model=Event)
def create_event(person_id: str, event: EventCreate):
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")

    new_event = {
        "id": generate_id(),
        **event.dict(),
        "isSystem": False
    }
    persons_db[person_id]["events"].append(new_event)
    return new_event


@app.patch("/persons/{person_id}/events/{event_id}", response_model=Event)
def update_event(person_id: str, event_id: str, event_update: EventUpdate):
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")

    events = persons_db[person_id]["events"]
    event_to_update = next((e for e in events if e["id"] == event_id), None)

    if not event_to_update:
        raise HTTPException(status_code=404, detail="Event not found")

    if event_update.type is not None:
        event_to_update["type"] = event_update.type

    if event_update.dateInfo is not None:
        event_to_update["dateInfo"] = event_update.dateInfo

    if event_update.location is not None:
        event_to_update["location"] = event_update.location

    if event_update.description is not None:
        event_to_update["description"] = event_update.description

    return event_to_update


@app.delete("/persons/{person_id}/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(person_id: str, event_id: str):
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")

    events = persons_db[person_id]["events"]
    event_to_delete = next((e for e in events if e["id"] == event_id), None)

    if not event_to_delete:
        raise HTTPException(status_code=404, detail="Event not found")

    persons_db[person_id]["events"] = [e for e in events if e["id"] != event_id]
    return None


@app.put("/persons/{person_id}/biography", response_model=Biography)
def update_biography(person_id: str, biography_update: BiographyUpdate):
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")

    if biography_update.content is not None:
        persons_db[person_id]["biography"]["content"] = biography_update.content

    if biography_update.mediaIdsToDelete:
        media_ids_to_delete = set(biography_update.mediaIdsToDelete)
        persons_db[person_id]["biography"]["media"] = [
            m for m in persons_db[person_id]["biography"]["media"]
            if m["id"] not in media_ids_to_delete
        ]

    persons_db[person_id]["biography"]["lastUpdated"] = get_current_datetime()

    bio = persons_db[person_id]["biography"]
    return {
        "content": bio["content"],
        "media": bio["media"],
        "lastUpdated": bio["lastUpdated"]
    }

@app.post("/persons/{person_id}/biography/media", status_code=status.HTTP_201_CREATED, response_model=MediaItem)
def add_biography_media(person_id: str, file: UploadFile, type: str, description: Optional[str] = None):
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")

    new_media = {
        "id": generate_id(),
        "url": f"https://example.com/media/{generate_id()}",
        "type": type,
        "description": description,
        "uploadedAt": get_current_datetime()
    }
    persons_db[person_id]["biography"]["media"].append(new_media)
    return new_media


@app.delete("/persons/{person_id}/biography/media/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_biography_media(person_id: str, media_id: str, confirmed: bool = Query(False)):
    if not confirmed:
        raise HTTPException(status_code=400, detail="Confirmation required")
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")

    persons_db[person_id]["biography"]["media"] = [
        m for m in persons_db[person_id]["biography"]["media"]
        if m["id"] != media_id
    ]
    return None


@app.post("/persons/{person_id}/archive-search", status_code=status.HTTP_202_ACCEPTED)
def search_archives(person_id: str):
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")
    return {"jobId": generate_id()}


@app.get("/persons/{person_id}/download")
def download_person(person_id: str, format: str = "PDF"):
    if person_id not in persons_db:
        raise HTTPException(status_code=404, detail="Person not found")
    return {"message": f"Downloading person {person_id} in {format} format"}


class LoginRequest(BaseModel):
    login: str
    password: str

@app.post("/dev-login", tags=["Dev Access"], summary="Логин")
def dev_login(payload: LoginRequest):
    if payload.login != 'admin' or payload.password != 'admin':
        raise HTTPException(status_code=401, detail="Invalid login or password")

    return {'message': 'ok'}


class UserRegistration(BaseModel):
    firstName: str
    lastName: str
    gender: Optional[str] = None
    email: Optional[str] = None
    birthDate: Optional[str] = None
    accessToken: Optional[str] = None
    refreshToken: Optional[str] = None


# Хардкод данных
HARDCODED_TREE = {
    "name": "Древо Ивановых"
}

HARDCODED_PERSONS = [
    {
        "id": "person-1",
        "firstName": "Иван",
        "lastName": "Иванов",
        "middleName": "",
        "x": 100,
        "y": 200,
        "gender": "male",
        "birthDate": "1980-05-15",
        "deathDate": "",
        "isAlive": True,
        "role": "Вы",
        "photoUrl": "https://example.com/photos/ivan.jpg"
    },
    {
        "id": "person-2",
        "firstName": "Мария",
        "lastName": "Иванова",
        "middleName": "Петровна",
        "x": 300,
        "y": 200,
        "gender": "female",
        "birthDate": "1985-07-20",
        "deathDate": "",
        "isAlive": True,
        "role": "Супруга",
        "photoUrl": "https://example.com/photos/maria.jpg"
    },
    {
        "id": "person-3",
        "firstName": "Алексей",
        "lastName": "Иванов",
        "middleName": "Иванович",
        "x": 200,
        "y": 350,
        "gender": "male",
        "birthDate": "2010-03-10",
        "deathDate": "",
        "isAlive": True,
        "role": "Сын",
        "photoUrl": "https://example.com/photos/alexey.jpg"
    },
    {
        "id": "person-4",
        "firstName": "Иван",
        "lastName": "Иванов",
        "middleName": "Сергеевич",
        "x": 100,
        "y": 50,
        "gender": "male",
        "birthDate": "1950-01-30",
        "deathDate": "2015-11-25",
        "isAlive": False,
        "role": "Отец",
        "photoUrl": "https://example.com/photos/ivan_sr.jpg"
    },
    {
        "id": "person-5",
        "firstName": "Ольга",
        "lastName": "Иванова",
        "middleName": "Николаевна",
        "x": 300,
        "y": 50,
        "gender": "female",
        "birthDate": "1955-09-12",
        "deathDate": "",
        "isAlive": True,
        "role": "Мать",
        "photoUrl": "https://example.com/photos/olga.jpg"
    }
]

HARDCODED_RELATIONSHIPS = [
    {"id": "rel-1", "fromPersonId": "1", "toPersonId": "2"},
    {"id": "rel-2", "fromPersonId": "1", "toPersonId": "3"},
    {"id": "rel-3", "fromPersonId": "2", "toPersonId": "3"},
    {"id": "rel-4", "fromPersonId": "4", "toPersonId": "1"},
    {"id": "rel-5", "fromPersonId": "5", "toPersonId": "1"},
    {"id": "rel-6", "fromPersonId": "4", "toPersonId": "5"}
]


@app.post("/trees", tags=["Tree Core"])
def create_tree(user_data: UserRegistration):
    """
    Создание нового древа с персоной (пользователем)

    Принимает данные пользователя и создает:
    1. Новое древо с именем по шаблону "Мое древо"
    2. Персону-владельца на основе данных пользователя
    """

    new_tree = {
        "name": f"Мое древо"
    }
    new_person = {
        "id": f"person-1",
        "firstName": user_data.firstName,
        "lastName": user_data.lastName,
        "middleName": "",
        "x": 0,
        "y": 0,
        "gender": user_data.gender or "male",
        "birthDate": user_data.birthDate or "1980-01-01",
        "deathDate": "",
        "isAlive": True,
        "role": "Вы",
        "photoUrl": None
    }

    # Обновляем хардкод-данные (в реальном приложении сохраняли бы в БД)
    global HARDCODED_TREE, HARDCODED_PERSONS
    HARDCODED_TREE = new_tree
    HARDCODED_PERSONS = [new_person] + HARDCODED_PERSONS[1:]  # Сохраняем остальные персоны

    return {
        "tree": new_tree,
        "person": new_person
    }


@app.get("/trees/", tags=["Tree Core"])
def get_tree_data():
    return {
        "tree": HARDCODED_TREE,
        "persons": HARDCODED_PERSONS,
        "relationships": HARDCODED_RELATIONSHIPS
    }


@app.delete("/trees/persons/{personId}", tags=["Persons"])
def delete_person(personId: str):
    # Просто возвращаем те же данные, как будто удалили
    return {
        "tree": HARDCODED_TREE,
        "persons": HARDCODED_PERSONS,
        "relationships": HARDCODED_RELATIONSHIPS
    }


@app.post("/trees/share", tags=["Tree Sharing"])
def share_tree(email_data: dict = Body(..., example={"email": "user@example.com"})):
    """
    Отправка приглашения на совместное редактирование древа

    Требует:
    {
        "email": "string"  # обязательное поле
    }
    """
    email = email_data.get("email")

    if not email:
        raise HTTPException(status_code=400, detail="Email обязателен")

    # Простейшая проверка email
    if "@" not in email or "." not in email.split("@")[-1]:
        raise HTTPException(status_code=400, detail="Невалидный email")

    return {"message": f"Приглашение отправлено на {email}"}


@app.post("/trees/persons/{personId}/invite", tags=["Tree Sharing"])
def invite_to_person(
        personId: str,
        email_data: dict = Body(..., example={"email": "guest@example.com"})
):
    """
    Приглашение на редактирование конкретной персоны

    Требует:
    {
        "email": "string"  # обязательное поле
    }
    """
    # Проверка что персона существует и жива (хардкод)
    if personId not in {"1", "2", "4", "5"}:  # ID 3 - умерший (из примера)
        raise HTTPException(status_code=404, detail="Персона не найдена")

    if personId == "3":
        raise HTTPException(status_code=400, detail="Персона умерла")

    email = email_data.get("email")

    if not email:
        raise HTTPException(status_code=400, detail="Email обязателен")

    if "@" not in email or "." not in email.split("@")[-1]:
        raise HTTPException(status_code=400, detail="Невалидный email")

    return {
        "message": f"Приглашение для персоны {personId} отправлено на {email}"
    }
