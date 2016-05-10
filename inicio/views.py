
from django.shortcuts import render
from django.shortcuts import redirect

from .forms import SismoUserForm
from .models import userApp

import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import mpld3 as mpld3
import random
from string import digits, letters
from Crypto.Cipher import DES

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
		instance.contrasena=cipher.encrypt(getPassword())
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
	red=nx.Graph()
	red.clear()
	query=userApp.objects.all()
	for instance in query :
		print instance.nombre
		red.add_node(instance.nombre)
			# labels.append(instance.nombre)
	print red.number_of_nodes()
	x=red.number_of_nodes()
	y=red.number_of_nodes()
	fig=plt.figure(figsize=(12,6))
	nx.draw(red,pos=None,arrows=False,with_labels=True,node_size=200,node_color='b',edge_color='b',alpha=0.3,font_size=11,font_family="Arial")
	htmlfig=mpld3.fig_to_html(fig)
	return htmlfig

def getPassword(length=8):
    s = ''
    for i in range(length):
        s += random.choice(digits + letters)
    return s

