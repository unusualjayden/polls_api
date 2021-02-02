from django.db import models


class Poll(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()

    class Meta:
        db_table = 'polls'

    def __str__(self):
        return f'Poll name: {self.name} Starts at: {self.starts_at} Ends at: {self.ends_at}'


class Question(models.Model):
    CHOICES = (
        ('1', 'Текстовый ответ'),
        ('2', 'Выбор одного варианта'),
        ('3', 'Выбор нескольких вариантов'),
    )

    question_type = models.CharField(max_length=1, choices=CHOICES, default=CHOICES[0])
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')
    content = models.TextField()

    class Meta:
        db_table = 'poll_question'

    def __str__(self):
        return f'poll: {self.poll}\nquestion content: {self.content}'


class PollAnswer(models.Model):
    user_id = models.IntegerField()
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='poll')

    class Meta:
        db_table = 'poll_answer'

    def __str__(self):
        return f'user: {self.user_id}\npoll: {self.poll}'


class QuestionAnswer(models.Model):
    poll_answer = models.ForeignKey(PollAnswer, on_delete=models.CASCADE, related_name='poll_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_answer')
    content = models.TextField()

    class Meta:
        db_table = 'question_answer'

    def __str__(self):
        return f'question: {self.question}\nanswer content: {self.content}'
