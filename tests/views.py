from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from tests.models import Variant, Question
from tests.serializers import VariantSerializer, QuestionSerializer


# Create your views here.
class VariantListView(ListAPIView):
    permission_classes = []
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer


class QuestionFilterView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        # Query parametrlarni olish
        test_type = request.query_params.get('test_type')
        subject = request.query_params.get('subject')
        variant = request.query_params.get('variant')
        class_number = request.query_params.get('class_number')
        quarter = request.query_params.get('quarter')

        # Filter qilish
        filters = {}
        if test_type:
            filters['test_type'] = test_type
        if subject:
            filters['subject'] = subject
        if variant:
            filters['variant'] = variant
        if class_number:
            filters['class_number'] = class_number
        if quarter and quarter in ['I chorak', 'II chorak', 'III chorak', 'IV chorak']:
            filters['quarter'] = quarter

        try:
            print(filters)  # To‘g‘ri: filters dictionary sifatida chiqariladi
            questions = Question.objects.filter(**filters)
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)