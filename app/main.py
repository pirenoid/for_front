from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from gedcom.parser import Parser
from gedcom.element.individual import IndividualElement
from gedcom.element.family import FamilyElement
from typing import Dict, List, Optional
import tempfile
import os
import uuid
from datetime import datetime

app = FastAPI()
gedcom_storage = {}



@app.post("/")
async def upload_gedcom_file():

        return {'response': 'hello'}
