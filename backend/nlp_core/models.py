from django.db import models

values = [
    (-1, 'Negative'),
    (0, 'Neutral'),
    (1, 'Positive'),
]

class Film(models.Model):
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.url


class Analysis(models.Model):
    film = models.OneToOneField(Film,on_delete=models.CASCADE)

    battery = models.IntegerField(choices=values, null=True, blank=True, default=None)
    screen = models.IntegerField(choices=values, null=True, blank=True, default=None)
    memory = models.IntegerField(choices=values, null=True, blank=True, default=None)
    ram_memory = models.IntegerField(choices=values, null=True, blank=True, default=None)
    camera = models.IntegerField(choices=values, null=True, blank=True, default=None)
    performance = models.IntegerField(choices=values, null=True, blank=True, default=None)
    design = models.IntegerField(choices=values, null=True, blank=True, default=None)
    quick_charge = models.IntegerField(choices=values, null=True, blank=True, default=None)
    audio = models.IntegerField(choices=values, null=True, blank=True, default=None)
    price = models.IntegerField(choices=values, null=True, blank=True, default=None)

    def __str__(self):
        return (f"Analysis for {self.film.url} \n"
                f"Battery: {self.battery}, Screen: {self.screen}, Memory: {self.memory}, RAM Memory: {self.ram_memory}, Camera: {self.camera},"
                f" Performance: {self.performance}, Design: {self.design}, Quick Charge: {self.quick_charge}, Audio: {self.audio}, Price: {self.price}")
