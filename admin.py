from django.contrib import admin
from mc.models import Device

from mc.models import Sensor

from mc.models import SensorInput

from mc.models import SensorInputReading

from mc.models import PollLog

from mc.models import PollDeviceLog

from mc.models import PollSensorLog

admin.site.register(Device)

admin.site.register(Sensor)

admin.site.register(SensorInput)

admin.site.register(SensorInputReading)

admin.site.register(PollLog)

admin.site.register(PollDeviceLog)

admin.site.register(PollSensorLog)
