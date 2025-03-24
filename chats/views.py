from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChatMessage
from .serializers import ChatMessageSerializer
import openai
from dotenv import load_dotenv
load_dotenv()
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

class ChatAPIView(APIView):
    permission_class = []
    
    def post(self, request):
        message = request.data.get('message')
        if not message:
            return Response({'error': 'Xabar bo‘sh bo‘lmasligi kerak'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Siz ixtisoslashgan maktab platformasi uchun yordamchi AI’siz. Foydalanuvchilarning savollariga aniq va foydali javoblar bering."},
                    {"role": "user", "content": message},
                ],
                max_tokens=150,
                temperature=0.7,
            )
            reply = response.choices[0].message['content'].strip()

            chat_message = ChatMessage.objects.create(
                user="Anonymous",
                message=message,
                reply=reply
            )

            return Response({'reply': reply}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ChatHistoryAPIView(APIView):
    permission_class = []

    
    def get(self, request):
        messages = ChatMessage.objects.all().order_by('timestamp')
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    