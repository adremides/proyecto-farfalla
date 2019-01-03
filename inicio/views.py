from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from django.template import loader
from cabina.models import Cliente, Sesion, Firma
from django.utils import timezone
from .filters import SesionFilter, ClienteSesionFilter

from django.urls import reverse
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required

# def index(request):
#     return HttpResponse("Estoy en inicio")

# --------- stub -----------
@login_required
def index(request):
    num_clientes = Cliente.objects.all().count()
    num_sesiones = Sesion.objects.all().count()
    # lista_sesiones_hoy = Sesion.objects.order_by('fecha') # Todas las sesiones
    lista_sesiones_hoy = Sesion.objects.filter(fecha=timezone.localdate())  # Sesiones de hoy
    template = loader.get_template('inicio/index.html')

    sesion_list = Sesion.objects.all()
    sesion_filter = SesionFilter(request.GET, queryset=sesion_list)

    context={'num_clientes': num_clientes,
             'num_sesiones': num_sesiones,
             'lista_sesiones_hoy': lista_sesiones_hoy}



    return HttpResponse(template.render(context, request))
# --------- stub ----------

def test(request):
    num_clientes = Cliente.objects.all().count()
    num_sesiones = Sesion.objects.all().count()
    # lista_sesiones_hoy = Sesion.objects.order_by('fecha') # Todas las sesiones
    # lista_sesiones_hoy = Sesion.objects.filter(fecha=timezone.localdate())  # Sesiones de hoy
    template = loader.get_template('inicio/test.html')

    lista_sesiones = Sesion.objects.all()

    if not request.GET: # Si esto es falso, es que fue llamado sin parámetros
        # entonces traer las sesiones del día actual
        qd = QueryDict('fecha=' + timezone.localdate().strftime('%d/%m/%Y'))
        # qd = QueryDict('fecha=23/09/2018') # Probando una fecha en particular

        # le paso el QueryDict porque si en lugar de usar SesionFilter uso lista_sesiones_hoy
        # no aparece el widget de fecha
        filtro_seiones = SesionFilter(qd, queryset=lista_sesiones)
    else:
        # sino traer la fecha que se especificó
        filtro_seiones = SesionFilter(request.GET, queryset=lista_sesiones)

    context={'num_clientes': num_clientes,
             'num_sesiones': num_sesiones,
             'filtro_sesiones': filtro_seiones}

    return HttpResponse(template.render(context, request))

def sesiones(request):
    template = loader.get_template('inicio/sesiones.html')

    lista_sesiones = Sesion.objects.all()

    filtro_seiones = ClienteSesionFilter(request.GET, queryset=lista_sesiones)

    context={'filtro_sesiones': filtro_seiones}

    return HttpResponse(template.render(context, request))