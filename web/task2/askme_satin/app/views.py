from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import copy
import random

questions = []
for i in range(500):
    ans_cnt = random.randint(0, 5)
    tags_cnt = random.randint(0, 5)
    num = i + 1
    questions.append({
        'title': 'Title ' + str(num),
        'id': i,
        'text': 'This text is for question ' + str(num),
        'ans_cnt': ans_cnt,
        'ans_range': range(ans_cnt),
        'answer': 'This is answer for question ' + str(num),
        'tags_range': range(tags_cnt),
        'tag': 'Tag' + str(num)
    })

def paginate(objects_list, request, per_page=10):
    page_number = request.GET.get('page', 1)
    paginator = Paginator(objects_list, per_page)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page


def index(request):
    page = paginate(questions, request, per_page=10)

    return render(request,
                  template_name='index.html',
                  context={'questions': page.object_list,
                           'page_obj': page}
                  )


def settings(request):
    return render(request,
                  template_name='settings.html'
                  )


def hot(request):
    hot_questions = copy.deepcopy(questions)
    hot_questions.reverse()
    page = paginate(hot_questions, request, per_page=10)
    return render(request,
                  template_name='hot.html',
                  context={'questions': page.object_list,
                           'page_obj': page}
                  )


def tag(request, tag_name):
    tag_questions = copy.deepcopy(questions)
    random.shuffle(tag_questions)
    page = paginate(tag_questions, request, per_page=10)
    return render(request,
                  template_name='tag.html',
                  context={
                      'questions': page.object_list,
                      'page_obj': page,
                      'tag_name': tag_name}
                  )


def question(request, question_id):
    one_question = questions[question_id]
    return render(request,
                  template_name='question.html',
                  context={'question': one_question}
                  )


def login(request):
    return render(request,
                  template_name='login.html'
                  )


def signup(request):
    return render(request,
                  template_name='signup.html'
                  )


def ask(request):
    return render(request,
                  template_name='ask.html'
                  )
