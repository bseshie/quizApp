from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login as auth_login, logout
from .serializers import UserSerializer, AuthTokenSerializer , ScoreSerializer
from accounts.models import Score




class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['POST'])
# def logout_user(request):
#     logout(request)
#     return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


from django.contrib.auth import logout as auth_logout
from accounts.models import Score  

@api_view(['POST'])
def logout_user(request):
    user = request.user
    auth_logout(request)
    
    # Clear scores for the logged-out user
    if user.is_authenticated:
        Score.objects.filter(account=user).delete()  # Make sure the field is 'account'
    
    return Response({'message': 'Logged out and scores cleared successfully'}, status=status.HTTP_200_OK)


# class ScoreListView(APIView):
#     def get(self, request):
#         print("Request received at ScoreListView")
#         username = request.query_params.get('username')
#         if username:
#             scores = Score.objects.filter(account__username=username)
#             if scores.exists():
#                 serializer = ScoreSerializer(scores, many=True)
#                 return Response(serializer.data)
#             else:
#                 return Response({"detail": "No scores found for this user."}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             return Response({"detail": "Username not provided."}, status=status.HTTP_400_BAD_REQUEST)


from django.contrib.auth.models import User

class ScoreListView(APIView):
    def get(self, request):
        print("Request received at ScoreListView")
        username = request.query_params.get('username')
        print(f"Username received: {username}")
        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            
            scores = Score.objects.filter(account=user)
            print(f"Scores found: {scores}")
            if scores.exists():
                serializer = ScoreSerializer(scores, many=True)
                return Response(serializer.data)
            else:
                return Response({"detail": "No scores found for this user."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Username not provided."}, status=status.HTTP_400_BAD_REQUEST)


class SubmitScoreView(generics.GenericAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Score saved successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

