from django.urls import path
from .views import SignUpView, LoginView, logout_user,SubmitScoreView,ScoreListView

urlpatterns = [
    path('signups/', SignUpView.as_view(), name='signup'),
    path('logins/', LoginView.as_view(), name='login'),
    path('logouts/', logout_user, name='logout_user'),
    path('scores/', SubmitScoreView.as_view(), name='score'),
    path('score/', ScoreListView.as_view(), name='scores'), 
]



