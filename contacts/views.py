from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import ContactRequest
from .serializers import ContactRequestSerializer

class ContactRequestListAPIView(ListAPIView):
    queryset = ContactRequest.objects.all()
    serializer_class = ContactRequestSerializer
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        # POST so'rov - yangi ContactRequest yaratish
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    