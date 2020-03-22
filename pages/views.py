from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.crypto import get_random_string

from polls.models import Game, Player

def index(request):
    return render(request, 'pages/index.html')

def new_game(request):
    secret_key = get_random_string(32)
    return render(request, 'pages/game.html', 
                  {'game_id':'new_id_will_be_here', 
                   'secret_key':secret_key})

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
    #return HttpResponseRedirect(reverse('pages:index'))
    return HttpResponseRedirect(reverse('pages:start_game', kwargs={'game_id': game.secret_key}))
    #reverse('pages:polls', kwargs={'game_id':game.secret_key}))

def start_game(request, game_id):
    return render(request, 'pages/start_game.html', 
                  {'game_id':game_id, 
                   'players':['dummy1', 'dummy2']})
