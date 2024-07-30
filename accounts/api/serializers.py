from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
# from accounts.models import Score, Quiz, Account
from rest_framework import serializers
from accounts.models import Score,Quiz  



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()



class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['title']  

class ScoreSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    quiz = QuizSerializer()  

    class Meta:
        model = Score
        fields = ['account', 'quiz', 'score', 'date_taken']

    def create(self, validated_data):
        quiz_data = validated_data.pop('quiz')
        quiz_title = quiz_data.get('title')
        quiz, created = Quiz.objects.get_or_create(title=quiz_title)
        validated_data['quiz'] = quiz
        return super().create(validated_data)