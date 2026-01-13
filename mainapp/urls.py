from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', ver_animales_veterinarios.as_view(), name='inicio'),

    path('detalle_animal/<int:pk>', detalle_aniamles.as_view(), name='detalle_animal'),
    path('detalle_veterinario/<int:pk>',  detalle_veterinario.as_view(), name='detalle_veterinario'),
    path('ver_animales', ver_animales.as_view(), name='ver_animales'),
    path('ver_veterinarios', ver_veterinarios.as_view(), name='ver_veterinarios'),

    path('editar_animal/<int:pk>', editar_animal.as_view(), name='editar_animal'),
    path('eliminar_animal/<int:pk>', eliminar_animal.as_view(), name='eliminar_animal'),
    path('crear_animal', crear_animal.as_view(), name='crear_animal'),

    path('editar_veterinario/<int:pk>', editar_veterinario.as_view(), name='editar_veterinario'),
    path('eliminar_veterinario/<int:pk>', eliminar_veterinario.as_view(), name='eliminar_veterinario'),
    path('crear_veterinario', crear_veterinario, name='crear_veterinario'),

    path('animal/<int:animal_pk>/ver_vacunas/', ver_vacunas_animal  , name='ver_vacunas'),
    path('animal/<int:animal_pk>/crear_vacunas_animal', crear_vacunas_animal, name='crear_vacunas_animal'),
    path('animal/<int:animal_pk>/eliminar_vacunas_animal/<int:pk>', eliminar_vacunas_animal, name='eliminar_vacunas_animal'),
    path('animal/<int:animal_pk>/editar_vacunas_animal/<int:pk>', editar_vacunas_animal, name='editar_vacunas_animal'),

    path('<int:pk>/ver_consultas', verCnsultas.as_view()  , name='ver_consultas'),
    path('<int:pk>/consulta/crear', crear_consulta, name='crear_consulta'),
    path('<int:pk_veterinario>/consulta/editar/<int:pk>', editar_consulta, name='editar_consulta'),
    path('<int:pk_veterinario>/consulta/eliminar/<int:pk>', eliminar_consulta, name='eliminar_consulta'),

    path('estadisticas/', estadisticas, name='estadisticas')


]

