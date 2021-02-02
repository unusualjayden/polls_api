from django.urls import path

from .views import (
    ActivePollListAPIView,
    PollByIdAPIView,
    UserResultsAPIView
)




urlpatterns = [
    # Endpoint'ы для пользователей
    path('polls/', ActivePollListAPIView.as_view(), name='active_poll_list'),
    path('polls/<int:poll_id>', PollByIdAPIView.as_view(), name='poll_by_id'),
    path('users/<int:user_id>', UserResultsAPIView.as_view(), name='user_results'),

]
