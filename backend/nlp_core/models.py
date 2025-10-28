from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Film(models.Model):
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.url


class Analysis(models.Model):
    film = models.OneToOneField(Film, on_delete=models.CASCADE)

    battery = models.FloatField(validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)], null=True, blank=True, default=None)
    screen = models.FloatField(validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)], null=True, blank=True, default=None)
    memory = models.FloatField(validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)], null=True, blank=True, default=None)
    ram_memory = models.FloatField(validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)], null=True, blank=True, default=None)
    camera = models.FloatField(validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)], null=True, blank=True, default=None)
    performance = models.FloatField(validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)], null=True, blank=True, default=None)
    design = models.FloatField(validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)], null=True, blank=True, default=None)
    quick_charge = models.FloatField(validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)], null=True, blank=True, default=None)
    audio = models.FloatField(validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)], null=True, blank=True, default=None)
    price = models.FloatField(validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)], null=True, blank=True, default=None)

    def __str__(self):
        return (f"Analysis for {self.film.url} \n"
                f"Battery: {self.battery}, Screen: {self.screen}, Memory: {self.memory}, RAM Memory: {self.ram_memory}, Camera: {self.camera},"
                f" Performance: {self.performance}, Design: {self.design}, Quick Charge: {self.quick_charge}, Audio: {self.audio}, Price: {self.price}")
