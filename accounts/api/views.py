from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login as auth_login, logout
from .serializers import UserSerializer, AuthTokenSerializer , ScoreSerializer
from accounts.models import Score,Quiz
from django.contrib.auth.models import User
import logging





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



@api_view(['POST'])
def logout_user(request):
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)





logger = logging.getLogger(__name__)
class SubmitScoreView(APIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

    def post(self, request, *args, **kwargs):
        user_name = request.data.get('userName')
        quiz_title = request.data.get('quiz', {}).get('title')
        score_value = request.data.get('score')

        print("Received data:")
        print(f"user_name: {user_name}")
        print(f"quiz_title: {quiz_title}")
        print(f"score_value: {score_value}")

        if not all([user_name, quiz_title, score_value]):
            return Response({"detail": "Incomplete data."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            quiz, created = Quiz.objects.get_or_create(title=quiz_title)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        score = Score(user=user, quiz=quiz, score=score_value)
        score.save()
        return Response({'message': 'Score saved successfully'}, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        username = request.query_params.get('username')
        if not username:
            return Response({"detail": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            scores = Score.objects.filter(user=user)
            serializer = ScoreSerializer(scores, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching scores: {str(e)}")
            return Response({"detail": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


