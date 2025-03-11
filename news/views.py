from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, News
from .serializers import CategorySerializer, NewsSerializer

# Kategoriyalar ro'yxati
class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Yangiliklar ro'yxati (qidiruv va kategoriyaga filtr)
class NewsListAPIView(ListAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        queryset = News.objects.all()
        category_id = self.request.query_params.get('category_id')
        search_query = self.request.query_params.get('search')

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        return queryset

# Mashhur yangiliklar (eng ko'p ko'rilgan 3 ta)
class PopularNewsAPIView(ListAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        return News.objects.order_by('-views')[:3]

# Yangilik detallari
class NewsDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            news = News.objects.get(pk=pk)
            news.views += 1  # Ko'rishlar sonini oshirish
            news.save()
            serializer = NewsSerializer(news)
            return Response(serializer.data)
        except News.DoesNotExist:
            return Response({'error': 'Yangilik topilmadi'}, status=404)
        