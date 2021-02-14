from django.db import models


class Ticket(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User',
                              related_name='tickets',
                              on_delete=models.CASCADE)

    def __str__(self):
        return f'Ticket: <{self.origin} -> {self.destination}>'

    class Meta:
        ordering = ['created']
