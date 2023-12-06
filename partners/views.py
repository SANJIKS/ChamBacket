from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


import qrcode
import json
import base64
from io import BytesIO


from .models import Partner
from .serializers import PartnerSerializer


class PartnersViewSet(ModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer


    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'points_to_spend': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['points_to_spend'],
        ),
        operation_summary='Снятие баллов'
    )
    @action(detail=True, methods=['post'])
    def spend_points(self, request, pk=None):
        try:
            partner = self.get_object()
            user = request.user

            # Получаем данные из запроса
            points_to_spend = int(request.data.get('points_to_spend', 0))

            # Проверяем, достаточно ли баллов у пользователя
            if user.points >= points_to_spend:
                # Снимаем баллы у пользователя
                user.points -= points_to_spend
                user.save()


                return Response({'message': f'{points_to_spend} points to {partner.name} spent successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Not enough points'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    @action(detail=True, methods=['get'])
    def generate_qr_code(self, request, pk=None):
        try:
            partner = self.get_object()

            # Создаем JSON с ID партнера
            qr_data = {'partner_id': partner.id}
            qr_json = json.dumps(qr_data)

            # Создаем QR-код с JSON-данными
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_json)
            qr.make(fit=True)
            qr_code_img = qr.make_image(fill_color="black", back_color="white")

            # Преобразование изображения в строку
            buffered = BytesIO()
            qr_code_img.save(buffered, format="PNG")
            qr_code_str = base64.b64encode(buffered.getvalue()).decode()

            qr_code_img.save(f"my_qrcode_{partner.id}.png")

            response = HttpResponse(content_type="image/png")
            qr_code_img.save(response, "PNG")
            return response

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)