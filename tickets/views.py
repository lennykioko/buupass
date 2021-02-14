from django.http import Http404
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.utils import jwt_decode_handler  # noqa

from tickets.models import Ticket
from tickets.serializers import TicketSerializer


class TicketList(APIView):
    """
    List all your tickets, or create a new ticket.
    """
    permission_classes = [IsAuthenticated]

    def get_token_id(self, request):
        decoded_token = jwt_decode_handler(bytes(str(request.auth), 'utf-8'))
        user_id = decoded_token['user_id']

        return user_id

    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def is_admin_user(self, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

        return user.is_superuser

    def get(self, request, format=None):
        user_id = self.get_token_id(request)

        tickets = Ticket.objects.filter(owner__id=user_id)

        # Only admins can view all tickets
        if self.is_admin_user(user_id):
            tickets = Ticket.objects.all()

        serializer = TicketSerializer(tickets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        user_id = self.get_token_id(request)

        user = self.get_user(user_id)
        serializer = TicketSerializer(data=request.data,
                                      context={'user': user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketDetail(APIView):
    """
    Retrieve, update or delete a ticket instance.
    """
    permission_classes = [IsAuthenticated]

    def get_token_id(self, request):
        decoded_token = jwt_decode_handler(bytes(str(request.auth), 'utf-8'))
        user_id = decoded_token['user_id']

        return user_id

    def is_admin_user(self, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

        return user.is_superuser

    def get_object(self, pk, owner_id):
        try:
            return Ticket.objects.get(pk=pk, owner_id=owner_id)
        except Ticket.DoesNotExist:
            raise Http404

    def get_object_admin(self, pk):
        try:
            return Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user_id = self.get_token_id(request)

        ticket = self.get_object(pk, user_id)

        if self.is_admin_user(user_id):
            ticket = self.get_object_admin(pk)

        if ticket:
            serializer = TicketSerializer(ticket)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        user_id = self.get_token_id(request)

        ticket = self.get_object(pk, user_id)

        if self.is_admin_user(user_id):
            ticket = self.get_object_admin(pk)

        if ticket:
            serializer = TicketSerializer(ticket, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user_id = self.get_token_id(request)

        ticket = self.get_object(pk, user_id)

        if self.is_admin_user(user_id):
            ticket = self.get_object_admin(pk)

        if ticket:
            ticket.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Unauthorised request"}, status=status.HTTP_400_BAD_REQUEST)  # noqa e501
