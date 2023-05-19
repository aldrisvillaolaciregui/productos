from fastapi import FastAPI,Request,Form,HTTPException
from fastapi.responses import HTMLResponse,JSONResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from database import db,Product,Category,Sale,Username

from datetime import date


from schemas import productBasemodel
from schemas import categoryBasemodel
from schemas import usernameBasemodel
from schemas import productoSales




app = FastAPI()



templates=Jinja2Templates(directory="templates")

app.mount("/static",StaticFiles(directory="static"),name="static")


@app.on_event('startup')
def startup():
    db.create_tables([Product,Category,Sale,Username])
    
    
#login

@app.get("/",response_class=HTMLResponse)
async def login(request:Request):
    username=request.cookies.get("user")
    if not username:
         return templates.TemplateResponse("login.html", {"request": request})
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/")
async def login(request:Request, username:str=Form(...), password:str=Form(...)):
    login=usernameBasemodel(username=username, password=password)
    cursor=db.cursor()
    query="SELECT password FROM Usuarios WHERE username=?"
    values=(login.username,)
    cursor.execute(query,values)
    users=cursor.fetchone()
    print(users)
    if (users is None or password != users[0]) :
       error_message="Credenciales invalidas"
       return templates.TemplateResponse("login.html",{"request":request, "error_message":error_message})
    response=RedirectResponse(url="/index")
    response.set_cookie(key="user",value=username)
    return response


@app.post("/index")
async def index(request:Request):
    username=request.cookies.get("user")
    print(username)
    if not username:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("index.html", {"request": request, "user":username})

@app.get("/index")
async def index(request:Request):
    username=request.cookies.get("user")
    if not username:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("index.html", {"request": request, "user":username})




@app.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/")
    response.delete_cookie("user")
    return response

@app.post("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/")
    response.delete_cookie("user")
    return response

#fin de login
    
    

#productos

@app.get('/listaProducto',response_class=HTMLResponse)
async def listaProducto(request: Request):
    cursor=db.cursor()
    cursor.execute('SELECT * FROM Productos')
    registros=cursor.fetchall()

    return templates.TemplateResponse("listaProducto.html", {"request": request, 'registros':registros})



@app.get('/addProducts')
async def addproducto(request:Request):
    cursor=db.cursor()
    cursor.execute("SELECT name_category FROM categorias")
    categorias=cursor.fetchall()
    #comprensión de lista
    categorias= [categoria[0] for categoria in categorias]
    return templates.TemplateResponse("addProducts.html", {"request": request, "categorias":categorias,"mensaje":''})
    


@app.post('/addProducts')
#los parametros que estan dentro de la funcion vienen del formulario
async def addProducts(request:Request,cod_product:int=Form(...), id_category:str=Form(...),nameProduct:str=Form(...),description:str=Form(...), price_purchase:int=Form(...), price_sale:int=Form(...),stock:int=Form(...)   ):
    producto=productBasemodel(cod_product=cod_product,id_category=id_category,nameProdcut=nameProduct,description=description, price_purchase=price_purchase, price_sale=price_sale,stock=stock)
    cursor=db.cursor()
    print(producto.id_category)
    query="SELECT id_category FROM Categorias where name_category=?"
    values=(producto.id_category,)
    print(query,values)
    cursor.execute(query,values)
    options=cursor.fetchall()
    options=[option[0] for  option in options]
    query2="INSERT INTO Productos (cod_product,id_category_id,nameProduct,description, price_purchase, price_sale, stock,date_creation) VALUES (?,?,?,?,?,?,?,DATE(CURRENT_TIMESTAMP))"
    values2=(producto.cod_product,options[0],producto.nameProdcut, producto.description, producto.price_purchase, producto.price_sale, producto.stock,)
    cursor.execute(query2,values2)
    print(query2,values2)
    db.commit()
    return  templates.TemplateResponse("addProducts.html", {"request": request})
    
    #despues de dar input se vuelva a rellenar el boton de opciones
    
    """
     cursor.execute(query2,values2)
sqlite3.OperationalError: incomplete input
   el error quiere decir problema de si

    """
     


@app.get('/addCategory',response_class=HTMLResponse)
async def addCategory(request:Request):
    cursor=db.cursor()
    cursor.execute('SELECT * FROM Categorias')
    categorias=cursor.fetchall()
    return templates.TemplateResponse("addCategory.html",{"request":request,'categorias':categorias})

@app.post('/addCategory')
async def addCategory(request:Request,name_category:str=Form(...)):
    category=categoryBasemodel(name_category=name_category)
    cursor=db.cursor()
    query="INSERT INTO Categorias (name_Category,date_creation) VALUES ( ?,DATE(CURRENT_TIMESTAMP))"
    values=(category.name_category,)
    cursor.execute(query,values)
    
    cursor.execute("SELECT * FROM categorias")
    categorias=cursor.fetchall()
    return templates.TemplateResponse("addCategory.html",{"request":request, "categorias":categorias})



@app.get("/ventas")
async def Ventas(request:Request):
    return templates.TemplateResponse("ventas.html", {"request": request})


@app.get("/productos")
async def get_productos(request:Request,term: str):
    cursor=db.cursor()
    cursor.execute('SELECT * FROM Productos WHERE nameProduct LIKE ?', ('%'+term+'%',))
    productos=cursor.fetchall()
    productos=[producto[2] for producto in productos]
    return JSONResponse(content=productos)

@app.post("/productos")
async def recibir_productos(request:Request, nombre: str=Form(...), cantidad: int=Form(...), precio: float=Form(...)):
    productos=productoSales(nombre=nombre, cantidad=cantidad, precio=precio)
    
    print(productos)
    
    
    # ...

    return {"message": "Productos recibidos"}


  




   
   
    
    
