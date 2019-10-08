from django.db import models
import datetime
import time
import uuid
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Ticket(models.Model):
    NAIROBI = 'NRB'
    NAKURU = 'NKR'
    ELDORET = 'ELD'
    KISUMU = 'KSM'
    KAKAMEGA = 'KMG'
    BUNGOMA = 'BNM'

    cities =(
        (NAIROBI, 'Nairobi'),
        (NAKURU, 'Nakuru'),
        (KAKAMEGA, 'Kakamega'),
        (ELDORET, 'Eldoret'),
        (KISUMU, 'Kisumu'),
        (BUNGOMA, 'Bungoma'),
    )
    ticket_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    phone_no = models.PositiveIntegerField()
    to = models.CharField(max_length=100,
                          choices=cities,
                          )
    origin = models.CharField(max_length=100,
                            choices=cities,
                          )
    time =(
        ('4','4am'),
        ('6', '6am'),
        ('8', '8am'),
        ('10', '10am'),
        ('12', '12 noon'),
        ('20', '8 pm'),
    )


    date_of_departure = models.DateField()

    time_of_departure = models.CharField(max_length=20,
                                         choices=time,)
    seat_no = models.PositiveIntegerField()

    price = models.PositiveIntegerField()

    def clean(self):
        if self.to == self.origin:
            raise ValidationError({'to':_('You cannot travel to your current destination')})

        if self.date_of_departure < datetime.datetime.now().date():
            raise ValidationError({'date_of_departure':_('You cannot choose a date before current date')})
        if time.strptime(self.time_of_departure, '%H').tm_hour < time.localtime().tm_hour and self.date_of_departure ==  datetime.date.today():
           raise ValidationError({'time_of_departure':_('You cannot choose a time before current time.')})

class Pricing(models.Model):
        NAIROBI = 'NRB'
        NAKURU = 'NKR'
        ELDORET = 'ELD'
        KISUMU = 'KSM'
        KAKAMEGA = 'KMG'
        BUNGOMA = 'BNM'

        cities =(
        (NAIROBI, 'Nairobi'),
        (NAKURU, 'Nakuru'),
        (KAKAMEGA, 'Kakamega'),
        (ELDORET, 'Eldoret'),
        (KISUMU, 'Kisumu'),
        (BUNGOMA, 'Bungoma'),
    )
        origin = models.CharField(max_length=100,choices=cities)


        to = models.CharField(max_length=100,choices=cities)

        price = models.PositiveIntegerField()















