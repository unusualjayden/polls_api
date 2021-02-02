from django.db import transaction
from django.utils.datetime_safe import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Poll,
    Question,
    QuestionAnswer,
)
from .serializers import (
    PollAnswerSerializer,
    PollSerializer,
    PollWithQuestionsSerializer,
    QuestionAndAnswerSerializer,
)


class ActivePollListAPIView(APIView):
    def get(self, request):
        polls = Poll.objects.filter(starts_at__lte=datetime.now(), ends_at__gte=datetime.now())
        serializer = PollSerializer(polls, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PollByIdAPIView(APIView):
    def get(self, request, poll_id):
        poll = Poll.objects.get(id=poll_id)
        serializer = PollWithQuestionsSerializer(poll)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, poll_id):
        if Question.objects.filter(poll=poll_id) is None or Poll.objects.filter(id=poll_id) is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PollAnswerSerializer(data=request.data, context={'poll': poll_id})
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserResultsAPIView(APIView):
    @staticmethod
    def get_user_answers(user_id):
        try:
            return QuestionAnswer.objects.prefetch_related('poll_answer').filter(
                poll_answer__user_id=int(user_id))
        except QuestionAnswer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_id):
        data = self.get_user_answers(user_id)
        serializer = QuestionAndAnswerSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
