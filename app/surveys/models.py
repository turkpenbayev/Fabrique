from django.db import models


class Survey(models.Model):
    name = models.CharField(max_length=400)
    description = models.TextField()
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.name)


class Question(models.Model):
    TEXT = 1
    RADIO = 2
    SELECT = 3

    QUESTION_TYPES = (
        (TEXT, 'text'),
        (RADIO, 'radio'),
        (SELECT, 'select'),
    )

    text = models.TextField()
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    question_type = models.PositiveSmallIntegerField(choices=QUESTION_TYPES, default=TEXT)


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=400)
