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

def post_new_game(request, game_id):
    print('data in new_game:', game_id)
    secret_key = request.POST['secret_key']
    player_name = request.POST['player_name']
    try:
        game = Game.objects.get(secret_key=secret_key)
    except: 
        raise Http404(f"Game with secret_key {secret_key} does not exist")
    else:
        player = Player(name=player_name, game=game)
        player.save()
        return HttpResponseRedirect(reverse('pages:polls', game.secret_key))
