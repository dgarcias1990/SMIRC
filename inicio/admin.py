from django.contrib import admin

# Register your models here.
from .models import userApp,localization
from .forms import SismoUserForm
#admin.site.register(MasterUsers)
#admin.site.register(SismoUser)
#admin.site.register(ubicacion)

class SismoUserAdmin(admin.ModelAdmin):
	list_display=["__unicode__","email","fechaNacimiento","fechaAlta","lastLogin"]
	search_fields=["nombre","apellidos"]
	#class meta:
	#	model=userApp
	form=SismoUserForm
admin.site.register(userApp,SismoUserAdmin)


class ubicacionAdmin(admin.ModelAdmin):
	list_display=["__unicode__","usuario","latitud","longitud","fechaHora"]
	class meta:
		model=localization

admin.site.register(localization,ubicacionAdmin)		