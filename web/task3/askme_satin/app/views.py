from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Question, Tag

# Функция для пагинации
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

# Главная страница с новыми вопросами
def index(request):
    questions = Question.objects.newest()
    page = paginate(questions, request, per_page=10)
    return render(request, 'index.html', {'questions': page.object_list, 'page_obj': page})

# Страница с популярными вопросами
def hot(request):
    questions = Question.objects.best()
    page = paginate(questions, request, per_page=10)
    return render(request, 'hot.html', {'questions': page.object_list, 'page_obj': page})

# Страница вопросов по тегу
def tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    questions = tag.questions.all()
    page = paginate(questions, request, per_page=10)
    return render(request, 'tag.html', {'questions': page.object_list, 'page_obj': page, 'tag_name': tag_name})

# Страница одного вопроса
def question(request, question_id):
    one_question = get_object_or_404(Question, id=question_id)
    answers = one_question.allanswers.all()

    paginator = Paginator(answers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'question.html', {
        'question': one_question,
        'answers': page_obj.object_list,
        'page_obj': page_obj
    })


# Страница настроек
def settings(request):
    return render(request, 'settings.html')

# Страница входа
def login(request):
    return render(request, 'login.html')

# Страница регистрации
def signup(request):
    return render(request, 'signup.html')

# Страница для создания нового вопроса
def ask(request):
    return render(request, 'ask.html')
