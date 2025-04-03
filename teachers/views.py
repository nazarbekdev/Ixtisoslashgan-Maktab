from rest_framework import generics, status
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Material, Test
from students.models import TestType
from tests.models import Question, QuestionType, QuestionDifficulty, Variant
from .serializers import MaterialSerializer, TeacherSerializer, MaterialNameSerializer, TestSerializer
from django.core.files.storage import default_storage
import pandas as pd


# O‘qituvchi profilini olish va o‘zgartirish
class TeacherProfileAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def get(self, request):
        try:
            user = request.user
            if user.role != 'teacher':
                return Response({'error': 'Faqat o‘qituvchilar uchun'}, status=status.HTTP_403_FORBIDDEN)
            serializer = TeacherSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        try:
            user = request.user
            if user.role != 'teacher':
                return Response({'error': 'Faqat o‘qituvchilar uchun'}, status=status.HTTP_403_FORBIDDEN)

            serializer = TeacherSerializer(user, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Materiallarni ro‘yxatlash va yangi material qo‘shish uchun


class MaterialListCreateView(generics.GenericAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        # Barcha materiallarni olish
        materials = self.get_queryset()
        serializer = self.get_serializer(materials, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Yangi material qo‘shish
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            material = serializer.save()  # Materialni saqlaymiz, test_file ham saqlanadi

            # Agar test_file mavjud bo‘lsa, savollarni o‘qib, Question modeliga saqlaymiz
            if 'test_file' in request.FILES:
                try:
                    # Faylni vaqtincha saqlash
                    file_path = default_storage.save('temp/test_file.xlsx', request.FILES['test_file'])
                    file_full_path = default_storage.path(file_path)

                    # Excel faylni o‘qish
                    df = pd.read_excel(file_full_path)

                    # Savol darajasini moslashtirish uchun mapping
                    difficulty_mapping = {
                        'B': QuestionDifficulty.objects.get(name='B'),
                        'Q': QuestionDifficulty.objects.get(name='Q'),
                        'M': QuestionDifficulty.objects.get(name='M')
                    }

                    # Savol turini moslashtirish uchun mapping
                    question_type_mapping = {
                        'ochiq': QuestionType.objects.get(name='ochiq'),
                        'yopiq': QuestionType.objects.get(name='yopiq')
                    }

                    # Test turi sifatida "Fanga oid" ni olish
                    test_type = TestType.objects.get(name='Fanga oid')

                    # Har bir qatorni o‘qib, Question modeliga saqlash
                    for index, row in df.iterrows():
                        # Savol darajasini moslashtirish
                        difficulty_name = row['Savol darajasi']
                        if difficulty_name not in difficulty_mapping:
                            return Response({'error': f'Noto‘g‘ri savol darajasi: {difficulty_name}'}, status=status.HTTP_400_BAD_REQUEST)
                        difficulty = difficulty_mapping[difficulty_name]

                        # Savol turini moslashtirish
                        question_type_name = row['Savol turi'].lower()
                        if question_type_name not in question_type_mapping:
                            return Response({'error': f'Noto‘g‘ri savol turi: {question_type_name}'}, status=status.HTTP_400_BAD_REQUEST)
                        question_type = question_type_mapping[question_type_name]

                        # Variantni olish
                        variant = Variant.objects.get(id=row['Variant'])
                        print('material', material.class_number)
                        # Question obyektini yaratish
                        Question.objects.create(
                            material=material,  # Material ID’sini qo‘shamiz
                            class_number=material.class_number,  # Materialdan olamiz
                            subject=material.subject,  # Materialdan olamiz
                            quarter=None,
                            test_type=test_type,  # "Fanga oid" test turi
                            question_type=question_type,
                            text=row['Savol'],
                            correct_answer=row['Javob'],
                            option_1=row['Xato javob 1'] if pd.notna(row['Xato javob 1']) and row['Xato javob 1'] != '-' else None,
                            option_2=row['Xato javob 2'] if pd.notna(row['Xato javob 2']) and row['Xato javob 2'] != '-' else None,
                            option_3=row['Xato javob 3'] if pd.notna(row['Xato javob 3']) and row['Xato javob 3'] != '-' else None,
                            score=row['Ball'],
                            difficulty=difficulty,
                            variant=variant,
                            image=None  # Excel’da rasm yo‘q
                        )

                    # Vaqtincha faylni o‘chirish
                    default_storage.delete(file_path)

                except Exception as e:
                    # Agar xato yuz bersa, material saqlangan bo‘lsa ham xato xabarini qaytaramiz
                    return Response({'error': f'Savollarni saqlashda xato: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

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


# Bitta material nomini olish uchun
class MaterialNameDetailView(generics.GenericAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialNameSerializer

    def get(self, request, material_id, *args, **kwargs):
        try:
            material = self.get_queryset().get(id=material_id)
            serializer = self.get_serializer(material, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Material.DoesNotExist:
            return Response({"error": "Material topilmadi"}, status=status.HTTP_404_NOT_FOUND)


# Teacher materiallarini olish uchun
class MaterialTeacherDetailView(generics.GenericAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    def get(self, request, teacher_id, *args, **kwargs):
        try:
            material = self.get_queryset().filter(teacher=teacher_id)
            serializer = self.get_serializer(material, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Material.DoesNotExist:
            return Response({"error": "Material topilmadi"}, status=status.HTTP_404_NOT_FOUND)


# Fan va sinf uchun materiallar ro'yxatini olish
class MaterialByClassSubjectView(generics.GenericAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    def get(self, request, class_id, subject_id, *args, **kwargs):
        try:
            material = self.get_queryset().filter(class_number=class_id, subject=subject_id)
            serializer = self.get_serializer(material, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Material.DoesNotExist:
            return Response({"error": "Material topilmadi"}, status=status.HTTP_404_NOT_FOUND)


# Test yuklash
class TestUploadView(ListCreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = []  # Hozircha ruxsatlar yo‘q, keyin o‘zgartirishingiz mumkin

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            test = serializer.save()  # Testni saqlaymiz, test_file ham saqlanadi

            # Agar test_file mavjud bo‘lsa, savollarni o‘qib, Question modeliga saqlaymiz
            if 'test_file' in request.FILES:
                try:
                    # Faylni vaqtincha saqlash
                    file_path = default_storage.save('temp/test_file.xlsx', request.FILES['test_file'])
                    file_full_path = default_storage.path(file_path)

                    # Excel faylni o‘qish
                    df = pd.read_excel(file_full_path)

                    # Savol darajasini moslashtirish uchun mapping
                    difficulty_mapping = {
                        'B': QuestionDifficulty.objects.get(name='B'),
                        'Q': QuestionDifficulty.objects.get(name='Q'),
                        'M': QuestionDifficulty.objects.get(name='M')
                    }

                    # Savol turini moslashtirish uchun mapping
                    question_type_mapping = {
                        'ochiq': QuestionType.objects.get(name='ochiq'),
                        'yopiq': QuestionType.objects.get(name='yopiq')
                    }

                    # Har bir qatorni o‘qib, Question modeliga saqlash
                    for index, row in df.iterrows():
                        # Savol darajasini moslashtirish
                        difficulty_name = row['Savol darajasi']
                        if difficulty_name not in difficulty_mapping:
                            return Response({'error': f'Noto‘g‘ri savol darajasi: {difficulty_name}'}, status=status.HTTP_400_BAD_REQUEST)
                        difficulty = difficulty_mapping[difficulty_name]

                        # Savol turini moslashtirish
                        question_type_name = row['Savol turi'].lower()
                        if question_type_name not in question_type_mapping:
                            return Response({'error': f'Noto‘g‘ri savol turi: {question_type_name}'}, status=status.HTTP_400_BAD_REQUEST)
                        question_type = question_type_mapping[question_type_name]

                        # Variantni olish
                        variant = Variant.objects.get(id=row['Variant'])

                        # Question obyektini yaratish
                        Question.objects.create(
                            material=None,  # Material bo‘sh qoladi
                            class_number=test.class_number,  # Testdan olamiz
                            subject=test.subject,  # Testdan olamiz
                            quarter=test.quarter,
                            test_type=test.test_type,  # Testdan olamiz
                            question_type=question_type,
                            text=row['Savol'],
                            correct_answer=row['Javob'],
                            option_1=row['Xato javob 1'] if pd.notna(row['Xato javob 1']) and row['Xato javob 1'] != '-' else None,
                            option_2=row['Xato javob 2'] if pd.notna(row['Xato javob 2']) and row['Xato javob 2'] != '-' else None,
                            option_3=row['Xato javob 3'] if pd.notna(row['Xato javob 3']) and row['Xato javob 3'] != '-' else None,
                            score=row['Ball'],
                            difficulty=difficulty,
                            variant=variant,
                            image=None  # Excel’da rasm yo‘q
                        )

                    # Vaqtincha faylni o‘chirish
                    default_storage.delete(file_path)

                except Exception as e:
                    # Agar xato yuz bersa, test saqlangan bo‘lsa ham xato xabarini qaytaramiz
                    return Response({'error': f'Savollarni saqlashda xato: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Teacher ga tegishli testlarni olish
class TestListView(APIView):
    permission_classes = []

    def get(self, request, teacher_id, *args, **kwargs):
        try:
            tests = Test.objects.filter(teacher=teacher_id)
            serializer = TestSerializer(tests, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
