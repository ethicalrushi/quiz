from django.shortcuts import render
from .models import Question, Questionset
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
import time
import socket

def get_q():
    if Questionset.objects.filter(status=True).exists():
        questionset = Questionset.objects.get(status=True)
        # questions = Question.objects.filter(question_set=questionset)
        # return questions
        i = questionset.set_id
        if i is not None:
            first = Question.objects.get(status=True, question_set=i)
            # imp = first & result
            first.status = True
            first.save()
            # obj = first.question
        return first
    else:
        return None

def get_question(request):
    i = get_q()
    if i is not None:
        obj = i.question
    else:
        obj = 'Oops! Qui is not live. Try again at specfied time'
    return render(request,'index.html',{'q':obj})
    
def get_active_questions():
    if Questionset.objects.filter(status=True).exists():
        questionset = Questionset.objects.get(status=True)
        questions = Question.objects.filter(question_set=questionset)
        return questions



def make_quiz_live(request,id):
    error_msg = {}
    questionset = Questionset.objects.get(id=id)
    questionset.status = True
    questionset.save()
    error_msg['succes'] = True
    error_msg['message'] = f'Questionset wiith id {id} is live'
    return JsonResponse(error_msg)

def end_quiz(request):
    error_msg = {}
    questionset = Questionset.objects.filter(status=True)
    for q in questionset:
        q.status = False
        q.save()
    error_msg['success'] = True
    error_msg['message'] = 'All questionsets turned inactive'
    return JsonResponse(error_msg)


def get_user(request):
    user = request.user
    un = user.username
    return render(request,'user.html',{'un':un,})