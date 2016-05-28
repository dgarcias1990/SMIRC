from django.db import models
from django.utils import timezone

# Create your models here.
		

class userApp(models.Model):
	nombre=models.CharField(max_length=200,blank=False)
	apellidos=models.CharField(max_length=200,blank=False)
	fechaNacimiento=models.DateField(verbose_name='Fecha Nacimiento',null=False)
	email=models.EmailField(blank=False, unique=True,verbose_name='E-mail')
	contrasena=models.CharField(max_length=300)
	fechaAlta=models.DateTimeField(auto_now_add=True)
	lastLogin=models.DateTimeField(auto_now_add=True, blank=True)
	sesionactiva=models.BooleanField()
	class Meta:
		verbose_name_plural="Participantes"
		ordering=["nombre"]

	def __unicode__(self):
		return '%s %s' % (self.nombre, self.apellidos)

class localization(models.Model):
	usuario=models.ForeignKey(userApp,on_delete=models.CASCADE,)
	latitud=models.FloatField()
	longitud=models.FloatField()
	altitud=models.FloatField()
	charla=models.BooleanField()
	fechaHora=models.DateTimeField()

	class Meta:
		verbose_name_plural="Ubicaciones"

	def __unicode__(self):
		return self.usuario


	
