from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
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
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  
    quiz = QuizSerializer()  

    class Meta:
        model = Score
        fields = ['user', 'score', 'date_taken', 'quiz'] 

    def create(self, validated_data):
        quiz_data = validated_data.pop('quiz')
        quiz, created = Quiz.objects.get_or_create(title=quiz_data['title'])
        score = Score.objects.create(quiz=quiz, **validated_data)
        return score
