from django.contrib.auth.models import User
from rest_framework import serializers

from tickets.models import Ticket


class UserSerializer(serializers.ModelSerializer):
    tickets = serializers.PrimaryKeyRelatedField(many=True, queryset=Ticket.objects.all())  # noqa E501

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'tickets']


class TicketSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        owner = self.context.get('user')
        if owner:
            ticket = Ticket.objects.create(owner=owner, **validated_data)
            return ticket

    class Meta:
        model = Ticket
        fields = ['id', 'created', 'origin', 'destination']
