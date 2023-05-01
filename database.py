from peewee import Model,CharField,IntegerField,FloatField,DateTimeField
from peewee import *
import sqlite3

from datetime import datetime,date

db=SqliteDatabase('system.db')

class Category(Model):
    id_category=PrimaryKeyField()
    name_category=CharField(unique=True)
    date_creation=DateTimeField(default=date.today)

    class Meta():
        database=db
        table_name='Categorias'

class Product(Model):
    cod_prduct=PrimaryKeyField()
    id_category=ForeignKeyField(Category)
    nameProduct=CharField(unique=True)
    description=CharField()
    price_purchase=FloatField()
    price_sale=FloatField()
    stock=IntegerField()
    date_creation=DateTimeField(default=date.today)
    
    
    class Meta:
        database=db
        table_name='Productos'
        
        

class Sale(Model):
    num_fact=PrimaryKeyField()
    cod_product=ForeignKeyField(Product)
    quantity=IntegerField()
    total_sale=FloatField()
    date_sale=DateTimeField(default=date.today)
    
    
    class Meta():
        database=db
        table_name='Ventas'
        
        

class Username(Model):
    username=IntegerField()
    password=IntegerField()
    
    class Meta():
        database=db
        table_name='Usuarios'
        
  