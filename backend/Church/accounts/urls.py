from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationViewSet, UserLoginView, UserLogoutView, AdminOrSecretaryView, ZonalUserView, AssignUserRoleView

router = DefaultRouter()
router.register(r'register', UserRegistrationViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),


    # Additional views for admin or secretary role and zonal heads
    path('users', AdminOrSecretaryView.as_view({'get': 'list'}), name='admin-or-secretary'),
    path('zonal-users', ZonalUserView.as_view({'get': 'list'}), name='zonal-users'), 

    # url for assgining roles and permissions to users
    path('assign-role/<str:username>/', AssignUserRoleView.as_view(), name='assign-user-role')
]
