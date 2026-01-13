from django.db import models
from django.core.exceptions import ValidationError
import datetime
from django.utils import timezone
# Validadores

def mayor_de_edad(value):
    if value >= datetime.date.today() - datetime.timedelta(days=18*365):
        raise ValidationError('No se puede introducir veterinarios menores de edad')
    return value

class SexoAnimal(models.TextChoices):
    MACHO = 'M','Macho'
    HEMBRA = 'H', 'Hembra'
    DESCONOCIDO = 'D', 'Desconocido'

class Sexo(models.TextChoices):
    MASCULINO = 'M','Masculino'
    FEMENINO = 'F', 'Femenino'
    DESCONOCIDO = 'D', 'Prefiero no responder'

class Animal(models.Model):
    nombre = models.CharField(max_length=50)
    sexo = models.CharField(max_length=1, choices=SexoAnimal.choices)
    fecha_nac = models.DateField()
    recinto = models.ForeignKey('Recinto', on_delete=models.SET_NULL, null=True, related_name='animales')
    especie = models.ForeignKey('Especie', on_delete=models.SET_NULL, null=True, related_name='animales')
    foto = models.ImageField(upload_to='imagenes/animales/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.nombre}"

class Recinto(models.Model):
    nombre = models.CharField(max_length=50)
    capacidad_max = models.IntegerField()
    clima = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre}"

class Consulta(models.Model):
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    fecha_hora = models.DateTimeField()
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='consultas')
    veterinario = models.ForeignKey('Veterinario', on_delete=models.SET_NULL, null=True, related_name='consultas')

    def __str__(self):
        return f"{self.diagnostico}"
    
    def clean(self):
        if self.fecha_hora < timezone.now():
            raise ValidationError('La consulta no puede ser en el pasado tiene que ser hoy en adelante')

class Vacuna(models.Model):
    nombre = models.CharField(max_length=50)
    fabricante = models.CharField(max_length=50)
    dosis_recomendada = models.IntegerField()
    animal = models.ManyToManyField(Animal, through='VacunaAnimal', related_name='vacunas')
    
    def __str__(self):
        return f"{self.nombre}"

class VacunaAnimal(models.Model):
    vacuna = models.ForeignKey(Vacuna, on_delete=models.SET_NULL, null=True)
    animal = models.ForeignKey(Animal, on_delete=models.SET_NULL, null=True, related_name='vacunasPuestas')
    fecha_hora = models.DateTimeField(auto_now_add=True)
    lote = models.CharField(max_length=20)
    fecha_proxima_dosis = models.DateField()
    veterinario = models.ForeignKey('Veterinario', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"El animal {self.animal} se ha puesto la vacuna {self.vacuna} aplicada por el veterinario {self.veterinario}"
    
    def clean(self):
         if self.fecha_proxima_dosis <= datetime.date.today():
            raise ValidationError('La proxima dosis tiene que ser otro dia que no sea hoy')

    class Meta:
        unique_together = ('animal', 'vacuna', 'fecha_hora')

class Especie(models.Model):
    nombre_comun = models.CharField(max_length=50)
    nombre_cientifico = models.CharField(max_length=70)
    familia = models.CharField(max_length=50)
    clima_recomendado = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre_comun}({self.nombre_cientifico})"

class Veterinario(models.Model):
    nombre = models.CharField(max_length=50)
    especialidad = models.CharField(max_length=50)
    licencia = models.CharField(max_length=80)
    sexo = models.CharField(max_length=1, choices=Sexo.choices)
    fecha_nac = models.DateField(validators=[mayor_de_edad], null=True)
    incorporacion = models.DateField(auto_now_add=True)
    telefono = models.IntegerField()
    foto = models.ImageField(upload_to='imagenes/veterinarios/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} Especialidad: ({self.especialidad})"
