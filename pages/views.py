from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
    
from polls.models import Game, Player, Round, Question

from .forms import UserForm

def index(request):
    return render(request, 'pages/index.html')

@login_required(login_url='/login?error_message="You need to log in!"')
def new_game(request):
    secret_key = get_random_string(10)
    return render(request, 'pages/game.html', 
                  {'secret_key':secret_key})

@login_required(login_url='/login?error_message="You need to log in!"')
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

@login_required(login_url='/login?error_message="You need to log in!"')
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

@login_required
def special(request):
    return HttpResponse("You are logged in !")
    
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
