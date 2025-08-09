from fastapi import FastAPI, HTTPException, Query, Body, Response

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

_persons = {
    "1": {"id": "1", "surname": "Иванов",  "name": "Иван"},
    "2": {"id": "2", "surname": "Иванова", "name": "Мария"},
    "3": {"id": "3", "surname": "Петров",  "name": "Сергей"},
    "4": {"id": "4", "surname": "Сидорова","name": "Елена"},
    "5": {"id": "5", "surname": "Орлов",   "name": "Дмитрий"},
}

_events = {
    "e1": {"id": "e1", "name": "Свадьба 1965"},
    "e2": {"id": "e2", "name": "Окончание вуза 1998"},
    "e3": {"id": "e3", "name": "Рождение 1998-11-15"},
}
_geotags = {
    "g1": {"id": "g1", "locationName": "Москва",          "coordinates": {"latitude": 55.75, "longitude": 37.61}},
    "g2": {"id": "g2", "locationName": "Санкт-Петербург", "coordinates": {"latitude": 59.93, "longitude": 30.31}},
    "g3": {"id": "g3", "locationName": "Ленинград",       "coordinates": {"latitude": 59.93, "longitude": 30.25}},
}

_media = {
    "m1": {
        "id": "m1", "type": "photo", "fileName": "grandpa", "fileExtension": "jpg", "fileSize": 123456,
        "dateAdded": "2025-08-01", "previewUrl": "https://example.com/media/m1_preview.jpg",
        "originalUrl": "https://example.com/media/m1.jpg", "description": "Дедушка в молодости.",
        "persons": [ _persons["1"], _persons["2"] ], "events": [ _events["e1"] ], "geotags": [ _geotags["g1"] ],
    },
    "m2": {
        "id": "m2", "type": "video", "fileName": "interview", "fileExtension": "mp4", "fileSize": 9876543,
        "dateAdded": "2025-08-02", "previewUrl": "https://example.com/media/m2_preview.jpg",
        "originalUrl": "https://example.com/media/m2.mp4", "description": "Интервью с отцом.",
        "persons": [ _persons["3"] ], "events": [ _events["e2"] ], "geotags": [ _geotags["g2"] ],
    },
    "m3": {
        "id": "m3", "type": "photo", "fileName": "mom_university", "fileExtension": "png", "fileSize": 222222,
        "dateAdded": "2025-08-03", "previewUrl": "https://example.com/media/m3_preview.jpg",
        "originalUrl": "https://example.com/media/m3.png", "description": "",
        "persons": [ _persons["4"] ], "events": [ _events["e2"] ], "geotags": [],
    },
    "m4": {
        "id": "m4", "type": "photo", "fileName": "son_birth", "fileExtension": "jpg", "fileSize": 333333,
        "dateAdded": "2025-08-03", "previewUrl": "https://example.com/media/m4_preview.jpg",
        "originalUrl": "https://example.com/media/m4.jpg", "description": "",
        "persons": [ _persons["5"] ], "events": [ _events["e3"] ], "geotags": [ _geotags["g2"] ],
    },
    "m5": {
        "id": "m5", "type": "photo", "fileName": "grandpa_award", "fileExtension": "jpg", "fileSize": 444444,
        "dateAdded": "2025-08-01", "previewUrl": "https://example.com/media/m5_preview.jpg",
        "originalUrl": "https://example.com/media/m5.jpg", "description": "",
        "persons": [ _persons["1"] ], "events": [], "geotags": [ _geotags["g1"] ],
    },
}

_documents = {
    "d1": {
        "id": "d1", "fileName": "birth_certificate_ivan", "fileExtension": "pdf", "fileSize": 120000,
        "dateAdded": "2025-08-02", "documentType": "birth_certificate",
        "description": "Свидетельство о рождении", "downloadUrl": "https://example.com/docs/d1.pdf",
        "persons": [ _persons["1"] ], "events": [ _events["e3"] ], "geotags": []
    },
    "d2": {
        "id": "d2", "fileName": "marriage_1965", "fileExtension": "pdf", "fileSize": 220000,
        "dateAdded": "2025-08-01", "documentType": "marriage_certificate",
        "downloadUrl": "https://example.com/docs/d2.pdf",
        "persons": [ _persons["1"], _persons["2"] ], "events": [ _events["e1"] ], "geotags": []
    },
    "d3": {
        "id": "d3", "fileName": "university_diploma_elena", "fileExtension": "jpg", "fileSize": 800000,
        "dateAdded": "2025-08-03", "documentType": "diploma",
        "downloadUrl": "https://example.com/docs/d3.jpg",
        "persons": [ _persons["4"] ], "events": [ _events["e2"] ], "geotags": []
    },
    "d4": {
        "id": "d4", "fileName": "archive_extract", "fileExtension": "pdf", "fileSize": 64000,
        "dateAdded": "2025-08-03", "documentType": "archive_extract",
        "downloadUrl": "https://example.com/docs/d4.pdf",
        "persons": [ _persons["3"] ], "events": [], "geotags": [ _geotags["g1"] ]
    },
    "d5": {
        "id": "d5", "fileName": "family_tree_notes", "fileExtension": "txt", "fileSize": 4096,
        "dateAdded": "2025-08-04", "documentType": "notes",
        "downloadUrl": "https://example.com/docs/d5.txt",
        "persons": [ _persons["2"], _persons["5"] ], "events": [], "geotags": [ _geotags["g2"] ]
    },
}

def _paginate(items, limit:int, offset:int):
    return items[offset: offset + limit]

def _sort(items, key, order):
    reverse = (order == "desc")
    return sorted(items, key=key, reverse=reverse)

def _media_brief(m):
    return {
        "id": m["id"], "type": m["type"], "fileName": m["fileName"],
        "fileExtension": m["fileExtension"], "fileSize": m["fileSize"],
        "dateAdded": m["dateAdded"], "previewUrl": m["previewUrl"],
    }

def _document_brief(d):
    return {
        "id": d["id"], "fileName": d["fileName"], "fileExtension": d["fileExtension"],
        "fileSize": d["fileSize"], "dateAdded": d["dateAdded"], "documentType": d["documentType"],
    }

@app.get("/metadata/persons", tags=["metadata"])
def meta_persons():
    return list(_persons.values())

@app.get("/metadata/events", tags=["metadata"])
def meta_events():
    return list(_events.values())

@app.get("/metadata/geotags", tags=["metadata"])
def meta_geotags():
    return list(_geotags.values())

@app.get("/media", tags=["media"])
def media_list(
    search: str | None = Query(None),
    type: str | None = Query(None, pattern="^(photo|video)$"),
    personId: str | None = Query(None),
    eventId: str | None = Query(None),
    geotagId: str | None = Query(None),
    sort: str = Query("dateAdded", pattern="^(fileName|dateAdded|fileSize)$"),
    order: str = Query("desc", pattern="^(asc|desc)$"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    items = list(_media.values())
    if search:
        s = search.lower()
        items = [m for m in items if s in m["fileName"].lower() or s in m.get("description","").lower()]
    if type:
        items = [m for m in items if m["type"] == type]
    if personId:
        items = [m for m in items if any(p["id"] == personId for p in m["persons"])]
    if eventId:
        items = [m for m in items if any(e["id"] == eventId for e in m["events"])]
    if geotagId:
        items = [m for m in items if any(g["id"] == geotagId for g in m["geotags"])]

    key = (lambda x: x["fileName"]) if sort == "fileName" else (lambda x: x["fileSize"]) if sort == "fileSize" else (lambda x: x["dateAdded"])
    brief = [_media_brief(m) for m in _sort(items, key=key, order=order)]
    return {"items": _paginate(brief, limit, offset), "total": len(brief)}

@app.get("/media/{mediaId}", tags=["media"])
def media_details(mediaId: str):
    if mediaId not in _media: raise HTTPException(status_code=404, detail="Медиа не найдено")
    return _media[mediaId]

@app.post("/media", status_code=201, tags=["media"])
def media_create(body: dict = Body(...)):
    # Мок: если не передали поля — заполним дефолтами
    new_num = max(int(k[1:]) for k in _media.keys()) + 1
    new_id = f"m{new_num}"
    item = {
        "id": new_id,
        "type": body.get("type", "photo"),
        "fileName": body.get("fileName", f"new_{new_id}"),
        "fileExtension": body.get("fileExtension", "jpg"),
        "fileSize": body.get("fileSize", 1),
        "dateAdded": "2025-08-09",
        "previewUrl": f"https://example.com/media/{new_id}_preview.jpg",
        "originalUrl": f"https://example.com/media/{new_id}.jpg",
        "description": body.get("description", ""),
        "persons": body.get("persons", []),
        "events": body.get("events", []),
        "geotags": body.get("geotags", []),
    }
    _media[new_id] = item
    return item

@app.patch("/media/{mediaId}", tags=["media"])
def media_update(mediaId: str, body: dict = Body(...)):
    if mediaId not in _media: raise HTTPException(status_code=404, detail="Медиа не найдено")
    _media[mediaId].update({k:v for k,v in body.items() if k in _media[mediaId]})
    return _media[mediaId]

@app.delete("/media/{mediaId}", status_code=204, tags=["media"])
def media_delete(mediaId: str):
    if mediaId not in _media: raise HTTPException(status_code=404, detail="Медиа не найдено")
    _media.pop(mediaId)
    return Response(status_code=204)

@app.get("/documents", tags=["documents"])
def docs_list(
    search: str | None = Query(None),
    documentType: str | None = Query(None),
    personId: str | None = Query(None),
    eventId: str | None = Query(None),
    geotagId: str | None = Query(None),
    sort: str = Query("dateAdded", pattern="^(fileName|dateAdded|fileSize)$"),
    order: str = Query("desc", pattern="^(asc|desc)$"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    items = list(_documents.values())
    if search:
        s = search.lower()
        items = [d for d in items if s in d["fileName"].lower() or s in d.get("description","").lower()]
    if documentType:
        items = [d for d in items if d["documentType"] == documentType]
    if personId:
        items = [d for d in items if any(p["id"] == personId for p in d["persons"])]
    if eventId:
        items = [d for d in items if any(e["id"] == eventId for e in d["events"])]
    if geotagId:
        items = [d for d in items if any(g["id"] == geotagId for g in d["geotags"])]

    key = (lambda x: x["fileName"]) if sort == "fileName" else (lambda x: x["fileSize"]) if sort == "fileSize" else (lambda x: x["dateAdded"])
    brief = [_document_brief(d) for d in _sort(items, key=key, order=order)]
    return {"items": _paginate(brief, limit, offset), "total": len(brief)}

@app.get("/documents/{docId}", tags=["documents"])
def docs_details(docId: str):
    if docId not in _documents: raise HTTPException(status_code=404, detail="Документ не найден")
    return _documents[docId]

@app.post("/documents", status_code=201, tags=["documents"])
def docs_create(body: dict = Body(...)):
    new_num = max(int(k[1:]) for k in _documents.keys()) + 1
    new_id = f"d{new_num}"
    item = {
        "id": new_id,
        "fileName": body.get("fileName", f"new_{new_id}"),
        "fileExtension": body.get("fileExtension", "pdf"),
        "fileSize": body.get("fileSize", 1),
        "dateAdded": "2025-08-09",
        "documentType": body.get("documentType", "other"),
        "description": body.get("description", ""),
        "downloadUrl": f"https://example.com/docs/{new_id}.pdf",
        "persons": body.get("persons", []),
        "events": body.get("events", []),
        "geotags": body.get("geotags", []),
    }
    _documents[new_id] = item
    return item

@app.patch("/documents/{docId}", tags=["documents"])
def docs_update(docId: str, body: dict = Body(...)):
    if docId not in _documents: raise HTTPException(status_code=404, detail="Документ не найден")
    _documents[docId].update({k:v for k,v in body.items() if k in _documents[docId]})
    return _documents[docId]

@app.delete("/documents/{docId}", status_code=204, tags=["documents"])
def docs_delete(docId: str):
    if docId not in _documents: raise HTTPException(status_code=404, detail="Документ не найден")
    _documents.pop(docId)
    return Response(status_code=204)
