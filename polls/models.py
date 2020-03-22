from django.db import models


class Game(models.Model):
    secret_key = models.CharField(max_length=32, default="")
    def __str__(self):
        return self.secret_key[:5]


class Player(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)

    name = models.CharField(max_length=32, default="unknown")
    scores = models.IntegerField(default=0)

    def __str__(self):
        return self.name 


class Round(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, 
                               default=None)

    number = models.IntegerField(default=1)

    def __str__(self):
        return f"round number {self.number}"


class Question(models.Model):
    round_id = models.ForeignKey(Round, on_delete=models.CASCADE, 
                                 default=None)

    question_number = models.IntegerField(default=1)
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, 
                               default=None)

    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
