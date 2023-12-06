from django.urls import path
from .views import CustomTokenObtainPairView, UsersPointsGet

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/points/', UsersPointsGet.as_view(), name='user_get_points')
]