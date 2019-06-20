from django.db import models
from user.models import Profile
# Create your models here.

class Questionset(models.Model):
    status = models.BooleanField(default=False)
    set_id = models.IntegerField()
    question_count = models.IntegerField()

    def __str__(self):
        return str(self.set_id)

    def save(self, *args, **kwargs):
        if self.status is True:
            if Questionset.objects.filter(status=True).exists():
                questionsets = Questionset.objects.filter(status=True)
                for questionset in questionsets:
                    questionset.status = False
                    questionset.save()
            self.status = True
        super(Questionset, self).save(*args, **kwargs)

class Question(models.Model):
    CHOICES = (
        ('IMG', 'Image Question'),
        ('TXT', 'Text Question')
    )
    status = models.BooleanField(default=False)
    q_type = models.CharField(max_length =3,choices = CHOICES, default='TXT' )
    question = models.CharField(max_length=256)
    description = models.TextField()
    timelimit = models.IntegerField()
    score = models.FloatField()
    question_set = models.ForeignKey(Questionset, on_delete=models.CASCADE)

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        if self.status is True:
            if Question.objects.filter(status=True).exists():
                questions = Question.objects.filter(status=True)
                for question in questions:
                    question.status = False
                    question.save()
            self.status = True
        super(Question, self).save(*args, **kwargs)
