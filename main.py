# criar um sistema SSR

from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session


app = FastAPI(title="Sistema de login simples")

#roda o codigo
# python -m uvicorn main:app --reload 

templates = Jinja2Templates(directory="templates")
# Rota - metodo HHTP (get, post)

@app.get("/cadastro")
def tela_cadastro(request: Request):
    return templates.TemplateResponse(
        request,
        "cadastro.html",
        {"request":request}
    )

@app.get("/login")
def tela_login(request: Request):
    return templates.TemplateResponse(
        request,
        "login.html",
        {"request":request}
    )
