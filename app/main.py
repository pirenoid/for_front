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

from fastapi import Query, HTTPException, Body

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
    "m1": {"id":"m1","type":"photo","fileName":"grandpa","fileExtension":"jpg","fileSize":123456,"dateAdded":"2025-08-01",
           "previewUrl":"https://example.com/m1_prev.jpg","originalUrl":"https://example.com/m1.jpg",
           "description":"Дедушка в молодости.","persons":[_persons["1"],_persons["2"]],"events":[_events["e1"]],"geotags":[_geotags["g1"]]},
    "m2": {"id":"m2","type":"video","fileName":"interview","fileExtension":"mp4","fileSize":9876543,"dateAdded":"2025-08-02",
           "previewUrl":"https://example.com/m2_prev.jpg","originalUrl":"https://example.com/m2.mp4",
           "description":"Интервью с отцом.","persons":[_persons["3"]],"events":[_events["e2"]],"geotags":[_geotags["g2"]]},
    "m3": {"id":"m3","type":"photo","fileName":"mom_university","fileExtension":"png","fileSize":222222,"dateAdded":"2025-08-03",
           "previewUrl":"https://example.com/m3_prev.jpg","originalUrl":"https://example.com/m3.png",
           "description":"","persons":[_persons["4"]],"events":[_events["e2"]],"geotags":[]},
    "m4": {"id":"m4","type":"photo","fileName":"son_birth","fileExtension":"jpg","fileSize":333333,"dateAdded":"2025-08-03",
           "previewUrl":"https://example.com/m4_prev.jpg","originalUrl":"https://example.com/m4.jpg",
           "description":"","persons":[_persons["5"]],"events":[_events["e3"]],"geotags":[_geotags["g2"]]},
    "m5": {"id":"m5","type":"photo","fileName":"grandpa_award","fileExtension":"jpg","fileSize":444444,"dateAdded":"2025-08-01",
           "previewUrl":"https://example.com/m5_prev.jpg","originalUrl":"https://example.com/m5.jpg",
           "description":"","persons":[_persons["1"]],"events":[],"geotags":[_geotags["g1"]]},
}
_documents = {
    "d1":{"id":"d1","fileName":"birth_certificate_ivan","fileExtension":"pdf","fileSize":120000,"dateAdded":"2025-08-02",
          "documentType":"birth_certificate","description":"Свидетельство о рождении","downloadUrl":"https://example.com/d1.pdf",
          "persons":[_persons["1"]],"events":[_events["e3"]],"geotags":[]},
    "d2":{"id":"d2","fileName":"marriage_1965","fileExtension":"pdf","fileSize":220000,"dateAdded":"2025-08-01",
          "documentType":"marriage_certificate","downloadUrl":"https://example.com/d2.pdf",
          "persons":[_persons["1"],_persons["2"]],"events":[_events["e1"]],"geotags":[]},
    "d3":{"id":"d3","fileName":"university_diploma_elena","fileExtension":"jpg","fileSize":800000,"dateAdded":"2025-08-03",
          "documentType":"diploma","downloadUrl":"https://example.com/d3.jpg",
          "persons":[_persons["4"]],"events":[_events["e2"]],"geotags":[]},
    "d4":{"id":"d4","fileName":"archive_extract","fileExtension":"pdf","fileSize":64000,"dateAdded":"2025-08-03",
          "documentType":"archive_extract","downloadUrl":"https://example.com/d4.pdf",
          "persons":[_persons["3"]],"events":[],"geotags":[_geotags["g1"]]},
    "d5":{"id":"d5","fileName":"family_tree_notes","fileExtension":"txt","fileSize":4096,"dateAdded":"2025-08-04",
          "documentType":"notes","downloadUrl":"https://example.com/d5.txt",
          "persons":[_persons["2"],_persons["5"]],"events":[],"geotags":[_geotags["g2"]]},
}

def _paginate(items, limit:int, offset:int): return items[offset:offset+limit]
def _sort(items, key, order): return sorted(items, key=key, reverse=(order=="desc"))
def _media_brief(m): return {"id":m["id"],"type":m["type"],"fileName":m["fileName"],"fileExtension":m["fileExtension"],"fileSize":m["fileSize"],"dateAdded":m["dateAdded"],"previewUrl":m["previewUrl"]}
def _doc_brief(d): return {"id":d["id"],"fileName":d["fileName"],"fileExtension":d["fileExtension"],"fileSize":d["fileSize"],"dateAdded":d["dateAdded"],"documentType":d["documentType"]}

@app.get("/storage/metadata/persons", tags=["metadata"])
def storage_meta_persons(): return list(_persons.values())

@app.get("/storage/metadata/events", tags=["metadata"])
def storage_meta_events(): return list(_events.values())

@app.get("/storage/metadata/geotags", tags=["metadata"])
def storage_meta_geotags(): return list(_geotags.values())

@app.get("/storage/media/all", tags=["media"])
def media_all(
    limit:int=Query(25, ge=1), offset:int=Query(0, ge=0),
    sort:str=Query("dateAdded", pattern="^(fileName|dateAdded|fileSize)$"),
    order:str=Query("desc", pattern="^(asc|desc)$"),
):
    items = [_media_brief(m) for m in _media.values()]
    key = (lambda x:x["fileName"]) if sort=="fileName" else (lambda x:x["fileSize"]) if sort=="fileSize" else (lambda x:x["dateAdded"])
    items = _sort(items, key, order)
    return {"items": _paginate(items, limit, offset), "total": len(items)}

@app.get("/storage/media/persons", tags=["media"])
def media_group_by_person(
    limit:int=Query(25, ge=1), offset:int=Query(0, ge=0),
    sort:str=Query("name", pattern="^(name|count)$"),
    order:str=Query("asc", pattern="^(asc|desc)$"),
):
    groups = []
    for p in _persons.values():
        attached = [m for m in _media.values() if any(pp["id"]==p["id"] for pp in m["persons"])]
        groups.append({"person":p, "mediaCount":len(attached), "previewUrl": attached[0]["previewUrl"] if attached else None})
    key = (lambda g:(g["person"]["surname"], g["person"]["name"])) if sort=="name" else (lambda g:g["mediaCount"])
    groups = _sort(groups, key, order)
    return {"items": _paginate(groups, limit, offset), "total": len(groups)}

@app.get("/storage/media/persons/{personId}/media", tags=["media"])
def media_of_person(
    personId:str,
    limit:int=Query(25, ge=1), offset:int=Query(0, ge=0),
    type:str|None=Query(None, pattern="^(photo|video)$"),
    sort:str=Query("dateAdded", pattern="^(fileName|dateAdded|fileSize)$"),
    order:str=Query("desc", pattern="^(asc|desc)$"),
):
    if personId not in _persons: raise HTTPException(status_code=404, detail="Персона не найдена")
    items = [m for m in _media.values() if any(p["id"]==personId for p in m["persons"])]
    if type: items = [m for m in items if m["type"]==type]
    key = (lambda x:x["fileName"]) if sort=="fileName" else (lambda x:x["fileSize"]) if sort=="fileSize" else (lambda x:x["dateAdded"])
    brief = [_media_brief(m) for m in _sort(items, key, order)]
    return {"items": _paginate(brief, limit, offset), "total": len(brief)}

@app.post("/storage/media/persons/{personId}/media", tags=["media"], status_code=201)
def media_create_for_person(personId:str, body:dict=Body(...)):
    if personId not in _persons: raise HTTPException(status_code=404, detail="Персона не найдена")
    new_num = max(int(k[1:]) for k in _media.keys())+1; new_id=f"m{new_num}"
    item = {
        "id":new_id,"type":body.get("type","photo"),"fileName":body.get("fileName",f"new_{new_id}"),
        "fileExtension":body.get("fileExtension","jpg"),"fileSize":body.get("fileSize",1),
        "dateAdded":"2025-08-09","previewUrl":f"https://example.com/{new_id}_prev.jpg",
        "originalUrl":f"https://example.com/{new_id}.jpg","description":body.get("description",""),
        "persons":[_persons[personId]],"events":body.get("events",[]),"geotags":body.get("geotags",[]),
    }
    _media[new_id]=item; return item

@app.get("/storage/media/events", tags=["media"])
def media_group_by_event(
    limit:int=Query(25, ge=1), offset:int=Query(0, ge=0),
    sort:str=Query("name", pattern="^(name|count)$"),
    order:str=Query("asc", pattern="^(asc|desc)$"),
):
    groups=[]
    for e in _events.values():
        attached=[m for m in _media.values() if any(ev["id"]==e["id"] for ev in m["events"])]
        groups.append({"event":e,"mediaCount":len(attached),"previewUrl": attached[0]["previewUrl"] if attached else None})
    key=(lambda g:g["event"]["name"]) if sort=="name" else (lambda g:g["mediaCount"])
    groups=_sort(groups,key,order)
    return {"items": _paginate(groups, limit, offset), "total": len(groups)}

@app.get("/storage/media/events/{eventId}/media", tags=["media"])
def media_of_event(eventId:str,
    limit:int=Query(25, ge=1), offset:int=Query(0, ge=0),
    type:str|None=Query(None, pattern="^(photo|video)$"),
    sort:str=Query("dateAdded", pattern="^(fileName|dateAdded|fileSize)$"),
    order:str=Query("desc", pattern="^(asc|desc)$"),
):
    if eventId not in _events: raise HTTPException(status_code=404, detail="Событие не найдено")
    items=[m for m in _media.values() if any(e["id"]==eventId for e in m["events"])]
    if type: items=[m for m in items if m["type"]==type]
    key=(lambda x:x["fileName"]) if sort=="fileName" else (lambda x:x["fileSize"]) if sort=="fileSize" else (lambda x:x["dateAdded"])
    brief=[_media_brief(m) for m in _sort(items,key,order)]
    return {"items": _paginate(brief, limit, offset), "total": len(brief)}

@app.post("/storage/media/events/{eventId}/media", tags=["media"], status_code=201)
def media_create_for_event(eventId:str, body:dict=Body(...)):
    if eventId not in _events: raise HTTPException(status_code=404, detail="Событие не найдено")
    new_num=max(int(k[1:]) for k in _media.keys())+1; new_id=f"m{new_num}"
    item={ "id":new_id,"type":body.get("type","photo"),"fileName":body.get("fileName",f"new_{new_id}"),
           "fileExtension":body.get("fileExtension","jpg"),"fileSize":body.get("fileSize",1),"dateAdded":"2025-08-09",
           "previewUrl":f"https://example.com/{new_id}_prev.jpg","originalUrl":f"https://example.com/{new_id}.jpg",
           "description":body.get("description",""),"persons":body.get("persons",[]),"events":[_events[eventId]],
           "geotags":body.get("geotags",[])}
    _media[new_id]=item; return item

# ====== MEDIA: GROUP BY DATE ======
@app.get("/storage/media/dateAdded", tags=["media"])
def media_group_by_date(limit:int=Query(25, ge=1), offset:int=Query(0, ge=0),
                        sort:str=Query("date", pattern="^(date|count)$"),
                        order:str=Query("desc", pattern="^(asc|desc)$")):
    counts={}
    for m in _media.values(): counts[m["dateAdded"]] = counts.get(m["dateAdded"],0)+1
    items=[{"date":d,"mediaCount":c} for d,c in counts.items()]
    key=(lambda x:x["date"]) if sort=="date" else (lambda x:x["mediaCount"])
    items=_sort(items,key,order)
    return {"items": _paginate(items, limit, offset), "total": len(items)}

@app.get("/storage/media/dateAdded/{date}/media", tags=["media"])
def media_by_date(date:str,
    limit:int=Query(25, ge=1), offset:int=Query(0, ge=0),
    type:str|None=Query(None, pattern="^(photo|video)$"),
    sort:str=Query("dateAdded", pattern="^(fileName|dateAdded|fileSize)$"),
    order:str=Query("desc", pattern="^(asc|desc)$"),
):
    items=[m for m in _media.values() if m["dateAdded"]==date]
    if type: items=[m for m in items if m["type"]==type]
    key=(lambda x:x["fileName"]) if sort=="fileName" else (lambda x:x["fileSize"]) if sort=="fileSize" else (lambda x:x["dateAdded"])
    brief=[_media_brief(m) for m in _sort(items,key,order)]
    return {"items": _paginate(brief, limit, offset), "total": len(brief)}

# ====== MEDIA: GROUP BY GEOTAG ======
@app.get("/storage/media/geotags", tags=["media"])
def media_group_by_geotag(limit:int=Query(25, ge=1), offset:int=Query(0, ge=0),
                          sort:str=Query("name", pattern="^(name|count)$"),
                          order:str=Query("asc", pattern="^(asc|desc)$")):
    groups=[]
    for g in _geotags.values():
        attached=[m for m in _media.values() if any(gg["id"]==g["id"] for gg in m["geotags"])]
        groups.append({"geotag":g,"mediaCount":len(attached),"previewUrl": attached[0]["previewUrl"] if attached else None})
    key=(lambda x:x["geotag"]["locationName"]) if sort=="name" else (lambda x:x["mediaCount"])
    groups=_sort(groups,key,order)
    return {"items": _paginate(groups, limit, offset), "total": len(groups)}

@app.get("/storage/media/geotags/{geoId}/media", tags=["media"])
def media_of_geotag(geoId:str,
    limit:int=Query(25, ge=1), offset:int=Query(0, ge=0),
    type:str|None=Query(None, pattern="^(photo|video)$"),
    sort:str=Query("dateAdded", pattern="^(fileName|dateAdded|fileSize)$"),
    order:str=Query("desc", pattern="^(asc|desc)$"),
):
    if geoId not in _geotags: raise HTTPException(status_code=404, detail="Геометка не найдена")
    items=[m for m in _media.values() if any(g["id"]==geoId for g in m["geotags"])]
    if type: items=[m for m in items if m["type"]==type]
    key=(lambda x:x["fileName"]) if sort=="fileName" else (lambda x:x["fileSize"]) if sort=="fileSize" else (lambda x:x["dateAdded"])
    brief=[_media_brief(m) for m in _sort(items,key,order)]
    return {"items": _paginate(brief, limit, offset), "total": len(brief)}

@app.post("/storage/media/geotags/{geoId}/media", tags=["media"], status_code=201)
def media_create_for_geotag(geoId:str, body:dict=Body(...)):
    if geoId not in _geotags: raise HTTPException(status_code=404, detail="Геометка не найдена")
    new_num=max(int(k[1:]) for k in _media.keys())+1; new_id=f"m{new_num}"
    item={ "id":new_id,"type":body.get("type","photo"),"fileName":body.get("fileName",f"new_{new_id}"),
           "fileExtension":body.get("fileExtension","jpg"),"fileSize":body.get("fileSize",1),"dateAdded":"2025-08-09",
           "previewUrl":f"https://example.com/{new_id}_prev.jpg","originalUrl":f"https://example.com/{new_id}.jpg",
           "description":body.get("description",""),"persons":body.get("persons",[]),"events":body.get("events",[]),
           "geotags":[_geotags[geoId]]}
    _media[new_id]=item; return item

# ====== MEDIA: CREATE + DETAIL + UPDATE (PUT) ======
@app.post("/storage/media", tags=["media"], status_code=201)
def media_create(body:dict=Body(...)):
    new_num=max(int(k[1:]) for k in _media.keys())+1; new_id=f"m{new_num}"
    item={ "id":new_id,"type":body.get("type","photo"),"fileName":body.get("fileName",f"new_{new_id}"),
           "fileExtension":body.get("fileExtension","jpg"),"fileSize":body.get("fileSize",1),"dateAdded":"2025-08-09",
           "previewUrl":f"https://example.com/{new_id}_prev.jpg","originalUrl":f"https://example.com/{new_id}.jpg",
           "description":body.get("description",""),"persons":body.get("persons",[]),"events":body.get("events",[]),
           "geotags":body.get("geotags",[])}
    _media[new_id]=item; return item

@app.get("/storage/media/{mediaId}", tags=["media"])
def media_detail(mediaId:str):
    if mediaId not in _media: raise HTTPException(status_code=404, detail="Медиа не найдено")
    return _media[mediaId]

@app.put("/storage/media/{mediaId}", tags=["media"])
def media_update(mediaId:str, body:dict=Body(...)):
    if mediaId not in _media: raise HTTPException(status_code=404, detail="Медиа не найдено")
    _media[mediaId].update({k:v for k,v in body.items() if k in _media[mediaId]})
    return _media[mediaId]

# ================= DOCUMENTS (аналогично) =================
@app.get("/storage/documents/all", tags=["documents"])
def docs_all(limit:int=Query(25, ge=1), offset:int=Query(0, ge=0),
             sort:str=Query("dateAdded", pattern="^(fileName|dateAdded|fileSize)$"),
             order:str=Query("desc", pattern="^(asc|desc)$")):
    items=[_doc_brief(d) for d in _documents.values()]
    key=(lambda x:x["fileName"]) if sort=="fileName" else (lambda x:x["fileSize"]) if sort=="fileSize" else (lambda x:x["dateAdded"])
    items=_sort(items,key,order)
    return {"items": _paginate(items, limit, offset), "total": len(items)}

@app.get("/storage/documents/persons", tags=["documents"])
def docs_group_by_person(limit:int=Query(25, ge=1), offset:int=Query(0, ge=0),
                         sort:str=Query("name", pattern="^(name|count)$"),
                         order:str=Query("asc", pattern="^(asc|desc)$")):
    groups=[]
    for p in _persons.values():
        attached=[d for d in _documents.values() if any(pp["id"]==p["id"] for pp in d["persons"])]
        groups.append({"person":p,"documentsCount":len(attached)})
    key=(lambda g:(g["person"]["surname"],g["person"]["name"])) if sort=="name" else (lambda g:g["documentsCount"])
    groups=_sort(groups,key,order)
    return {"items": _paginate(groups, limit, offset), "total": len(groups)}

@app.get("/storage/documents/persons/{personId}/documents", tags=["documents"])
def docs_of_person(personId:str, limit:int=Query(25, ge=1), offset:int=Query(0, ge=0),
                   sort:str=Query("dateAdded", pattern="^(fileName|dateAdded|fileSize)$"),
                   order:str=Query("desc", pattern="^(asc|desc)$")):
    if personId not in _persons: raise HTTPException(status_code=404, detail="Персона не найдена")
    items=[d for d in _documents.values() if any(p["id"]==personId for p in d["persons"])]
    key=(lambda x:x["fileName"]) if sort=="fileName" else (lambda x:x["fileSize"]) if sort=="fileSize" else (lambda x:x["dateAdded"])
    brief=[_doc_brief(d) for d in _sort(items,key,order)]
    return {"items": _paginate(brief, limit, offset), "total": len(brief)}

@app.post("/storage/documents/persons/{personId}/documents", tags=["documents"], status_code=201)
def docs_create_for_person(personId:str, body:dict=Body(...)):
    if personId not in _persons: raise HTTPException(status_code=404, detail="Персона не найдена")
    new_num=max(int(k[1:]) for k in _documents.keys())+1; new_id=f"d{new_num}"
    item={"id":new_id,"fileName":body.get("fileName",f"new_{new_id}"),"fileExtension":body.get("fileExtension","pdf"),
          "fileSize":body.get("fileSize",1),"dateAdded":"2025-08-09","documentType":body.get("documentType","other"),
          "description":body.get("description",""),"downloadUrl":f"https://example.com/{new_id}.pdf",
          "persons":[_persons[personId]],"events":body.get("events",[]),"geotags":body.get("geotags",[])}
    _documents[new_id]=item; return item

@app.get("/storage/documents/events", tags=["documents"])
def docs_group_by_event(limit:int=Query(25, ge=1), offset:int=Query(0, ge=0),
                        sort:str=Query("name", pattern="^(name|count)$"),
                        order:str=Query("asc", pattern="^(asc|desc)$")):
    groups=[]
    for e in _events.values():
        attached=[d for d in _documents.values() if any(ev["id"]==e["id"] for ev in d["events"])]
        groups.append({"event":e,"documentsCount":len(attached)})
    key=(lambda g:g["event"]["name"]) if sort=="name" else (lambda g:g["documentsCount"])
    groups=_sort(groups,key,order)
    return {"items": _paginate(groups, limit, offset), "total": len(groups)}

@app.get("/storage/documents/events/{eventId}/documents", tags=["documents"])
def docs_of_event(eventId:str, limit:int=Query(25, ge=1), offset:int=Query(0, ge=0),
                  sort:str=Query("dateAdded", pattern="^(fileName|dateAdded|fileSize)$"),
                  order:str=Query("desc", pattern="^(asc|desc)$")):
    if eventId not in _events: raise HTTPException(status_code=404, detail="Событие не найдено")
    items=[d for d in _documents.values() if any(e["id"]==eventId for e in d["events"])]
    key=(lambda x:x["fileName"]) if sort=="fileName" else (lambda x:x["fileSize"]) if sort=="fileSize" else (lambda x:x["dateAdded"])
    brief=[_doc_brief(d) for d in _sort(items,key,order)]
    return {"items": _paginate(brief, limit, offset), "total": len(brief)}

@app.post("/storage/documents/events/{eventId}/documents", tags=["documents"], status_code=201)
def docs_create_for_event(eventId:str, body:dict=Body(...)):
    if eventId not in _events: raise HTTPException(status_code=404, detail="Событие не найдено")
    new_num=max(int(k[1:]) for k in _documents.keys())+1; new_id=f"d{new_num}"
    item={"id":new_id,"fileName":body.get("fileName",f"new_{new_id}"),"fileExtension":body.get("fileExtension","pdf"),
          "fileSize":body.get("fileSize",1),"dateAdded":"2025-08-09","documentType":body.get("documentType","other"),
          "description":body.get("description",""),"downloadUrl":f"https://example.com/{new_id}.pdf",
          "persons":body.get("persons",[]),"events":[_events[eventId]],"geotags":body.get("geotags",[])}
    _documents[new_id]=item; return item

@app.get("/storage/documents/dateAdded", tags=["documents"])
def docs_group_by_date(limit:int=Query(25, ge=1), offset:int=Query(0, ge=0),
                       sort:str=Query("date", pattern="^(date|count)$"),
                       order:str=Query("desc", pattern="^(asc|desc)$")):
    counts={}
    for d in _documents.values(): counts[d["dateAdded"]] = counts.get(d["dateAdded"],0)+1
    items=[{"date":dt,"documentsCount":c} for dt,c in counts.items()]
    key=(lambda x:x["date"]) if sort=="date" else (lambda x:x["documentsCount"])
    items=_sort(items,key,order)
    return {"items": _paginate(items, limit, offset), "total": len(items)}

@app.get("/storage/documents/dateAdded/{date}/documents", tags=["documents"])
def docs_by_date(date:str, limit:int=Query(25, ge=1), offset:int=Query(0, ge=0),
                 sort:str=Query("dateAdded", pattern="^(fileName|dateAdded|fileSize)$"),
                 order:str=Query("desc", pattern="^(asc|desc)$")):
    items=[d for d in _documents.values() if d["dateAdded"]==date]
    key=(lambda x:x["fileName"]) if sort=="fileName" else (lambda x:x["fileSize"]) if sort=="fileSize" else (lambda x:x["dateAdded"])
    brief=[_doc_brief(d) for d in _sort(items,key,order)]
    return {"items": _paginate(brief, limit, offset), "total": len(brief)}

@app.get("/storage/documents/geotags", tags=["documents"])
def docs_group_by_geotag(limit:int=Query(25, ge=1), offset:int=Query(0, ge=0),
                         sort:str=Query("name", pattern="^(name|count)$"),
                         order:str=Query("asc", pattern="^(asc|desc)$")):
    groups=[]
    for g in _geotags.values():
        attached=[d for d in _documents.values() if any(gg["id"]==g["id"] for gg in d["geotags"])]
        groups.append({"geotag":g,"documentsCount":len(attached)})
    key=(lambda x:x["geotag"]["locationName"]) if sort=="name" else (lambda x:x["documentsCount"])
    groups=_sort(groups,key,order)
    return {"items": _paginate(groups, limit, offset), "total": len(groups)}

@app.get("/storage/documents/geotags/{geoId}/documents", tags=["documents"])
def docs_of_geotag(geoId:str, limit:int=Query(25, ge=1), offset:int=Query(0, ge=0),
                   sort:str=Query("dateAdded", pattern="^(fileName|dateAdded|fileSize)$"),
                   order:str=Query("desc", pattern="^(asc|desc)$")):
    if geoId not in _geotags: raise HTTPException(status_code=404, detail="Геометка не найдена")
    items=[d for d in _documents.values() if any(g["id"]==geoId for g in d["geotags"])]
    key=(lambda x:x["fileName"]) if sort=="fileName" else (lambda x:x["fileSize"]) if sort=="fileSize" else (lambda x:x["dateAdded"])
    brief=[_doc_brief(d) for d in _sort(items,key,order)]
    return {"items": _paginate(brief, limit, offset), "total": len(brief)}

@app.post("/storage/documents/geotags/{geoId}/documents", tags=["documents"], status_code=201)
def docs_create_for_geotag(geoId:str, body:dict=Body(...)):
    if geoId not in _geotags: raise HTTPException(status_code=404, detail="Геометка не найдена")
    new_num=max(int(k[1:]) for k in _documents.keys())+1; new_id=f"d{new_num}"
    item={"id":new_id,"fileName":body.get("fileName",f"new_{new_id}"),"fileExtension":body.get("fileExtension","pdf"),
          "fileSize":body.get("fileSize",1),"dateAdded":"2025-08-09","documentType":body.get("documentType","other"),
          "description":body.get("description",""),"downloadUrl":f"https://example.com/{new_id}.pdf",
          "persons":body.get("persons",[]),"events":body.get("events",[]),"geotags":[_geotags[geoId]]}
    _documents[new_id]=item; return item

@app.post("/storage/documents", tags=["documents"], status_code=201)
def docs_create(body:dict=Body(...)):
    new_num=max(int(k[1:]) for k in _documents.keys())+1; new_id=f"d{new_num}"
    item={"id":new_id,"fileName":body.get("fileName",f"new_{new_id}"),"fileExtension":body.get("fileExtension","pdf"),
          "fileSize":body.get("fileSize",1),"dateAdded":"2025-08-09","documentType":body.get("documentType","other"),
          "description":body.get("description",""),"downloadUrl":f"https://example.com/{new_id}.pdf",
          "persons":body.get("persons",[]),"events":body.get("events",[]),"geotags":body.get("geotags",[])}
    _documents[new_id]=item; return item

@app.get("/storage/documents/{documentId}", tags=["documents"])
def docs_detail(documentId:str):
    if documentId not in _documents: raise HTTPException(status_code=404, detail="Документ не найден")
    return _documents[documentId]

@app.put("/storage/documents/{documentId}", tags=["documents"])
def docs_update(documentId:str, body:dict=Body(...)):
    if documentId not in _documents: raise HTTPException(status_code=404, detail="Документ не найден")
    _documents[documentId].update({k:v for k,v in body.items() if k in _documents[documentId]})
    return _documents[documentId]
