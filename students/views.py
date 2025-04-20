from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.models import CustomUser
from accounts.serializers import RegisterSerializer
from teachers.models import Material
from .models import Submission, TestResult, TestType, Feedback
from .serializers import SubmissionSerializer, TestTypeSerializer, TestResultSerializer, FeedbackSerializer
from django.core.files.storage import default_storage
from django.db.models import Avg
from rest_framework.parsers import MultiPartParser, FormParser
import logging
import os
import openai

logger = logging.getLogger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")


class StudentProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            if user.role != 'student':
                return Response({'error': 'Faqat talabalar uchun'}, status=status.HTTP_403_FORBIDDEN)
            serializer = RegisterSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        try:
            user = request.user
            if user.role != 'student':
                return Response({'error': 'Faqat talabalar uchun'}, status=status.HTTP_403_FORBIDDEN)

            # Validatsiya uchun regions.json faylidan ro'yxatni o'qish
            import json
            with open('regions.json', 'r') as f:  # regions.json fayl yo'lini moslashtiring
                regions_data = json.load(f)
                valid_regions = [region['name'] for region in regions_data['regions']]
                valid_districts = []
                for region in regions_data['regions']:
                    valid_districts.extend(region['districts'])

            # region va district ni validatsiya qilish
            if 'region' in request.data and request.data['region'] and request.data['region'] not in valid_regions:
                return Response({'error': 'Noto‘g‘ri viloyat'}, status=status.HTTP_400_BAD_REQUEST)
            if 'district' in request.data and request.data['district'] and request.data[
                'district'] not in valid_districts:
                return Response({'error': 'Noto‘g‘ri tuman'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = RegisterSerializer(user, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StudentProfileImageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            if user.role != 'student':
                return Response({'error': 'Faqat talabalar uchun'}, status=status.HTTP_403_FORBIDDEN)

            if 'image' not in request.FILES:
                return Response({'error': 'Rasm yuklanmadi'}, status=status.HTTP_400_BAD_REQUEST)

            image_file = request.FILES['image']
            if user.image and default_storage.exists(user.image.name):
                default_storage.delete(user.image.name)
            user.image = image_file
            user.save()

            serializer = RegisterSerializer(user, context={'request': request})
            return Response({'image': serializer.data['image']}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StudentProfileByIdAPIView(APIView):
    permission_classes = []

    def get(self, request, student_id, *args, **kwargs):
        try:
            student = CustomUser.objects.get(id=student_id, role='student')
            serializer = RegisterSerializer(student, context={'request': request})
            # Faqat first_name va last_name qaytarish uchun ma'lumotlarni filtrlaymiz
            data = {
                'first_name': serializer.data.get('first_name'),
                'last_name': serializer.data.get('last_name')
            }
            return Response(data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'O‘quvchi topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SubmitAssignmentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        try:
            material_id = request.data.get('material_id')
            file = request.FILES.get('file')

            if not material_id or not file:
                return Response(
                    {"error": "Material ID va fayl majburiy!"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Materialni topish
            try:
                material = Material.objects.get(id=material_id)
            except Material.DoesNotExist:
                return Response(
                    {"error": "Material topilmadi!"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Foydalanuvchining student ekanligini tekshirish
            if request.user.role != 'student':
                return Response(
                    {"error": "Faqat studentlar vazifa jo‘nata oladi!"},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Submission obyektini yaratish
            submission = Submission.objects.create(
                student=request.user,  # To‘g‘ridan-to‘g‘ri CustomUser obyektini saqlaymiz
                material=material,
                class_number=material.class_number,
                subject=material.subject,
                file=file
            )

            serializer = SubmissionSerializer(submission, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"Vazifani jo‘natishda xato: {str(e)}")
            return Response(
                {"error": f"Vazifani jo‘natishda xato: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StudentSubmitAssignmentAPIView(APIView):
    permission_classes = []

    def get(self, request, student_id, *args, **kwargs):
        try:
            submissions = Submission.objects.filter(student=student_id)
            serializer = SubmissionSerializer(submissions, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StudentSubmitAssignmentByClassSubjectView(APIView):
    permission_classes = []

    def get(self, request, class_number, subject, *args, **kwargs):
        try:
            # Class_number va subject bo‘yicha topshiriqlarni olish
            submissions = Submission.objects.filter(class_number=class_number, subject=subject)
            serializer = SubmissionSerializer(submissions, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StudentSubmitAssignmentMarkGradeView(APIView):
    permission_classes = []

    def patch(self, request, pk, *args, **kwargs):
        try:
            submission = Submission.objects.get(pk=pk)
            grade = request.data.get('grade')

            # grade ni int ga aylantirish
            try:
                grade = int(grade)  # Stringdan int ga aylantirish
            except (ValueError, TypeError):
                return Response({'error': 'Baho butun son bo‘lishi kerak'}, status=status.HTTP_400_BAD_REQUEST)

            # grade ni tekshirish
            if grade < 1 or grade > 5:
                return Response({'error': 'Baho 1-5 oralig‘ida bo‘lishi kerak'}, status=status.HTTP_400_BAD_REQUEST)

            submission.grade = grade
            submission.save()
            serializer = SubmissionSerializer(submission, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Submission.DoesNotExist:
            return Response({'error': 'Topshiriq topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TestTypeListCreateAPIView(APIView):
    permission_classes = []

    def get(self, request):
        test_types = TestType.objects.all()
        serializer = TestTypeSerializer(test_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TestTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestResultListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            test_results = TestResult.objects.filter(is_active=True)
            serializer = TestResultSerializer(test_results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"TestResultListCreateAPIView GET xatosi: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            # Foydalanuvchi autentifikatsiyadan o‘tgan bo‘lishi kerak
            student = request.user
            if student.role != 'student':
                return Response({'error': 'Faqat talabalar uchun'}, status=status.HTTP_403_FORBIDDEN)

            # So‘rovdan ma’lumotlarni olish
            data = request.data
            logger.info(f"So‘rov ma’lumotlari: {data}")

            test_type_id = data.get('test_type')
            subject_id = data.get('subject')
            variant_id = data.get('variant')
            quarter = data.get('quarter')

            # Test turini olish
            try:
                test_type = TestType.objects.get(id=test_type_id)
            except TestType.DoesNotExist:
                logger.error(f"Test turi topilmadi: {test_type_id}")
                return Response({'error': 'Test turi topilmadi'}, status=status.HTTP_404_NOT_FOUND)

            # Avvalgi natijani tekshirish (faqat is_active=True bo‘lganlar)
            query = {
                'student': student,
                'test_type': test_type,
                'subject_id': subject_id,
                'variant_id': variant_id,
                'is_active': True
            }

            # Fanga oid testlar uchun chorakni tekshirish
            if test_type.name == 'Fanga oid':
                if not quarter:
                    logger.error("Fanga oid testlar uchun chorak parametri talab qilinadi")
                    return Response({'error': 'Fanga oid testlar uchun chorak parametri talab qilinadi'},
                                    status=status.HTTP_400_BAD_REQUEST)
                query['quarter'] = quarter

            existing_result = TestResult.objects.filter(**query).first()

            # DTM testlari uchun logika
            if test_type.name == 'DTM':
                if existing_result:
                    # Agar avval ishlagan bo‘lsa, natijani yangilash (PATCH)
                    serializer = TestResultSerializer(existing_result, data=data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    logger.error(f"Serializer xatosi (DTM, PATCH): {serializer.errors}")
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # Yangi natija yaratish (POST)
                    data['student'] = student.id
                    serializer = TestResultSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    logger.error(f"Serializer xatosi (DTM, POST): {serializer.errors}")
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Mock va Fanga oid testlar uchun logika
            else:
                if existing_result:
                    # Agar avval ishlagan bo‘lsa, ruxsat berilmaydi
                    logger.warning(f"Test avval ishlangan: {student.id}, {test_type.name}")
                    return Response(
                        {
                            'error': 'Siz bu testni avval ishlagansiz. Mock va Fanga oid testlarni faqat bir marta ishlash mumkin.'},
                        status=status.HTTP_403_FORBIDDEN
                    )
                else:
                    # Yangi natija yaratish (POST)
                    data['student'] = student.id
                    serializer = TestResultSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    logger.error(f"Serializer xatosi (Mock/Fanga oid, POST): {serializer.errors}")
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"TestResultListCreateAPIView POST xatosi: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestResultDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):
        try:
            test_result = TestResult.objects.filter(student=student_id, is_active=True)
            serializer = TestResultSerializer(test_result, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TestResult.DoesNotExist:
            logger.error(f"Test natijasi topilmadi: student_id={student_id}")
            return Response({"error": "Test natijasi topilmadi!"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"TestResultDetailView GET xatosi: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentReytingView(APIView):
    permission_classes = []

    def get(self, request, student_id):
        try:
            # Berilgan student_id bo‘yicha barcha submission’larni olish va fanlar bo‘yicha guruhlash
            ratings = (
                Submission.objects
                .filter(student=student_id)
                .values('subject__id')  # Fanlar bo‘yicha guruhlash (subject__id)
                .annotate(average_grade=Avg('grade'))  # Har bir fan bo‘yicha o‘rtacha grade
                .order_by('subject__id')  # Tartib uchun
            )

            # Natijani kerakli formatga keltirish
            ratings_dict = {str(rating['subject__id']): float(rating['average_grade']) for rating in ratings}

            # Yakuniy javobni tayyorlash
            response_data = {
                'student_id': student_id,
                'ratings': ratings_dict
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"StudentReytingView xatosi: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FeedbackAPIView(GenericAPIView):
    permission_classes = ()  # Agar autentifikatsiya kerak bo‘lsa, o‘zgartirishingiz mumkin
    serializer_class = FeedbackSerializer  # Serializer sinfini aniqlash

    def post(self, request, *args, **kwargs):
        incorrect_answers = request.data.get('incorrect_answers', [])
        feedback_list = []

        for item in incorrect_answers:
            question_text = item.get('question_text')
            user_answer = item.get('user_answer')
            correct_answer = item.get('correct_answer')
            question_id = item.get('question_id')

            # OpenAI API’dan feedback so‘rash
            prompt = (
                f"Foydalanuvchi quyidagi savolga noto‘g‘ri javob berdi:\n"
                f"Savol: {question_text}\n"
                f"Foydalanuvchi javobi: {user_answer}\n"
                f"To‘g‘ri javob: {correct_answer}\n"
                f"Foydalanuvchiga xatosi haqida tushunarli va foydali feedback bering. Feedback o‘zbek tilida bo‘lsin."
            )

            try:
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system",
                         "content": "Siz o‘quvchilarga feedback beruvchi yordamchisiz. Feedback o‘zbek tilida bo‘lishi"
                                    " kerak. Salom berish shart emas! Faqat savolga qisqa va aniq javob "
                                    "berish bilan chegaralaning!!!"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=150,
                    temperature=0.7
                )
                feedback_text = response.choices[0].message.content.strip()
            except Exception as e:
                feedback_text = f"Feedback generatsiya qilishda xato yuz berdi: {str(e)}"

            # Feedback’ni bazaga saqlash yoki yangilash
            feedback, created = Feedback.objects.get_or_create(
                student=request.user,
                question_id=question_id,
                defaults={
                    'question_text': question_text,
                    'user_answer': user_answer,
                    'correct_answer': correct_answer,
                    'feedback_text': feedback_text
                }
            )

            # Agar feedback allaqachon mavjud bo‘lsa, uni yangilash
            if not created:
                feedback.question_text = question_text
                feedback.user_answer = user_answer
                feedback.correct_answer = correct_answer
                feedback.feedback_text = feedback_text
                feedback.save()

            feedback_list.append({
                'question_id': question_id,
                'question_text': question_text,
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'feedback': feedback_text
            })

        return Response({'feedback': feedback_list}, status=status.HTTP_200_OK)
