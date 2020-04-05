from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
    
from polls.models import Game, Player, Round, Question, create_round


from .forms import UserForm

DEBUG = 'pages/views'
LOGIN_URL = '/login?error_message=Du+musst+dich+einloggen+um+zu+spielen!'

# start page
def index(request):
    return render(request, 'pages/index.html')

# create new game
@login_required(login_url=LOGIN_URL)
def new_game(request, **kwargs):
    print(f"{DEBUG} new_game kwargs: {kwargs}")

    # set the secret key to random if it was not already set.
    secret_key = get_random_string(10)
    kwargs['secret_key'] = kwargs.get('secret_key', secret_key)
    return render(request, 'pages/new_game.html', context=kwargs)

def quit_game(request, secret_key, **kwargs):
    # TODO: remove the player from the list
    # if it was this player's turn, assign someone else.
    try:
        game = Game.objects.get(secret_key=secret_key)
        player = Player.objects.get(user=request.user, game=game)
    except:
        print('error in quit_game')
        raise
    print(f"{DEBUG}: {player} left.")
    return render(request, 'pages/index.html')

# helper function to create or load chosen game. 
@login_required(login_url=LOGIN_URL)
def post_new_game(request):
    secret_key = request.POST['secret_key']
    player_name = request.POST['player_name']

    print(f'{DEBUG}: data in new_game:', secret_key, player_name)

    new_game = False
    try:
        game = Game.objects.get(secret_key=secret_key)
        print(f'{DEBUG}: loaded game of key {secret_key}')
    except Game.DoesNotExist:
        game = Game(secret_key=secret_key)
        new_game = True
        game.save()

    # make sure this user does not already have a player in the game.
    context = {
        'secret_key': secret_key,
        'player_name': player_name
    }
    if Player.objects.filter(game=game, name=player_name):
        # TODO: I want to pass a context here but I can't
        # It isi easy with render but then that's not "safe". 
        # Need to figure out how to do this...
        # return HttpResponseRedirect(reverse('pages:new_game'))
        context['error_message'] = "Diesen Namen hat schon jemand anderes benutzt!"
        return render(request, 'pages/new_game.html', context=context)
    elif Player.objects.filter(game=game, user=request.user):
        context['error_message'] = f"Du ({request.user.username}) bist schon im Spiel!"
        return render(request, 'pages/new_game.html', context=context)

    player = Player(name=player_name, game=game, user=request.user)
    player.save()

    if new_game:
        print('creating new game')
        first_round = create_round(game)
        game.current_round = first_round
        game.save()

    return HttpResponseRedirect(reverse('pages:index_game', kwargs={'secret_key': game.secret_key }))

# game start page
@login_required(login_url=LOGIN_URL)
def index_game(request, secret_key):
    game = Game.objects.get(secret_key=secret_key)
    current_round = Round.objects.get(id=game.current_round.id)
    # find out which players are in this game.
    players = Player.objects.filter(game=game)
    all_round_ids = [r.id for r in Round.objects.filter(game=game)]
    context = {
        'secret_key':secret_key, 
        'all_round_ids': all_round_ids, 
        'round_id': current_round.id,
        'players':players
    }
    return render(request, 'pages/index_game.html', 
                  context=context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('pages:index'))
    
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,'pages/register.html',
                          {'user_form':user_form,
                           'registered':registered})
 
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('pages:index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        print('rendering', request.GET)
        return render(request, 'pages/login.html', request.GET)
