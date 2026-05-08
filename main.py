# criar um sistema SSR

from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db, Usuario


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

@app.get("/")
def tela_inicial(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"request":request}
    )

#post - criar um usuario
@app.post("/cadastro")
def cadastrar_usuario(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    nome: str = Form(...),
    db: Session = Depends(get_db)

):
    
    usuario_existente = db.query(Usuario).filter(Usuario.email==email).first()
    if usuario_existente:
        return templates.TemplateResponse(
            request,
            "cadastro.html",
            {"request": request, "erro": "email já cadastrado."}
        )
    novo_usuario = Usuario(email=email, senha=senha, nome=nome)
    db.add(novo_usuario)
    db.commit()

    return RedirectResponse(url="/login", status_code=303)

#rota para fazer login 
@app.post("/login")
def fazer_login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    
    usuario = db.query(Usuario).filter(Usuario.email == email).first()


    if usuario is None:
        return templates.TemplateResponse(
            request,
            "login.html",
            {"request": request, "erro": "Email ou senha inválido."}
        )
    
    response = RedirectResponse(url="/poslogin", status_code=303)

    #criando cookie simples
    response.set_cookie(
        key="usuario_id",
        value=str(usuario.id)                                                         
    )

    return response
#Tela protegida 
@app.get("/poslogin")
def tela_poslogin(request: Request, db: Session = Depends(get_db)):

    #verificar id no cookie
    usuario_id = request.cookies.get("usuario_id")

    if usuario_id is None:
        return RedirectResponse(url="/login", status_code=303)
    
    user_existente = db.query(Usuario).get(int(usuario_id))

    return templates.TemplateResponse(
        request, 
        "inicio.html",
        {"request": request, "usuario": user_existente}
    )
#Logout do sistema  - Sair 
@app.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="usuario_id")
    return response