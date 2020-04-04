from django.db import models
from django.contrib.auth.models import User


def find_next_player(all_players):
    from itertools import cycle, islice, dropwhile
    cycled = cycle(all_players)
    skipped = dropwhile(lambda x: x.is_master, cycled)
    sliced = islice(skipped, None, 1)
    result = list(sliced)[0]
    return result

def create_round(game, number=1):
    # find all players
    all_players = Player.objects.filter(game=game)
    master_players = [p for p in all_players if p.is_master]
    if len(master_players) == 0:
        print('assigning first master player.')
        next_player = all_players[0]
    elif len(master_players) == 1:
        print('assigning next master player.')
        curr_player = Player.objects.get(game=game, is_master=True)
        next_player = find_next_player(all_players)
        curr_player.is_master = False
        curr_player.save()

    next_player.is_master = True
    next_player.save()

    # create next round with 3 questions.
    next_round = Round(game=game, player=next_player, number=number)
    next_round.save()
    questions = [Question(round=next_round, 
                          question_number=i,
                          question_text=f"Frage {i}") for i in range(1, 4)]
    [q.save() for q in questions]
    return next_round


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
        return f"Round {self.pk}"


class Question(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, 
                                 default=None)

    question_number = models.IntegerField(default=1)
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    class Meta:
        ordering = ['choice_text']
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
