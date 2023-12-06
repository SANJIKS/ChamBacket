import qrcode
import base64
import hashlib

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.http import HttpResponse
from .models import Backet
from .serializers import BackerSerializer

class BacketViewSet(ModelViewSet):
    queryset = Backet.objects.all()
    serializer_class = BackerSerializer

    @action(detail=True, methods=['post'])
    def add_bottles(self, request, pk=None):
        try:
            num_bottles = int(request.data.get('num_bottles', 0))
            if num_bottles > 0:
                backet = self.get_object()
                backet.active_points += num_bottles * 5  # Предполагаем 5 баллов за бутылку

                # Генерация токена
                token_data = f"{backet.id}-{num_bottles}"  # Пример данных, которые могут быть включены в токен
                token = base64.b64encode(hashlib.sha256(token_data.encode()).digest()).decode()
                
                backet.token = token

                backet.save()
                # Создание QR-кода с токеном
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(token)
                qr.make(fit=True)
                qr_code_img = qr.make_image(fill_color="black", back_color="white")

                # Сохранение изображения QR-кода (это опционально)
                qr_code_img.save(f"my_qrcode_{backet.id}.png")

                response = HttpResponse(content_type="image/png")
                qr_code_img.save(response, "PNG")
                return response
            else:
                return Response({'error': 'Invalid number of bottles'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    @action(detail=False, methods=['post'])
    def scan_qr_code(self, request):
        try:
            # Получаем данные из запроса
            hash_value = request.data.get('hash_value', '')
            # user_token = request.data.get('user_token', '')

            # Ищем backet по хэшу
            backet = Backet.objects.filter(token=hash_value).first()

            if backet and backet.active_points > 0:
                # Проверяем соответствие токена пользователя
                if backet.token:
                    # Начисляем баллы пользователю
                    user = request.user
                    user.points += backet.active_points
                    user.save()

                    # Обнуляем баллы backet и ставим None в его token
                    backet.active_points = 0
                    backet.token = None
                    backet.save()

                    return Response({'message': 'Points added successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid user token'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'No active points to add or invalid hash'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)