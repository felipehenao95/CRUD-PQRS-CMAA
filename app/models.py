import os
from django.db import models
from django.utils import timezone

# Create your models here.


class Peticionarios(models.Model):
    ciudades = (
        ('Bogotá D.C.','Bogotá D.C.'),
        ('Funza', 'Funza')
    )
    localidades = (
        ('Barrios Unidos', 'Barrios Unidos'),
        ('Usaquén', 'Usaquén'),
        ('Fontibón', 'Fontibón'),
        ('Engativa', 'Engativa'),
        ('Teusaquillo', 'Teusaquillo'),
        ('Funza', 'Funza'),
        ('Suba', 'Suba'),
        ('Kennedy', 'Kennedy'),
        ('Bosa', 'Bosa'),
        ('Ciudad Bolivar', 'Ciudad Bolivar'),
        ('Soacha', 'Soacha'),
    )

    tipos_dps = (
        ('Queja','Queja'),
        ('Solicitud', 'Solicitud')
    )
    temas_dps = (
        ('Ruido','Ruido'),
        ('Altitud','Altitud'),
        ('Rutas','Rutas'),
        ('Ruido, rutas y altitud','Ruido, rutas y altitud'),
        ('Insonorizacion','Insonorizacion'),
        ('Vibraciones','Vibraciones'),
        ('Solicitud Información','Solicitud Información'),
        ('Eventos especificos','Eventos especificos'),
        ('Otros','Otros'),
    )
    
    fecha_llegada = models.DateField()
    fecha_entrega = models.DateField(null=True, blank=True)
    fecha_radicado = models.DateField(null=True, blank=True)
    nombre=models.CharField(max_length =100)
    radicado=models.CharField(max_length =500, blank=True)
    correo=models.EmailField(max_length =254, blank=True)
    direccion=models.CharField(max_length =200, blank=True)
    latitud=models.CharField(max_length =100, blank=True)
    longitud=models.CharField(max_length =100, blank=True)
    ciudad = models.CharField(max_length=50, choices=ciudades, blank=True)
    localidad = models.CharField(max_length=50, choices=localidades, blank=True)
    barrio=models.CharField(max_length =50, blank=True)
    tipo_dp = models.CharField(max_length=50, choices=tipos_dps, blank=True)
    tema_dp = models.CharField(max_length=50, choices=temas_dps, blank=True)
    asunto = models.TextField(blank= True, max_length = 5000)
    peticion = models.TextField(blank= True, max_length = 5000)
    enviada  = models.BooleanField(default=False)
    enviada_aerocivil  = models.BooleanField(default=False)
    enviada_revision  = models.BooleanField(default=False)
    radicado_salida=models.CharField(max_length =500, blank=True)
    fecha_salida = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table ='peticionario'
    
    def __str__(self):
        return f'{self.nombre} - {self.fecha_llegada}' 

def ruta_archivo(instance, filename):
    # Obtener el nombre del peticionario
    nombre_peticionario = instance.peticionario.nombre.replace(' ', '_')
    # Obtener la fecha de llegada
    fecha_llegada = instance.peticionario.fecha_llegada.strftime('%Y-%m-%d')
    # Construir la ruta del archivo utilizando el nombre del peticionario y la fecha de llegada
    return os.path.join('documents', f'{nombre_peticionario} {fecha_llegada}', filename)


class Documents(models.Model):
    archivo = models.FileField(upload_to=ruta_archivo)
    peticionario = models.ForeignKey(Peticionarios, on_delete=models.CASCADE)
    def __str__(self):
        return f'DP - {self.peticionario.nombre} / {self.archivo}'


class RtasFinales(models.Model):
    rta = models.FileField(upload_to='rtas/')
    peticionario = models.ForeignKey(Peticionarios, on_delete=models.CASCADE)
    def __str__(self):
        return f'RTA - {self.peticionario.nombre} / {self.rta}'
      