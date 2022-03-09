from datetime import date
from pydoc import describe
from django.db import models
from django.utils.timezone import now
from dataclasses import dataclass

# Create your models here.

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=100, default="Car Make")
    description = models.CharField(null=True, max_length=255)

    def __str__(self):
        return "Name: " + self.name + ", " + \
               "Description: " + self.description


class CarModel(models.Model):
    CHOICES = [("SEDAN", "Sedan"), ("SUV", "SUV"), ("WAGON", "Wagon")]
    name = models.CharField(null=False, max_length=100, default="Car Model")
    car_make = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    type = models.CharField(null=True, max_length=10, choices = CHOICES, default="SUV")
    year = models.DateField()

    def __str__(self):
        return "Name: " + self.name + ", " + \
               "Car Make: " + str(self.car_make) + ", " + \
               "Dealer Id: " + str(self.dealer_id) + ", " + \
               "Type: " + self.type + ", " + \
               "Year: " + str(self.year)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
@dataclass
class CarDealer:
    id: int
    city: str
    state: str
    st: str
    address: str
    zip: str
    lat: float
    long: float
    short_name: str
    full_name: str

# <HINT> Create a plain Python class `DealerReview` to hold review data
@dataclass
class DealerReview:
#    id: int
    name: str
    dealership: int
    review:str
    purchase: bool
    purchase_date: date
    car_make: str
    car_model: str
    car_year: date
    sentiment: str