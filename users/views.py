from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            username = request.data.get('username')

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise exceptions.ValidationError("Пользователь не найден")

            if not user.phone_number:
                return Response({"user_id": user.id}, status=status.HTTP_400_BAD_REQUEST)

        return response
    
class UsersPointsGet(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user

        user_points = getattr(user, 'points', None)

        if user_points is not None:
            return Response({'points': user_points}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User points not found'}, status=status.HTTP_404_NOT_FOUND)
