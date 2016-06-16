import pprint
from .models import userApp,localization
from datetime import timedelta,datetime,time,date
import munipaths # get the path data we previously grabbed
import random
import math

def rutas(fecha):
	
	usuarios=userApp.objects.all()
	allRoutesPathData = {}

	for usuario in usuarios:
    		ubicaciones=localization.objects.raw('select id,latitud,longitud from inicio_localization where usuario_id=%s and "fechaHora"::timestamp::date=%s group by id,latitud,longitud',[usuario.id,fecha]) 
        
        	pathElement = []
    		for locate in ubicaciones:
        		pathElement.append({'lon': locate.longitud, 'lat': locate.latitud})
        	print "{0}:{1}".format("pathElement",pathElement) 
        	allRoutesPathData[usuario.nombre]=[]
    		allRoutesPathData[usuario.nombre].append(pathElement) 
    		

	fo = open('munipaths.py', 'w')
	fo.write('munipaths = ' + pprint.pformat(allRoutesPathData))
	fo.close()

	rutitas=polineas()
	return rutitas

def polineas():
	COLORS = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF', '#FF00FF', '#800000', '#008000', '#000080', '#808000', '#008080', '#800080']
	fo = open('polylineJS.js', 'w')
	ruta=""
	polylineJavaScript=""
	for route in munipaths.munipaths.keys():
		routeColor = random.choice(COLORS) # choose a random color for this route's paths

		for path in munipaths.munipaths[route]:
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
