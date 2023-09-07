from django.db import models
from django.contrib.auth.models import User


class Tarea(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)   #Viene de otra tabla, el ondelete significa que si se borra un user sus tareas tamb
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(null =True, blank = True)  #TextField acepta textos mas largos
    completo = models.BooleanField(default=False)      #Al crearse una tarea su estado inicial será False
    creado = models.DateTimeField(auto_now_add=True)   #El argumento agrega manualmente la fecha y hora actual al ser creado

    def __str__(self):
        return self.titulo

    class Meta:                        #Clase para especificar orden personalizado y ordenar los registros
        ordering = ['completo']

