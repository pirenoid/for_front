from fastapi import FastAPI, Query, HTTPException, Body, Response
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

ALLOWED_ROLES = {"participant", "admin"}
ALLOWED_STATUSES = {"pending", "accepted", "declined"}

_invites_db = {
    "1": {"id": "1", "email": "anna@example.com",    "nameSurname": "Анна Сидорова",
          "invitedAt": "2025-07-01", "status": "pending",  "role": "participant", "treeName": "Семья Сидоровых"},
    "2": {"id": "2", "email": "boris@example.com",   "nameSurname": "Борис Иванов",
          "invitedAt": "2025-07-03", "status": "accepted", "role": "admin",       "treeName": "Семья Ивановых"},
    "3": {"id": "3", "email": "svetlana@example.com","nameSurname": "Светлана Петрова",
          "invitedAt": "2025-07-05", "status": "declined", "role": "participant", "treeName": "Семья Петровых"},
    "4": {"id": "4", "email": "dmitry@example.com",  "nameSurname": "Дмитрий Орлов",
          "invitedAt": "2025-07-10", "status": "pending",  "role": "participant", "treeName": "Семья Орловых"},
    "5": {"id": "5", "email": "maria@example.com",   "nameSurname": "Мария Романова",
          "invitedAt": "2025-07-12", "status": "pending",  "role": "admin",       "treeName": "Семья Романовых"},
}

# Токены для by-token ручек
_token_to_invite = {
    "tok-1-accept": "1", "tok-2-accept": "2", "tok-3-accept": "3", "tok-4-accept": "4", "tok-5-accept": "5",
    "tok-1-decline": "1","tok-2-decline": "2","tok-3-decline": "3","tok-4-decline": "4","tok-5-decline": "5",
}

@app.get("/invites", tags=["invites"])
def list_invites(
    search: str | None = Query(None, description="Подстрочный поиск по nameSurname"),
    sort: str = Query("date", pattern="^(date|name)$", description="Поле сортировки: date|name"),
    order: str = Query("desc", pattern="^(asc|desc)$", description="Порядок сортировки: asc|desc"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    items = list(_invites_db.values())

    # фильтр: строго по nameSurname
    if search:
        s = search.lower()
        items = [it for it in items if s in it["nameSurname"].lower()]

    # сортировка
    key_fn = (lambda it: it["invitedAt"]) if sort == "date" else (lambda it: it["nameSurname"])
    items.sort(key=key_fn, reverse=(order == "desc"))

    total = len(items)
    items = items[offset:offset + limit]
    return {"items": items, "total": total}

@app.post("/invites", status_code=201, tags=["invites"])
def create_invite(body: dict = Body(...)):
    email = body.get("email")
    role = body.get("role")
    if not email or role not in ALLOWED_ROLES:
        raise HTTPException(status_code=400, detail="email и role обязательны; role ∈ {participant, admin}")

    new_id = str(max(map(int, _invites_db.keys())) + 1)
    invite = {
        "id": new_id,
        "email": email,
        "nameSurname": body.get("nameSurname") or email.split("@")[0].capitalize(),
        "invitedAt": "2025-08-01",
        "status": "pending",
        "role": role,
        "treeName": body.get("treeName") or "Семья Романовых",
    }
    _invites_db[new_id] = invite
    _token_to_invite[f"tok-{new_id}-accept"] = new_id
    _token_to_invite[f"tok-{new_id}-decline"] = new_id
    return invite

@app.patch("/invites/{inviteId}", tags=["invites"])
def update_invite_role(inviteId: str, body: dict = Body(...)):
    if inviteId not in _invites_db:
        raise HTTPException(status_code=404, detail="Приглашение не найдено")
    role = body.get("role")
    if role not in ALLOWED_ROLES:
        raise HTTPException(status_code=400, detail="Некорректное значение role (participant|admin)")
    _invites_db[inviteId]["role"] = role
    return _invites_db[inviteId]

@app.delete("/invites/{inviteId}", status_code=204, tags=["invites"])
def delete_invite(inviteId: str):
    if inviteId not in _invites_db:
        raise HTTPException(status_code=404, detail="Приглашение не найдено")
    _invites_db.pop(inviteId, None)
    # подчистим связанные токены
    for k in list(_token_to_invite.keys()):
        if _token_to_invite[k] == inviteId:
            _token_to_invite.pop(k, None)
    return Response(status_code=204)

@app.post("/invites/by-token/{token}/accept", tags=["invites"])
def accept_invite(token: str):
    invite_id = _token_to_invite.get(token)
    if not invite_id:
        raise HTTPException(status_code=400, detail="Некорректный или просроченный токен")
    if invite_id not in _invites_db:
        raise HTTPException(status_code=404, detail="Приглашение не найдено")
    _invites_db[invite_id]["status"] = "accepted"
    return _invites_db[invite_id]

@app.post("/invites/by-token/{token}/decline", tags=["invites"])
def decline_invite(token: str):
    invite_id = _token_to_invite.get(token)
    if not invite_id:
        raise HTTPException(status_code=400, detail="Некорректный или просроченный токен")
    if invite_id not in _invites_db:
        raise HTTPException(status_code=404, detail="Приглашение не найдено")
    _invites_db[invite_id]["status"] = "declined"
    return _invites_db[invite_id]
