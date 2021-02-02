from rest_framework import serializers

from .models import Poll, Question, PollAnswer, QuestionAnswer


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'


# Сериализаторы для обработки вопросов


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'content',)


class PollWithQuestionsSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ('name', 'description', 'questions',)


# Сериализаторы для обработки ответов на вопросы


class QuestionAnswerSerializer(serializers.ModelSerializer):
    question = serializers.IntegerField()

    class Meta:
        model = QuestionAnswer
        fields = ('question', 'content')


class PollAnswerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=False)
    answers = QuestionAnswerSerializer(many=True)

    class Meta:
        model = PollAnswer
        fields = ('user_id', 'answers')

    def create(self, validated_data):
        print()
        ans = validated_data.pop('answers')
        if validated_data.get('user_id') is None:
            user_id = 0
        else:
            user_id = validated_data['user_id']
        poll_answer = PollAnswer.objects.create(poll_id=self.context['poll'],
                                                user_id=user_id)
        for answer in ans:
            print(answer)
            QuestionAnswer.objects.create(poll_answer=poll_answer, question_id=int(answer['question']),
                                          content=answer['content'])
        return poll_answer


# Сериализатор для вывода пользователя


class QuestionAndAnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    answer = serializers.CharField(source='content')
    poll_id = serializers.IntegerField(source='question.poll_id')

    class Meta:
        model = QuestionAnswer
        fields = ('poll_id', 'question', 'answer')
