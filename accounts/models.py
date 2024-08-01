from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# class Account(models.Model):
#     name = models.CharField(max_length=128)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128)

#     def __str__(self):
#         return self.name
    

class Quiz(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title



class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.quiz.title} - {self.score}"
    
    
