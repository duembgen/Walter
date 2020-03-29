from django.db import models
from django.contrib.auth.models import User

def create_round(game):
    # choose next "master" player 
    try:
        curr_player = Player.objects.get(game=game, is_master=True)
    except Exception as e:
        player = Player.objects.filter(game=game)[0]
    else:
        curr_player.is_master = False
        curr_player.save()
        player = Player.get_next_by_timestamp(curr_player)
        print('got next by number:', player)
    player.is_master = True
    player.save()

    first_round = Round(game=game, player=player, number=1)
    first_round.save()
    questions = [Question(round=first_round, 
                          question_number=i,
                          question_text=f"Frage {i}") for i in range(1, 4)]
    [q.save() for q in questions]
    return first_round


class Game(models.Model):
    secret_key = models.CharField(max_length=32, default="")
    current_round = models.ForeignKey('Round', on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    def __str__(self):
        return self.secret_key[:5]


class Player(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    name = models.CharField(max_length=32, default="unknown")
    score = models.IntegerField(default=0)
    is_master = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name 


class Round(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, 
                               default=None)

    number = models.IntegerField(default=1)

    def __str__(self):
        return f"round number {self.number}"


class Question(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, 
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


class Vote(models.Model):
    # each player has one choice for each question.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, default=0, null=True, blank=True)


