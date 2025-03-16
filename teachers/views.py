from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Material
from .serializers import MaterialSerializer

# Materiallarni ro‘yxatlash va yangi material qo‘shish uchun
class MaterialListCreateView(generics.GenericAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    parser_classes = (MultiPartParser, FormParser)  # Fayl yuklash uchun

    def get(self, request, *args, **kwargs):
        # Barcha materiallarni olish
        materials = self.get_queryset()
        serializer = self.get_serializer(materials, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Yangi material qo‘shish
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Bitta materialni olish uchun
class MaterialDetailView(generics.GenericAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    def get(self, request, pk, *args, **kwargs):
        # Bitta materialni ID bo‘yicha olish
        try:
            material = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(material)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Material.DoesNotExist:
            return Response({"error": "Material topilmadi"}, status=status.HTTP_404_NOT_FOUND)