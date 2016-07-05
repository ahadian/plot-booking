from booking_api.models import Booking
from booking_api.serializers import BookingSerializer, CreateBookingSerializer, BookingDetailsSerializer, BookingListSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


class BookingList(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingListSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = BookingListSerializer(queryset, many=True)
        return Response(serializer.data)


class CreateBooking(generics.CreateAPIView):

    serializer_class = CreateBookingSerializer

    def perform_create(self, serializer):
        serializer.save()


class DestroyBooking(generics.DestroyAPIView):
    serializer_class = BookingSerializer,

    def get_object(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        booking = self.get_object(pk)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookingDetail(generics.RetrieveAPIView):
    serializer_class = BookingSerializer

    def get_object(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        booking = self.get_object(pk)
        serializer = BookingSerializer(booking)
        return Response(serializer.data)


class BookingUpdate(generics.UpdateAPIView):
    serializer_class = BookingSerializer

    def get_object(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise Http404

    def patch(self, request, pk, format=None):
        booking = self.get_object(pk)
        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
