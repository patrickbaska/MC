from django.db import models

# device and sensor status codes
statuss = (
        (0,'new'),
        (1,'active'),
        (2,'disabled'),
        (3,'test'),
        )

NEW = 0
ACTIVE = 1
DISABLED = 2


color_codes = (
        (0, 'green'),
        (1, 'yellow'),
        (2, 'red'),
        )


GREEN = 0
YELLOW = 1
RED = 2


class Device(models.Model):
        """
        Represents a DX250.
        """
        description = models.CharField(max_length=128, default = "(no description)")
        admin_status = models.IntegerField(choices = statuss, default=0)
        def fingerprint(self):
                "Produce fingerprint of signature"
                return self.signature # not implemented at the moment

        signature = models.CharField(max_length=2048)

        def __str__(self):
                return "{} {} ({})".format(
						self.description,
                        self.get_admin_status_display(),
                        self.fingerprint())




class Sensor(models.Model):
        """
        Represents a sensor. Sensors have globally unique codes, and therefore
        do not need to be linked to a device or bus to be uniquely identified.
        This linkage is noted in logs (and can change over time), but is not needed in this table.
        The advantage of this is that buses and devices can be reorganized without having to reflect
        the same structure in the database. It is figured out on the fly each time.

        That said, duplicate codes may leave the factory. The device_affinity field allows a device
        to be entered to help uniquely identify sensors with the same code. This always stays empty
        unless you are actually dealing with a duplicate situation.
        """
        description = models.CharField(max_length=128, default = "(no description)")
        device_affinity = models.ForeignKey(Device, null=True)
        #bus = models.IntegerField()
        code = models.IntegerField()
        admin_status = models.IntegerField(choices = statuss, default=0)

        def __str__(self):
                s = "{} {} {}".format(
                        self.code,
                        self.get_admin_status_display(),
                        #self.device_affinity,
                        self.description)
                return s

        # needs date_added

class SensorInput(models.Model):
        """
        RMU input. There are 8 per RMU.
        """
        description = models.CharField(max_length=128, default = "(no description)")
        sensor = models.ForeignKey(Sensor)
        input_num = models.IntegerField()
        # admin_status = models.IntegerField(choices = statuss, default=0)
        enabled                 = models.BooleanField(default=True)
        alarmthreshold = models.FloatField(default=0)

        def __str__(self):
                s = "{} {} {} {}".format(
                        self.sensor.code,
                        self.input_num,
                        self.enabled,
                        self.description,
                        self.alarmthreshold)
                return s


class SensorInputReading(models.Model):
        """
        Sensor measurement. This table is used for moisture analysis and does not
        include infrastructure management information.
        """
        input = models.ForeignKey(SensorInput)
        timestamp = models.DateField()
        reading = models.FloatField()

        def __str__(self):
                s = "{} {} {} {} {}".format(
                        self.input.sensor.code,
                        self.input.input_num,
                        self.timestamp,
                        self.reading,
                        self.input.alarmthreshold)
                return s




class PollLog(models.Model):
        """
        Track polling cycles. Serves as an anchor for generating reports.
        """
        begin_timestamp         = models.DateField() #poll timeframe
        end_timestamp         = models.DateField(null=True)
        # completed                 = models.BooleanField(default=False)
        # color_code = models.IntegerField(choices=color_codes, default=2) # worst
        # device_fails                = models.IntegerField(default=-1)
        # sensor_fails                = models.IntegerField(default=-1)
        # input_alarms                = models.IntegerField(default=-1)
        detail                                 = models.CharField(max_length=128, default="")
        def __str__(self):
                return "{} {}".format(self.begin_timestamp, self.detail)

class PollDeviceLog(models.Model):
        """
        A record of successful and unsuccessful device comms. One of these will
        be generated for each poll cycle for each active device.
        """                
        poll                 = models.ForeignKey(PollLog)
        device = models.ForeignKey(Device)
        timestamp = models.DateField() # when all access completed
        color_code = models.IntegerField(choices=color_codes)
        detail                 = models.CharField(max_length=128, default="")
        def __str__(self):
                return "{} {} {}".format(
                        self.device.description,
                        self.get_color_code_display(),
                        self.detail)



class PollSensorLog(models.Model):
        """
        A record of successful and unsuccessful sensor comms. One of these will
        be generated for each poll cycle for each active sensor with active inputs.
        """
        poll                 = models.ForeignKey(PollLog)
        device = models.ForeignKey(Device, null=True)
        sensor = models.ForeignKey(Sensor)
        bus = models.IntegerField(default=-1)
        timestamp = models.DateField() # when all access completed
        color_code = models.IntegerField(choices=color_codes)
        detail                 = models.CharField(max_length=128, default="")

        def __str__(self):
                return "{} {} {} {}".format(
                        self.device.description,
                        self.sensor.code,
                        self.get_color_code_display(),
                        self.detail)



