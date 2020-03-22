from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Question, Choice, Round, Player

# Get questions and display them
def index(request, **kwargs): #game,round_id
    this_round = get_object_or_404(Round, pk=kwargs.get('round_id'))
    latest_question_list = Question.objects.filter(round_id=this_round)
    context = {'latest_question_list': latest_question_list, 
               **kwargs}
    return render(request, 'polls/index.html', context)

# Show specific question and choices
def detail(request, **kwargs): #game,round,question_id
    question = get_object_or_404(Question, pk=kwargs['question_id'])
    context = {'question':question, **kwargs}
    return render(request, 'polls/detail.html', context)

# Get question and display results
def results(request, **kwargs): #game,round,question_id
    question = get_object_or_404(Question, pk=kwargs['question_id'])
    context = {'question':question, **kwargs}
    return render(request, 'polls/results.html', context)

# helper view to register submitted vote.
def vote(request, **kwargs): # game,round,question_id
    question = get_object_or_404(Question, pk=kwargs.get('question_id'))
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        #return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        return HttpResponseRedirect(reverse('polls:index',kwargs=kwargs))

# form to enter answer
def create(request, **kwargs): # game,round,question_id
    question = get_object_or_404(Question, pk=kwargs.get('question_id'))
    context = {
        'current_answer': "Enter answer here", 
        'question': question,
        **kwargs
    }
    return render(request, 'polls/create.html', context)

# helper view to register submitted answer.
def submit(request, **kwargs): # game,round,question_id
    current_answer = request.POST['answer']
    print("submitted answer", current_answer)
    print("user:", request.user)
    question = get_object_or_404(Question, pk=kwargs.get('question_id'))

    # TODO change this...
    player = Player.objects.first()

    try:
        choice = Choice(choice_text=current_answer, question=question, 
                        player_id=player)
        choice.save()
        question.choice_set.add(choice)
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/create.html', {
            'question': question,
            'current_answer': current_answer,
            'error_message': "Invalid answer",
        })
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:index',kwargs=kwargs))
