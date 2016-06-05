
from django.shortcuts import render
from django.shortcuts import redirect
from datetime import timedelta
from .forms import SismoUserForm
from .models import userApp, localization
from django.db.models import Q
import networkx as nx
import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import math
import mpld3 as mpld3
import random
from string import digits, letters
from Crypto.Cipher import DES
from django.db.models import Count

def homeInicio(request):
	if request.user.is_authenticated() :
		# plt.savefig("Red %s.png"%datetime.today())
		figure=getNetwork()
		return render(request, "home.html",{"figure":figure})
	else:
		return redirect("/login/?next=%s"%request.path)

def sismoUserInsert(request):
	form = SismoUserForm(request.POST)
	cipher = DES.new('sismoTT2')
	if form.is_valid():	
		instance = form.save(commit=False)
		instance.contrasena=getPassword()
		instance.sesionactiva=False
		instance.save()
	context = {
	"form":form,
	}
	if request.user.is_authenticated() and request.user.is_staff:
		queryset = userApp.objects.all().order_by('fechaAlta') #.filter(full_name__iexact="Justin")
		#print(SignUp.objects.all().order_by('-timestamp').filter(full_name__iexact="Justin").count())
		context = {
		"form":form,
		"queryset": queryset,
		}
	return render(request,'forms.html',context)
	
def getNetwork():
	minutos=timedelta(seconds=30)
	red=nx.Graph()
	red.clear()
	usuarios_nodos=userApp.objects.all()
	for instance in usuarios_nodos :
		print instance.nombre
		red.add_node(instance.nombre)
		#ubicaciones=localization.objects.raw('select id, usuario_id,latitud,longitud,altitud,charla,fechaHora from inicio_localization where usuario_id=%s',[instance.id])
		#ubicaciones=localization.objects.filter(instance.id)
		ubicaciones=localization.objects.filter(usuario_id=instance.id)
		for ubicacion in ubicaciones:
			fechamin=ubicacion.fechaHora - minutos
			fechamax=ubicacion.fechaHora + minutos
			t1=fechamin.strftime('%Y-%m-%d %H:%M:%S')
			t2=fechamax.strftime('%Y-%m-%d %H:%M:%S')
			print "Ubicaciones del usuario"
			print ubicacion.latitud, ubicacion.longitud, ubicacion.fechaHora
			start=instance.id+1
			for x in range(start,len(usuarios_nodos)+1):
				#otrasLoc=list(localization.objects.raw('select id, usuario_id,latitud,longitud,altitud,charla,fechaHora from inicio_localization where usuario_id=%s and truncate(latitud,4)=%s and truncate(longitud,4)=%s and (fechaHora>=%s and fechaHora<=%s) LIMIT 1',[x,float("%.4f" % ubicacion.latitud),float("%.4f"%ubicacion.longitud),t1,t2]))
				#Para postgres
				otrasLoc=list(localization.objects.raw('select id, usuario_id,latitud,longitud,altitud,charla,"fechaHora" from inicio_localization where usuario_id=%s and round(latitud::numeric,4)=%s and round(longitud::numeric,4)=%s and ("fechaHora">=%s and "fechaHora"<=%s) LIMIT 1',[x,float("%.4f" % ubicacion.latitud),float("%.4f"%ubicacion.longitud),t1,t2]))
				if len(otrasLoc)>0:
				#print otrasLoc
					print len(otrasLoc)
					locate=otrasLoc[0]
					d=betweenDots(ubicacion.latitud,locate.latitud,ubicacion.longitud,locate.longitud)*1000
					print "Distancia entre puntos"
					print d
					print ubicacion.charla, locate.charla
					#print locate.latitud, locate.longitud, locate.fechaHora, locate.usuario_id
					if ((ubicacion.charla==True and locate.charla==True) and (d<=2)):
						print "coincidencias"
						print locate.usuario_id, locate.latitud,locate.longitud,locate.fechaHora
						coincide=userApp.objects.get(id=locate.usuario_id)
						
						if not red.has_edge(instance.nombre,coincide.nombre):
							red.add_edge(instance.nombre,coincide.nombre,weight=1)
							peso=red[instance.nombre][coincide.nombre]['weight']
							aux2=locate
						elif not(locate.latitud==aux2.latitud and locate.longitud==aux2.longitud and locate.fechaHora==aux2.fechaHora):
							red[instance.nombre][coincide.nombre]['weight']=peso+1
							print red[instance.nombre][coincide.nombre]['weight']
					#instancia=coincide[0]
					#nombre=userApp.objects.get(id=coincide.usuario_id)
					#red.add_edge(instance.nombre,nombre.nombre)
	# labels.append(instance.nombre)
	print red.number_of_nodes()
	fig=plt.figure(figsize=(12,6))
	nx.draw(red,pos=None,arrows=False,with_labels=True,node_size=200,node_color='b',edge_color='r',alpha=0.3,font_size=11,font_family="Arial")
	htmlfig=mpld3.fig_to_html(fig)
	return htmlfig

def getPassword(length=8):
    s = ''
    for i in range(length):
        s += random.choice(digits + letters)
    return s
def betweenDots(lat1,lat2,long1,long2):
	R=6378.137
	dlat=(lat1-lat2)*math.pi/180
	dlong=(long1-long2)*math.pi/180
	a=math.sin(dlat/2)*math.sin(dlat/2)+math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlong/2)*math.sin(dlong/2)
	c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
	d=R*c
	return d

	
