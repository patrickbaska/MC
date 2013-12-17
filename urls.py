from django.conf.urls import patterns, include, url

from mc.views import DeviceList
from mc.views import SensorList
from mc.views import SensorInputReadingList
from mc.views import MarcatoInputList
from mc.views import BellagioInputList

from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
	url(r'^devices/', DeviceList.as_view()),
	url(r'^sensors/', SensorList.as_view()),
	url(r'^marcato/', MarcatoInputList.as_view()),
	url(r'^bellagio/', BellagioInputList.as_view()),
	url(r'^admin/', include(admin.site.urls)),

	#url(r'^$', views.index, name='index')
	
)
