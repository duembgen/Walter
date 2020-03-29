from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Question, Choice, Round, Player, Game, Vote

# Get questions and display them
def index(request, **kwargs): #game,round_id
    this_round = get_object_or_404(Round, pk=kwargs.get('round_id'))
    master = this_round.player.name
    latest_question_list = Question.objects.filter(round=this_round)
    context = {'latest_question_list': latest_question_list, 
               'master': master,
               **kwargs}
    return render(request, 'polls/index.html', context)

# Show specific question and choices for voting
def detail(request, **kwargs): #game,round,question_id
    game_key = kwargs.get('secret_key')
    game = Game.objects.get(secret_key=kwargs.get('secret_key'))
    player = get_object_or_404(Player, user=request.user, 
                               game=game)
    question = get_object_or_404(Question, pk=kwargs['question_id'])

    try:
        current_vote = Vote.objects.get(player=player, question=question)
        current_choice = current_vote.choice
        print('found vote', vote)
    except Vote.DoesNotExist:
        current_choice = -1

    users_choice = Choice.objects.get(player=player, question=question)

    context = {'question':question, 
               'current_choice': current_choice,
               'users_choice': users_choice,
               **kwargs}
    return render(request, 'polls/detail.html', context)

# Get question and display results
def results(request, **kwargs): #game,round,question_id
    question = get_object_or_404(Question, pk=kwargs['question_id'])
    context = {'question':question, **kwargs}
    return render(request, 'polls/results.html', context)

# Helper view to submit vote
def vote(request, **kwargs): # game,round,question_id
    question = get_object_or_404(Question, pk=kwargs.get('question_id'))
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except:
        #Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
          'question': question,
          'error_message': "Komisch, ungültige Antwort.",
          **kwargs
        })

    selected_choice.votes += 1
    selected_choice.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    #return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    url_kwargs = {key:kwargs.get(key) for key in ['secret_key', 'round_id']}
    return HttpResponseRedirect(reverse('polls:index',kwargs=url_kwargs))

# Form to enter answer
def create(request, **kwargs): # game,round,question_id
    question = get_object_or_404(Question, pk=kwargs.get('question_id'))
    game = get_object_or_404(Game, secret_key=kwargs.get('secret_key'))
    print('looking for', request.user, game)
    player = get_object_or_404(Player, user=request.user, game=game)
    try:
        current_answer = get_object_or_404(Choice, question=question, player=player)
    except:
        current_answer = ""

    context = {
        'current_answer': current_answer, 
        'question': question,
        **kwargs
    }
    print('context:', context)
    return render(request, 'polls/create.html', context=context)

# Helper view to register submitted answer
def submit(request, **kwargs): # game,round,question_id
    print('submitted', kwargs)
    current_answer = request.POST['answer']
    question = get_object_or_404(Question, pk=kwargs.get('question_id'))

    game_key = kwargs.get('secret_key')
    game = Game.objects.get(secret_key=kwargs.get('secret_key'))
    player = Player.objects.get(user=request.user, game=game)

    try:
        choice = Choice.objects.get(question=question, player=player)
        choice.choice_text = current_answer
        choice.save()
    except Choice.DoesNotExist:
        choice = Choice(choice_text=current_answer, question=question, 
                        player=player)
        choice.save()
        question.choice_set.add(choice)
    except Exception as e:
        # Redisplay the question voting form.
        print('error occured...', e)
        return render(request, 'polls/create.html', {
            'question': question,
            'current_answer': current_answer,
            'error_message': "Antwort nicht gültig",
            **kwargs
        })

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.

    url_kwargs = {key:kwargs.get(key) for key in ['secret_key', 'round_id']}
    print('url kwargs:', url_kwargs)
    return HttpResponseRedirect(reverse('polls:index', kwargs=url_kwargs))
