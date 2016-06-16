#!/usr/bin/python
# -*- coding: latin-1 -*-
from datetime import datetime,date,time,timedelta
from django import forms
from .models import userApp

class SismoUserForm(forms.ModelForm):
	class Meta:
		model=userApp
		fields=['nombre','apellidos','email','fechaNacimiento']
	
	def clean_fechaNacimiento(self):
		fechaNacimiento=self.cleaned_data.get('fechaNacimiento')
		anioNac=int(fechaNacimiento.year)
		anioActual=int(date.today().year)
		if  anioActual-anioNac < 18:
		#if edad < 18:
			raise forms.ValidationError('El usuario debe ser mayor de edad')
		return fechaNacimiento


class rutasFechaForm(forms.Form):
	#fecha=forms.DateField(label="Filtra por fecha:")
	choices=[(x.id, x.nombre + " " + x.apellidos) for x in userApp.objects.all()]
	choices.insert(0, ('', '----'))
	usuario=forms.ChoiceField(choices=choices,required=False)
	fecha = forms.DateField(required=False,
    widget=forms.DateInput(format=('%Y-%m-%d'), 
                               attrs={ 'placeholder':'yyyy-mm-dd'}))


