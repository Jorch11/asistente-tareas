from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import  LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Tarea


class Logueo(LoginView):
    template_name = "base/Login.html"
    field = '__all__'
    redirect_authenticated_user = True # Para redigir al usuario que ya este autenticado

    def get_success_url(self):  #Sitio al que va el usuario ya logueado
        return reverse_lazy('tareas')

class PaginaRegistro(FormView):
    template_name = 'base/registro.html'
    form_class = UserCreationForm               #este es el que se importa y esta predeterminado
    redirect_authenticated_user = True
    success_url = reverse_lazy('tareas')

    def form_valid(self, form):
        usuario = form.save()
        if usuario is not None:
            login(self.request, usuario)
        return super(PaginaRegistro,self).form_valid(form)    #devuelve lo de la instancia superior con toda la informacion

    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('tareas')
        return super(PaginaRegistro,self).get(*args,**kwargs)
class ListaPendientes(LoginRequiredMixin,ListView):
    model = Tarea
    context_object_name = 'tareas'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['tareas'] = context['tareas'].filter(usuario=self.request.user)
        context['count'] = context['tareas'].filter(completo = False).count()

        valor_buscado = self.request.GET.get('tarea-buscar') or ''
        if valor_buscado:
            context['tareas'] = context['tareas'].filter(titulo__icontains = valor_buscado)
        context['valor_buscado'] = valor_buscado
        return context


class DetalleTarea(LoginRequiredMixin,DetailView):
    model = Tarea
    context_object_name = 'tarea'
    template_name = 'base/tarea.html'


class CrearTarea(LoginRequiredMixin,CreateView):
    model = Tarea
    fields = ['titulo','descripcion','completo']
    success_url = reverse_lazy('tareas')

    def form_valid(self, form):
        form.instance.usuario = self.request.user                #Asigna instantaneamente el valor de esta instancia al usuario loggeado
        return super(CrearTarea,self).form_valid(form)

class EditarTarea(LoginRequiredMixin,UpdateView):
    model = Tarea
    fields = ['titulo','descripcion','completo']
    success_url = reverse_lazy('tareas')

class EliminarTarea(LoginRequiredMixin,DeleteView):
    model = Tarea
    context_object_name = 'tarea'
    success_url = reverse_lazy('tareas')