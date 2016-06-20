
from django.shortcuts import render
from django.shortcuts import redirect
from datetime import timedelta,date,datetime,time
from .forms import SismoUserForm, rutasFechaForm
from .models import userApp, localization
import networkx as nx
from django.core.mail import send_mail
import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import math
import mpld3 as mpld3
import random
from string import digits, letters
from Crypto.Cipher import DES
from mpld3 import plugins
from networkx.algorithms import approximation as approx
from dateutil import parser
import pprint
import funciones 
# Define some CSS to control our custom labels

def homeInicio(request):
	if request.user.is_authenticated() :
		# plt.savefig("Red %s.png"%datetime.today())
		figure=getNetwork()[0]
		gradored=getNetwork()[1]
		densidad=getNetwork()[2]
		n_nodos=getNetwork()[3]
		k_components=getNetwork()[4]
		conectividadentrepares=getNetwork()[5]
		conectividad_nodo=getNetwork()[6]
		coef_prom_agrup=getNetwork()[7]
		maxclique=getNetwork()[9]
		local_conec=getNetwork()[10]
		gradodecentralidad=getNetwork()[11]
		cercania=getNetwork()[8]
		intermediacion=getNetwork()[12]

		context={
		'figure':figure,
		'densidad':densidad,
		'n_nodos':n_nodos,
		'gradored':gradored,
		'coef_prom_agrup':coef_prom_agrup,
		'maxclique':maxclique,
		'conectividad_entre_pares':conectividadentrepares,
		'local_conec':local_conec,
		'k_components':k_components,
		'conectividad_nodo':conectividad_nodo,
		'gradodecentralidad':gradodecentralidad,
		'intermediacion':intermediacion,
		'cercania':cercania

		}

		return render(request, "home.html",context)
	else:
		return redirect("/login/?next=%s"%request.path)

def sismoUserInsert(request):
	form = SismoUserForm(request.POST)
	cipher = DES.new('sismoTT2')
	if form.is_valid():	
		instance = form.save(commit=False)
		instance.contrasena=funciones.getPassword()
		instance.sesionactiva=False
		instance.save()
		enviado=send_mail("Bienvenido a  SMIRC","","CSLAB",[instance.email],html_message=funciones.messageHTML(instance.email,instance.contrasena,instance.nombre,instance.apellidos))
		print enviado

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
	css = """
table
{
  border-collapse: collapse;
}
th
{
  color: #000000;
  background-color: #CEE3F6;
}
td
{
  background-color: #F2F2F2;
}
table, th, td
{
  font-family:Arial, Helvetica, sans-serif;
  border: 1px solid black;
  text-align: right;
}"""

	minutos=timedelta(seconds=30)
	red=nx.Graph()
	red.clear()
	usuarios_nodos=userApp.objects.all()
	for instance in usuarios_nodos:
		print instance.nombre
		red.add_node(instance.nombre)
		ubicaciones=localization.objects.filter(usuario_id=instance.id)
		
		for ubicacion in ubicaciones:
			fechamin=ubicacion.fechaHora - minutos
			fechamax=ubicacion.fechaHora + minutos
			t1=fechamin.strftime('%Y-%m-%d %H:%M:%S')
			t2=fechamax.strftime('%Y-%m-%d %H:%M:%S')
			print "Ubicaciones del usuario"
			print ubicacion.latitud, ubicacion.longitud, ubicacion.fechaHora
			otros_usuarios=userApp.objects.filter(id__gt=instance.id)
			for x in otros_usuarios:
				#otrasLoc=list(localization.objects.raw('select id, usuario_id,latitud,longitud,altitud,charla,fechaHora from inicio_localization where usuario_id=%s and truncate(latitud,4)=%s and truncate(longitud,4)=%s and (fechaHora>=%s and fechaHora<=%s) LIMIT 1',[x,float("%.4f" % ubicacion.latitud),float("%.4f"%ubicacion.longitud),t1,t2]))
				#Para postgres
				otrasLoc=list(localization.objects.raw('select id, usuario_id,latitud,longitud,altitud,charla,"fechaHora" from inicio_localization where usuario_id=%s and round(latitud::numeric,4)=%s and round(longitud::numeric,4)=%s and ("fechaHora">=%s and "fechaHora"<=%s) LIMIT 1',[x.id,float("%.4f" % ubicacion.latitud),float("%.4f"%ubicacion.longitud),t1,t2]))
				if len(otrasLoc)>0:
				
					locate=otrasLoc[0]
					d=funciones.betweenDots(ubicacion.latitud,locate.latitud,ubicacion.longitud,locate.longitud)*1000
					print "Distancia entre puntos: {0}".format(d)
					#print "Charla"ubicacion.charla, locate.charla
					#print locate.latitud, locate.longitud, locate.fechaHora, locate.usuario_id
					if ((ubicacion.charla==True or locate.charla==True) and (d<=2)):
						print "coincidencias"
						
						print ubicacion.charla, locate.charla
						print locate.usuario_id, locate.latitud,locate.longitud,locate.fechaHora
						coincide=userApp.objects.get(id=locate.usuario_id)
						
						if not red.has_edge(instance.nombre,coincide.nombre):
							red.add_edge(instance.nombre,coincide.nombre,weight=1)
							peso=red[instance.nombre][coincide.nombre]['weight']
							aux2=locate
						elif not(locate.latitud==aux2.latitud and locate.longitud==aux2.longitud and locate.fechaHora==aux2.fechaHora):
							red[instance.nombre][coincide.nombre]['weight']=peso+1
							print red[instance.nombre][coincide.nombre]['weight']
					
	
	fig=plt.figure(figsize=(12,6),facecolor=None, linewidth=0.0)
	#nx.draw(red,pos=None,arrows=False,with_labels=True,node_size=200,node_color='b',edge_color='r',alpha=0.3,font_size=11,font_family="Arial")
	

	labels=[]
	closs_centrality=nx.closeness_centrality(red)
	between_centrality=nx.betweenness_centrality(red)
	print between_centrality
	for i in red.nodes():
		info=nx.info(red,i)
		print info
		datos=info.split(":")
		grado=datos[2].replace("Neighbors"," ")
		print datos
		non_neighbors=nx.non_neighbors(red,i)
		print non_neighbors
		centrality=closs_centrality[i]
		valores='<table><tr><th colspan="2">{0}</th></tr><tr><td>Grado:</td><td>{1}</td></tr><tr><td>Vecinos:</td><td>{2[3]}</td></tr><tr><td>Cercania:</td><td>{3}<td></tr></table>'.format(i,grado,datos,centrality)
		labels.append(valores)
#		label = df.ix[[i], :].T
#		label.columns=['{0}'.format(i)]
#		print label
  
#    	labels.append(str(label.to_html()))
	#labels=red.nodes()
	pos=nx.spring_layout(red)
	scatter = nx.draw_networkx_nodes(red,pos,node_color='b',node_size=200,alpha=0.3)
	nx.draw_networkx_edges(red,pos,edge_color='r',alpha=0.3)
	conectividadentrepares=nx.all_pairs_node_connectivity(red)
	conectividad_nodo=approx.node_connectivity(red)
	gradored=nx.degree(red)
	densidad=nx.density(red)
	n_nodos=red.number_of_nodes()
	k_components=approx.k_components(red,densidad)
	coeficiente_agrup_prom=nx.average_clustering(red)
	max_clique=approx.max_clique(red)
	gradodecentralidad=nx.degree_centrality(red)
	dispersion=nx.dispersion(red)
	print "conectividad: {0}".format(conectividadentrepares)
	print "grado:{0}".format(gradored)
	print "densidad:{0}".format(densidad)
	print "numero de nodos:{0}".format(red.number_of_nodes())
	print "componentes K:{0}".format(k_components)
	print "centralidad :{0}".format(closs_centrality)
	print"maxClique:{0}".format(max_clique)
	print"conectividad nodo:{0}".format(conectividad_nodo)
	print "Grado de centralidad:{0}".format(gradodecentralidad)
	nodos=red.nodes()
	cont=0
	conec_local=[]
	conectividad_nodo=[]
	gradodered=""
	for nodo in nodos:
		gradodered=gradodered+ " " + "Grado de {0}:{1}\n".format(nodo,gradored[nodo])
		cont=cont+1
		if cont < len(nodos):
			local_conec=approx.local_node_connectivity(red,nodo, nodos[cont])
			conec_local.append("conectividad entre {0}->{1}:{2}".format(nodo,nodos[cont],local_conec))
			print "conectividad entre {0}->{1}:{2}".format(nodo,nodos[cont],local_conec)
	print conec_local
	print gradodered
	#nx.draw_networkx_labels(red,pos,labels=red.nodes(),font_size=11,font_family="Arial", font_color='m')
	tooltip = plugins.PointHTMLTooltip(scatter, labels, voffset=10, hoffset=10,css=css)
	mpld3.plugins.connect(fig, tooltip)
	htmlfig=mpld3.fig_to_html(fig)
	return htmlfig, gradodered, densidad, n_nodos, k_components, conectividadentrepares, conectividad_nodo, coeficiente_agrup_prom, closs_centrality, max_clique,conec_local,gradodecentralidad,between_centrality



def routesView(request):
	form=rutasFechaForm()
	inicializa=""
	usuarioid="0"
	if request.method=='POST':
		print "Entre a if de POST"
		form=rutasFechaForm(request.POST)
		cd=form['fecha'].value()
		a=parser.parse(cd)
		fecha=datetime.strftime(a,"%Y-%m-%d")
		print fecha
		usuarioid=form['usuario'].value()
		print usuarioid
	else:
		fecha=date.today().isoformat()

	if usuarioid == "0":

		print "Entre en if sin usuario"
		inicializa="""<script>
		var map;
		function initMap() {
			var mapOptions = {
						center: new google.maps.LatLng(19.4283333, -99.127777),
						zoom: 12,
						mapTypeId: google.maps.MapTypeId.ROADMAP
						};
			var map = new google.maps.Map(document.getElementById("map-canvas"),mapOptions);"""
		rutas=funciones.rutas(fecha)
		print rutas
		if not(rutas==""):
			inicializa=inicializa+"\n"+rutas+"""}
			</script>"""
		else:
			inicializa=inicializa+"""}
			</script>"""

		print inicializa
		print fecha
		context = {
		"form":form,
		"inicializa":inicializa
		}
	else:

		print "Entre en if de uusuario"
		inicializa=funciones.rutaPorUsuario(usuarioid,fecha)
		if inicializa == "":
			inicializa="""<script>
		var map;
		function initMap() {
			var mapOptions = {
						center: new google.maps.LatLng(19.4283333, -99.127777),
						zoom: 13,
						mapTypeId: google.maps.MapTypeId.ROADMAP
						};
			var map = new google.maps.Map(document.getElementById("map-canvas"),mapOptions);
			}
			</script>"""

		context = {
		"form":form,
		"inicializa":inicializa
		}
# this will be the big dictionary we store all data in
	return render(request, "mapas.html",context)


def showMap(request):

	usuario=request.GET['usuario']
	fecha=request.GET['fecha']
	instanceUser=userApp.objects.all().get(email=usuario)

	ubicaciones=list(localization.objects.raw('select id,latitud,longitud from inicio_localization where usuario_id=%s and "fechaHora"::timestamp::date=%s group by id,latitud,longitud order by id',[instanceUser.id,fecha])) 
	
	mapsCode="""
	<script>
		var map;
      	function initMap() {
        	var mapOptions = {
          				center: new google.maps.LatLng(%s, %s),
          				zoom: 15,
          				mapTypeId: google.maps.MapTypeId.ROADMAP
        			};
        	var map = new google.maps.Map(document.getElementById("map-canvas"),mapOptions);
					"""%(ubicaciones[0].latitud,ubicaciones[0].longitud)
	
	pathElement = []
	for locate in ubicaciones:
		pathElement.append('new google.maps.LatLng(%s, %s)' % (locate.latitud, locate.longitud))
	
	pathElement = ', '.join(pathElement)
	polylineJavaScript = """var routePath = new google.maps.Polyline({path: [%s],
					strokeColor: '#FA5882',
					strokeOpacity: 1.0,
					strokeWeight: 2
					});
routePath.setMap(map);""" % (pathElement)
	
	mapsCode= mapsCode + "\n"+polylineJavaScript +"""
	}
	</script>"""
	print mapsCode

	return render(request,"RutasMaps.html",{'instancia':mapsCode})
