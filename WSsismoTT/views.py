from django.shortcuts import render
from django.http import HttpResponse
from inicio.models import userApp
import json
def wsLogin(request):
	usuario=request.GET['usuario']
	contrasena=request.GET['contrasena']
	try:
		queryset = userApp.objects.all().get(email=usuario,contrasena=contrasena)
		data={'estatus':'ok','usuario':queryset.email,'id':queryset.id}
		return HttpResponse(json.dumps(data), content_type="application/json")
	except (RuntimeError, TypeError, NameError):
		data={'estatus':'fallo'}
		return HttpResponse(json.dumps(data), content_type="application/json")

# Create your views here.
