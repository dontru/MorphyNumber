from django.db import models


class Site(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Player(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Result(models.Model):
    name = models.CharField(max_length=7)

    def __str__(self):
        return self.name


class Game(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    year = models.SmallIntegerField()
    white = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='white')
    black = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='black')
    result = models.ForeignKey(Result, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {} {} {} {}".format(self.white, self.result, self.black, self.site, self.year)
