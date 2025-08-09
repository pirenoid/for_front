from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

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