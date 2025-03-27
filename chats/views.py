from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import ChatMessage
from .serializers import ChatMessageSerializer
import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


class ChatAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message = request.data.get('message')
        if not message:
            return Response({'error': 'Xabar bo‘sh bo‘lmasligi kerak'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Foydalanuvchining oldingi xabarlarini olish
            previous_messages = ChatMessage.objects.filter(user=request.user.username).order_by('-timestamp')[:2]

            # Open AI API uchun messages ro‘yxatini tayyorlash
            messages = [
                {
                    "role": "system",
                    "content": "Siz ixtisoslashgan maktab platformasi uchun yordamchi AI’siz. Foydalanuvchilarning savollariga aniq va foydali javoblar bering."
                }
            ]

            # Oldingi xabarlarni qo‘shish
            for msg in previous_messages:
                messages.append({"role": "user", "content": msg.message})
                messages.append({"role": "assistant", "content": msg.reply})

            # Joriy foydalanuvchi xabarini qo‘shish
            messages.append({"role": "user", "content": message})

            # OpenAI API’ga so‘rov yuborish
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=messages,
            )

            # Javobni olish
            reply = response.choices[0].message.content.strip()

            # Xabarni bazaga saqlash
            chat_message = ChatMessage.objects.create(
                user=request.user.username if request.user.is_authenticated else "Anonymous",
                message=message,
                reply=reply
            )

            return Response({'reply': reply}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChatHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = ChatMessage.objects.filter(user=request.user.username).order_by('timestamp')
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
