#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import pprint
from .models import userApp,localization
from datetime import timedelta,datetime,time,date
#import munipaths # get the path data we previously grabbed
import random
import math
from string import digits, letters

def rutas(fecha):
	
	usuarios=userApp.objects.all()
	allRoutesPathData = {}

	for usuario in usuarios:
    		ubicaciones=localization.objects.raw('select id,latitud,longitud from inicio_localization where usuario_id=%s and "fechaHora"::timestamp::date=%s group by id,latitud,longitud order by id',[usuario.id,fecha]) 
        
        	pathElement = []
    		for locate in ubicaciones:
        		pathElement.append({'lon': locate.longitud, 'lat': locate.latitud})
        	print "{0}:{1}".format("pathElement",pathElement) 
        	allRoutesPathData[usuario.nombre]=[]
    		allRoutesPathData[usuario.nombre].append(pathElement) 
    		

	#fo = open('munipaths.py', 'w')
	#fo.write('munipaths = ' + pprint.pformat(allRoutesPathData))
	#fo.close()
	print allRoutesPathData
	rutitas=polineas(allRoutesPathData)
	return rutitas

def polineas(munipaths):
	COLORS = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF', '#FF00FF', '#800000', '#008000', '#000080', '#808000', '#008080', '#800080']
	fo = open('polylineJS.js', 'w')
	ruta=""
	polylineJavaScript=""
	for route in munipaths.keys():
		routeColor = random.choice(COLORS) # choose a random color for this route's paths

		for path in munipaths[route]:
			if len(path)>0:
				latlngJavaScript = []
			
				for point in path:
					latlngJavaScript.append('new google.maps.LatLng(%s, %s)' % (point['lat'], point['lon']))
				latlngJavaScript = ', '.join(latlngJavaScript)
				polylineJavaScript = """var routePath = new google.maps.Polyline({path: [%s],
					strokeColor: '%s',
					strokeOpacity: 1.0,
					strokeWeight: 2
					});
routePath.setMap(map);

""" % (latlngJavaScript, routeColor)
				ruta=ruta+"\n"+polylineJavaScript
        		fo.write(polylineJavaScript)
	fo.close()
	return ruta
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
def rutaPorUsuario(usuario,fecha):
	mapsCode=""

	ubicaciones=list(localization.objects.raw('select id,latitud,longitud from inicio_localization where usuario_id=%s and "fechaHora"::timestamp::date=%s group by id,latitud,longitud order by id',[usuario,fecha])) 
	
	if len(ubicaciones) > 0:
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
	
	return mapsCode

def messageHTML(usuario,contrasena,nombre,apellidos):
	participante=nombre+" "+apellidos
	code_HTML='''<table width="100%" style="font-family:Verdana,Arial,Helvetica,sans-serif; font-size:13px; color:#696969">
<tbody>
<tr style="background-color:#F5F5F5">
<td style="font-weight:bold; font-style:italic; font-family:Trebuchet MS; font-size:x-large; color:#87CEFA; text-align:left">
<center><img src="http://static.wixstatic.com/media/a04aa3_910be078b5ec46068b973b72dfa53c05.png_srz_88_80_85_22_0.50_1.20_0.00_png_srz" alt="UPIITA" style="width:100px"></center>
</td>
</tr>
<tr>
<td>Estimado usuario le damos la bienvenida a SMIRC. SMIRC es la contracción que se definió para nombrar al prototipo "Sistema de monitoreo de convivencia entre individuos para generar red compleja de interacción humana". 
Este estudio para investigación es parte del laboratorio de sistemas complejos que pertenece a la UPIITA y se encargará de observar la forma en que interactúa usted y los demás participantes en el mundo real para definir una red de conexiones resultado de la interacción. 
A partir de este momento y con su autorización se recolectarán la información de su geolicalización así como las señales recibidas por el micrófono que se le proporcionó.  </td>
</tr>
<tr>
<td>Para esto pedimos su apoyo para iniciar sesión diariamente en la aplicación móvil que se le ha instalado, con la siguiente información:</td>
</tr>
<tr>
<td style="font-weight:bold">Participante: {0}</td>
</tr>
<tr>
<td style="font-weight:bold">usuario: {1}</td>
</tr>
<tr>
<td style="font-weight:bold">contraseña: {2}</td>
</tr>
<tr>
<td>Si no ha instalado la aplicación en su celular, favor de solicitar al administrador le sea instalada. Cualquier duda o solicitud comunicarse a <b>smirc.cslab@gmail.com</b></td>
</tr>
<tr>
<td>Favor de conservar esta información de forma segura ya que es su medio de autorización para participar en este estudio de investigación. 
Agradecemos su apoyo. </td>
</tr><tr>
<td><br>
Atentamente el equipo del Laboratorio de Sistemas Complejos de la UPIITA.</td>
</tr>
</tbody>
</table>
<hr>
<font color="#999999" size="1" face="Verdana, Arial, Helvetica, sans-serif" style="line-height:normal">Este es un correo de carácter informativo, favor de no responderlo</font> '''.format(participante,usuario,contrasena)

	return code_HTML
