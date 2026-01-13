from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from .models import Animal, Veterinario, VacunaAnimal, Consulta
from .forms import AnimalForm, VeterinarioForm, VacunaAnimalForm, ConsultaForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, AccessMixin
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.http import HttpResponseForbidden
from django.db.models import Count, Sum
from django.contrib.auth.models import User, Group

# class soloAdmins(AccessMixin):
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated or not request.user.is_staff:
#             return self.handle_no_permission()
#         return super().dispatch(request, *args, **kwargs)

# def solo_usuarios_premium(function_view):
#     def _wrapped_view(request, *args, **kwargs):
#         if not request.user.is_authenticated or not request.user.is_staff:
#             return HttpResponseForbidden("Acceso denegado")
#         return view_func(request, *args, **kwargs)
#     return _wrapped_view

class ver_animales_veterinarios(ListView):
    model = Animal
    template_name = 'mainapp/inicio.html'
    context_object_name = 'animales'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['veterinarios'] = Veterinario.objects.all()
        return context
    
class ver_animales(PermissionRequiredMixin, ListView):
    model = Animal
    template_name = 'mainapp/ver_animales.html'
    context_object_name = 'animales'
    permission_required = 'mainapp.view_animal'


class ver_veterinarios(PermissionRequiredMixin, ListView):
    model = Veterinario
    template_name = 'mainapp/ver_veterinarios.html'
    context_object_name = 'veterinarios'
    permission_required = 'mainapp.view_veterinario'


class detalle_aniamles(DetailView):
    model = Animal
    template_name = 'mainapp/detalle_animal.html'
    context_object_name = 'animal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        num_vacunas = Animal.objects.annotate(Count('vacunasPuestas'))
        print(num_vacunas.values()[0]['vacunasPuestas__count'])
        context['num_vacunas'] = num_vacunas.values()[0]['vacunasPuestas__count']
        print(context)
        return context

class detalle_veterinario(UserPassesTestMixin,DetailView):
    model = Veterinario
    template_name = 'mainapp/detalle_veterinario.html'
    context_object_name = 'veterinario'

    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_consultas'] = Veterinario.objects.aggregate(Count('consultas'))['consultas__count']
        return context
    
class editar_animal(UpdateView):
    model = Animal
    template_name = 'mainapp/editar_animal.html'
    success_url = reverse_lazy('inicio')
    form_class = AnimalForm

class eliminar_animal(DeleteView):
    model = Animal
    template_name = 'mainapp/eliminar_animal.html'
    success_url = reverse_lazy('inicio')

class crear_animal(CreateView):
    model = Animal
    template_name = 'mainapp/editar_animal.html'
    success_url = reverse_lazy('inicio')
    form_class = AnimalForm


class editar_veterinario(UpdateView):
    model = Veterinario
    template_name = 'mainapp/editar_veterinario.html'
    success_url = reverse_lazy('inicio')
    form_class = VeterinarioForm
    

class eliminar_veterinario(DeleteView):
    model = Veterinario
    template_name = 'mainapp/eliminar_veterinario.html'
    success_url = reverse_lazy('inicio')

# class crear_veterinario(CreateView):
#     model = Veterinario
#     template_name = 'mainapp/editar_veterinario.html'
#     success_url = reverse_lazy('inicio')
#     form_class = VeterinarioForm

def crear_veterinario(request):

    if request.method == 'POST':
        form = VeterinarioForm(request.POST)
        
        if form.is_valid():
            nuevo_veterinario = form.save(commit=False)
            nuevo_veterinario.save()
            usuario = User.objects.create_user(f'{form.cleaned_data['nombre']}', f'{form.cleaned_data['nombre']}@veterinarios.es', f'{form.cleaned_data['nombre']}1234' )
            grupo_veterinario = Group.objects.get(name='Veterinario')
            usuario.groups.add(grupo_veterinario)
            print(usuario.groups)

            return redirect('ver_veterinarios')
            
    else:
        form = VeterinarioForm()
    return render(request, 'mainapp/editar_consulta.html', {'form': form})

@login_required
def ver_vacunas_animal(request, animal_pk):
    anotacion = Animal.objects.annotate(numero_vacunas=Count('vacunasPuestas'))
    agregacion = Animal.objects.aggregate(numero_vacunas=Count('vacunasPuestas'))
    animal = get_object_or_404(anotacion, pk=animal_pk)
    return render(request, 'mainapp/ver_vacunas_animal.html', {'animal':animal, 'num_vacunas':agregacion['numero_vacunas']})


def crear_vacunas_animal(request, animal_pk):
    
    animal = get_object_or_404(Animal, pk=animal_pk)

    if request.method == 'POST':
        form = VacunaAnimalForm(request.POST)

        if form.is_valid():
            nueva_vacuna = form.save(commit=False)
            nueva_vacuna.animal = animal
            nueva_vacuna.save()
            return redirect('inicio') 
    else:
        form = VacunaAnimalForm()
    

    return render(request, 'mainapp/editar_vacunas_animal.html', {'form':form})

def editar_vacunas_animal(request, animal_pk, pk):
    
    animal = get_object_or_404(Animal, pk=animal_pk)
    vacunaAnimal = get_object_or_404(VacunaAnimal, pk=pk)

    if request.method == 'POST':
        form = VacunaAnimalForm(request.POST, instance=vacunaAnimal)

        if form.is_valid():
            nueva_vacuna = form.save(commit=False)
            nueva_vacuna.animal = animal
            nueva_vacuna.save()
            return redirect('inicio') 
    else:
        form = VacunaAnimalForm(instance=vacunaAnimal)
    

    return render(request, 'mainapp/editar_vacunas_animal.html', {'form':form})


def eliminar_vacunas_animal(request, animal_pk, pk):

    vacunaAnimal = get_object_or_404(VacunaAnimal, pk=pk, animal_id=animal_pk)

    if request.method == 'POST':
        vacunaAnimal.delete()
        return redirect('inicio') 
    
    return render(request, 'mainapp/eliminar_vacunas_animal.html', {'vacuna':vacunaAnimal})


class verCnsultas(PermissionRequiredMixin,DetailView):
    model = Veterinario
    template_name = 'mainapp/ver_consultas.html'
    context_object_name = 'veterinario'
    permission_required = 'mainapp.view_consulta'

@permission_required('mainapp.create_consulta')
def crear_consulta(request, pk):
    veterinario = get_object_or_404(Veterinario, pk=pk)

    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        
        if form.is_valid():
            nueva_consulta = form.save(commit=False)
            nueva_consulta.veterinario = veterinario
            nueva_consulta.save()
            return redirect('ver_consultas', pk=pk)
            
    else:
        form = ConsultaForm()
    return render(request, 'mainapp/editar_consulta.html', {'form': form,'veterinario': veterinario })

def es_admin(user):
    return user.is_staff 

@user_passes_test(es_admin)
def editar_consulta(request, pk_veterinario, pk):
    veterinario = get_object_or_404(Veterinario, pk=pk_veterinario)
    consulta = get_object_or_404(Consulta, pk=pk)

    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        
        if form.is_valid():
            nueva_consulta = form.save(commit=False)
            nueva_consulta.veterinario = veterinario
            nueva_consulta.save()
            return redirect('ver_consultas', pk=pk_veterinario)
            
    else:
        form = ConsultaForm(instance=consulta)
    return render(request, 'mainapp/editar_consulta.html', {'form': form,'veterinario': veterinario })

def eliminar_consulta(request, pk_veterinario, pk):
    consulta = get_object_or_404(Consulta, pk=pk, veterinario_id=pk_veterinario)

    if request.method == 'POST':
        consulta.delete()
        
        return redirect('ver_consultas', pk=pk_veterinario)
       
    return render(request, 'mainapp/eliminar_consulta.html')

def estadisticas(request):
    num_consultas = Veterinario.objects.aggregate(Count('consultas'))['consultas__count']
    num_vacunas = Animal.objects.aaggregate(Count('nombre'))
    return render(request, 'mainapp/estadisticas.html', {'num_consultas':num_consultas, 'num_vacunas':num_vacunas})