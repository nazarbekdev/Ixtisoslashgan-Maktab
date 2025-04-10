from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
import pandas as pd
from django.http import HttpResponse
from students.models import TestResult
from tests.models import Variant, Question, TestControl
from tests.serializers import VariantSerializer, QuestionSerializer
import logging

# Logger sozlamasi
logger = logging.getLogger(__name__)


class VariantListView(ListAPIView):
    permission_classes = []
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer


class QuestionFilterView(APIView):
    permission_classes = []  # Hozircha ochiq, keyin kerak bo‘lsa qo‘shishingiz mumkin

    def get(self, request, *args, **kwargs):
        # Query parametrlarni olish
        test_type_id = request.query_params.get('test_type')
        subject_id = request.query_params.get('subject')
        variant_id = request.query_params.get('variant')
        class_number = request.query_params.get('class_number')
        quarter = request.query_params.get('quarter')

        # Filtrlar uchun asosiy shartlarni tayyorlash
        control_filters = {}
        if test_type_id:
            control_filters['test_type_id'] = test_type_id
        if subject_id:
            control_filters['subject_id'] = subject_id
        if variant_id:
            control_filters['variant_id'] = variant_id

        try:
            # TestControl dan mos shartlarni olish
            test_controls = TestControl.objects.filter(**control_filters)
            if not test_controls.exists():
                logger.warning(f"TestControl topilmadi: {control_filters}")
                return Response({'error': 'TestControl shartlari topilmadi'}, status=status.HTTP_404_NOT_FOUND)

            # Har bir TestControl bo‘yicha savollarni yig‘ish
            questions = []
            for control in test_controls:
                # Question filtrlari
                question_filters = {
                    'test_type_id': control.test_type_id,
                    'subject_id': control.subject_id,
                    'variant_id': control.variant_id,
                    'question_type_id': control.question_type_id,
                    'difficulty': control.difficulty,
                }

                # Qo‘shimcha shartlar (class_number va quarter)
                if class_number:
                    question_filters['class_number'] = class_number
                if quarter and quarter in ['I chorak', 'II chorak', 'III chorak', 'IV chorak']:
                    question_filters['quarter'] = quarter

                # Savollarni filtrlab olish
                filtered_questions = Question.objects.filter(**question_filters)

                # Limit bo‘yicha cheklash
                limited_questions = filtered_questions.order_by('?')[:control.limit]
                questions.extend(limited_questions)

            if not questions:
                logger.warning(f"Savollar topilmadi: {question_filters}")
                return Response({'error': 'Savollar topilmadi'}, status=status.HTTP_404_NOT_FOUND)

            # Serializer orqali natijani qaytarish
            serializer = QuestionSerializer(questions, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"QuestionFilterView xatosi: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ExportTestResultsToExcel(APIView):
    permission_classes = []

    def get(self, request):
        # Barcha natijalarni olish
        test_results = TestResult.objects.all().prefetch_related('details')

        # Ma’lumotlarni tayyorlash
        data = []
        for test_result in test_results:
            for detail in test_result.details.all():
                name = test_result.student.first_name + ' ' + test_result.student.last_name
                data.append({
                    'Ism Familiya': name,
                    'Test Turi': test_result.test_type.name,
                    'Fan': test_result.subject.name,
                    'Variant': test_result.variant.name if test_result.variant else '-',
                    'Chorak': test_result.quarter if test_result.quarter else '-',
                    "Umumiy Natijasi": test_result.correct,
                    'Umumiy Ball': test_result.score,
                    'Savol': detail.question.text,
                    'Savol Turi': detail.question_type,  # Yangi maydon
                    'Savol Darajasi': detail.difficulty,  # Yangi maydon
                    'Student Javobi': detail.user_answer,
                    "To'g'rimi": detail.is_correct,
                    'Savol Uchun Olgan Ball': detail.score,
                })

        # Pandas DataFrame’ga aylantirish
        df = pd.DataFrame(data)

        # Excel faylini yaratish
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="test_results.xlsx"'
        df.to_excel(response, index=False)

        return response
