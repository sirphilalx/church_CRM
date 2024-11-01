from .models import CustomUser
from rest_framework import viewsets, views,status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, IsAdminOrSecretary, IsZonalHead, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

class UserRegistrationViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully', 'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(views.APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            response_data = {
                'id': user.id,
                'username': user.username,
                'role': user.role,
                'firstname': user.firstname,
                'middlename': user.middlename,
                'lastname': user.lastname,
                'zone': user.zone,
                'address': user.address,
                'date_of_birth': user.date_of_birth,
                'token': token.key  # Include the token in the response
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)



class UserLogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()  # Delete the token to log out
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'error': 'You were not logged in'}, status=status.HTTP_400_BAD_REQUEST)


# list of members in the church only accessible to administrators and not members

class ZonalAttendanceView(views.APIView):
    permission_classes = [IsZonalHead]  # Only zonal heads can access this view

    def get(self, request):
        # Fetch the users in the same zone as the logged-in user
        users_in_zone = CustomUser.objects.filter(zone=request.user.zone)
        serializer = UserSerializer(users_in_zone, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AdminOrSecretaryView(views.APIView):
    permission_classes = [IsAdminOrSecretary]  # Only admin or secretary can access this view

    def get(self, request):
        # Some admin/secretary functionality that can access all users
        all_users = CustomUser.objects.all()
        serializer = UserSerializer(all_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AdminOrSecretaryView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated & IsAdminOrSecretary]  # Only allows admin or secretary
    queryset = CustomUser.objects.all()  # All users
    serializer_class = UserSerializer

class ZonalUserView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated & IsZonalHead]  # Only allows zonal heads
    serializer_class = UserSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(zone=self.request.user.zone)  # Filter users by the zonal head's zone
    
# A dedicated view for assigning roles and permissions to users
class AssignUserRoleView(views.APIView):
    permission_classes = [IsAuthenticated & IsAdminOrSecretary]  # Only admins or secretaries can assign roles

    def post(self, request, username):
        role = request.data.get('role')
        if role not in [choice[0] for choice in CustomUser.ROLE_CHOICES]:
            return Response({'error': 'Invalid role specified.'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(CustomUser, username=username)
        user.role = role  # Assign the new role
        user.save()
        
        return Response({'message': f'Role for {username} updated to {role}.'}, status=status.HTTP_200_OK)