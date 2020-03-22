from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.crypto import get_random_string

from polls.models import Game, Player, Round, Question

def index(request):
    return render(request, 'pages/index.html')

def new_game(request):
    secret_key = get_random_string(10)
    return render(request, 'pages/game.html', 
                  {'secret_key':secret_key})

def post_new_game(request):
    print('data in new_game:')
    secret_key = request.POST['secret_key']
    player_name = request.POST['player_name']
    print(secret_key, player_name)
    try:
        game = Game.objects.get(secret_key=secret_key)
    except Game.DoesNotExist:
        game = Game(secret_key=secret_key)
        game.save()

    player = Player(name=player_name, game_id=game)
    player.save()
    return HttpResponseRedirect(reverse('pages:start_game', kwargs={'game_id': game.secret_key}))

def start_game(request, game_id):
    game = Game.objects.get(secret_key=game_id)

    # find out which players are in this game.
    players = Player.objects.filter(game_id=game)
    # create first round with three questions.
    first_round = Round(game_id=game, player=players[0], number=1)
    first_round.save()
    questions = [Question(round_id=first_round, 
                          question_number=i,
                          question_text=f"Question {i}") for i in range(1, 4)]
    [q.save() for q in questions]
    return render(request, 'pages/start_game.html', 
                  {'game_id':game_id, 
                   'round_id': first_round.pk,
                   'players':players})
