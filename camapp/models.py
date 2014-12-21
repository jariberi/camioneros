# -*- coding: utf-8 -*-

from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

def validar_ano(ano):
    if len(str(ano))!=4:
        raise ValidationError('Año incorrecto. Formato: 2014, 1985')
    
def validar_mes (mes):
    if mes >12 or mes < 1:
        raise ValidationError('Mes incorrecto.')
        
class Empresa(models.Model):
    nombre = models.CharField(max_length=150)
    cuit = models.CharField(max_length=13, validators=[RegexValidator(regex="\d{2}-\d{8}-\d",message="Ingrese un CUIT/CUIL válido")])

class Empleado(models.Model):
    empresa = models.ForeignKey(Empresa, editable=False)
    apellido = models.CharField(max_length=50)
    nombre = models.CharField(max_length=70)
    cuit = models.CharField(max_length=13, validators=[RegexValidator(regex="\d{2}-\d{8}-\d",message="Ingrese un CUIT/CUIL válido")])
 
class Periodo(models.Model):
    chofer = models.ForeignKey(Empleado, editable=False)
    ano = models.IntegerField(validators=[validar_ano], verbose_name="Año")
    mes = models.IntegerField(validators=[validar_mes])
            
class Viajes(models.Model):
    periodo = models.ForeignKey(Periodo, editable=False)
    fecha_salida = models.DateField()
    fecha_llegada = models.DateField()
    kms_normales_recorridos = models.DecimalField(max_digits=8, decimal_places=2)
    kms_extraordinarios_feriados = models.DecimalField(max_digits=8, decimal_places=2)
    kms_extraordinarios_1_2 = models.DecimalField(max_digits=8, decimal_places=2)
    kms_extraordinarios_1_4 = models.DecimalField(max_digits=8, decimal_places=2)
    descargas = models.DecimalField(max_digits=5, decimal_places=2)
    cruce_frontera = models.DecimalField(max_digits=5, decimal_places=2)
    provincia_salida = models.CharField(max_length=30)
    localidad_salida = models.CharField(max_length=30)
    provincia_llegada = models.CharField(max_length=30)
    localidad_llegada = models.CharField(max_length=30)
    descanso = models.CharField(max_length=1,choices=(('P','P'),('C','C'),('V','V')),blank=True, default="")
    