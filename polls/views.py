# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice
from django.shortcuts import render, get_object_or_404

# Create your views here.
def index(req):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(req, 'polls/index.html', context)


def detail(req, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(req, 'polls/detail.html', {'question': question})

def results(req, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(req, 'polls/results.html', {'question': question})

def vote (req, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=req.POST['choice'])
    except (selected_choice.DoesNotExist, KeyError):
        return render(req, 'polls/detail.html', {'question': question, 'error_message': 'You did not select a choice.'})
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=[question.id]))
