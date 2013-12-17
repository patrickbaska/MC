# Create your views here.
from django.http import HttpResponse
from django.views.generic import ListView


from mc.models import Device
from mc.models import Sensor
from mc.models import SensorInput
from mc.models import SensorInputReading

#def index(request):
    #return HttpResponse("Hello World,your in the mc index")
    
class DeviceList(ListView):
	model = Device
	
class SensorList(ListView):
	model = Sensor
	
class SensorInputReadingList(ListView):
	model = SensorInputReading
	
class MarcatoInputList(ListView):
	model = SensorInput
	queryset = SensorInput.objects.filter(sensor__description__contains="77")
	template_name = "mc/detailsensorinput_list.html"	
	
class BellagioInputList(ListView):
	model = SensorInput
	queryset = SensorInput.objects.filter(sensor__description__contains="76")
	template_name = "mc/detailsensorinput_list.html"

	
	
