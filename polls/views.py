from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Question, Choice

# Get questions and display them
def index(request, *args, **kwargs):
    latest_question_list = Question.objects.order_by('-question_number')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# Show specific question and choices
def detail(request, question_id, *args, **kwargs):
  try:
    question = Question.objects.get(pk=question_id)
  except Question.DoesNotExist:
    raise Http404("Question does not exist")
  return render(request, 'polls/detail.html', { 'question': question })

# Get question and display results
def results(request, question_id, *args, **kwargs):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'polls/results.html', { 'question': question })

# Vote for a question choice
# helper view to register submitted answer.
def vote(request, question_id, *args, **kwargs):
    # print(request.POST['choice'])
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist) as e:
        print('error:', e)
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
        return HttpResponseRedirect(reverse('polls:index',))

# form to enter answer
def create(request, question_id, *args, **kwargs):
  try:
    question = Question.objects.get(pk=question_id)
  except Question.DoesNotExist:
    raise Http404("Question does not exist")
  
  context = {'current_answer': "my answer", 
             'question': question
            }
  return render(request, 'polls/create.html', context)

# helper view to register submitted answer.
def submit(request, question_id, *args, **kwargs):
    current_answer = request.POST['answer']
    print("submitted answer", current_answer)
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice = Choice(choice_text=current_answer, question=question)
        choice.save()
        question.choice_set.add(choice)
        #selected_choice = question.choice_set.get(pk=request.POST['choice'])
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
        return HttpResponseRedirect(reverse('polls:index',))
