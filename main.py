from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import time

USERNAME="jawad"
PASSWORD="admin123"
TOKEN="tempToken"
isLoggedIn=False

app=FastAPI()

class Logging(BaseModel):
    username:str
    password:str

@app.middleware("http")
async def authenticator(request:Request,call_next):
    if request.url.path in ['/','/login','logout']:
        return await call_next(request)
    token=request.headers.get('x-token')
    if token==TOKEN and isLoggedIn==True:
        return await call_next(request)
    else:
        return JSONResponse(
            status_code=401,
            content={
                "error":"Not Authorized"
            }
        )
    
@app.middleware('http')
async def logger(request:Request,call_next):
    print('Request Incoming')
    response=await call_next(request)
    print('Response Incoming')
    return response

@app.post('/login')
def ToLogin(data:Logging):
    
    if data.username==USERNAME and data.password==PASSWORD:
        global isLoggedIn
        isLoggedIn=True
        return {
            "message":"Login Success",
            "token":TOKEN
        }
    else:
        return JSONResponse(
            status_code=401,
            content={
                "error":"Login Failed due to Wrong Credentials"
            }
        )


@app.post('/logout')
def logout():
    global isLoggedIn
    isLoggedIn=False
    return {
        "message":"Logout Success"
    }



class singleList(BaseModel):
    id:int
    Heading:str
    note:str

lists:List[singleList]=[]

@app.get("/")
def mainHomePage():
    return {"message":"Welcome to TDL main page"}

@app.get("/lists")
def getAllNotes():
    return lists

@app.get("/lists/{list_id}")
def getDesiredNote(list_id:int):
    for listi in lists:
        if listi.id==list_id:
            return listi
    return {"error":"desired list not found"}


@app.post("/lists")
def addNewList(list:singleList):
    for listi in lists:
        if list.id == listi.id:
            return {"error":"ID already exists"}
    

    lists.append(list)
    return {"message":"one list added"}

@app.put("/lists/{list_id}")
def updateExistingNote(list_id:int,list:singleList):
    for index,listi in enumerate(lists):
        if listi.id==list_id:
            lists[index]=list
            return {"message":"List Updated"}
        
    return {"error":"list with specified id not found"}

@app.delete("/lists/{list_id}")
def deleteAList(list_id:int):
    for index,listi in enumerate(lists):
        if listi.id==list_id:
            lists.pop(index)
            return {"message":"list deleted"}
        
    return {"error":"list not found"}

@app.delete("/lists")
def deleteAllLists():
    if len(lists)==0:
        return {"error":"no list found"}
    else:
        lists.clear()
        return {"message":"All lists deleted"}

    

