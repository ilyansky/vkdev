# management/commands/fill_db.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Question, Answer, Tag, QuestionLike, AnswerLike
import random

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Filling ratio')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        num_users = ratio
        num_questions = ratio * 10
        # num_answers = ratio * 100
        num_tags = ratio
        # num_likes = ratio * 200

        # Создаем пользователей
        users = []
        for i in range(num_users):
            user, created = User.objects.get_or_create(username=f'user_{i}')
            if created:
                user.set_password('password')
                user.save()
            users.append(user)

        # Создаем теги
        tags = []
        for i in range(num_tags):
            tag, created = Tag.objects.get_or_create(name=f'Tag_{i}')
            tags.append(tag)

        # Создаем вопросы
        questions = [
            Question(
                title=f'Question title {i}',
                text=f'This is the text for question {i}',
                author=random.choice(users),
                likes_count= random.randint(0, ratio * 20),
                answers_count=random.randint(0, ratio * 20)
            ) for i in range(num_questions)
        ]
        Question.objects.bulk_create(questions)

        for question in Question.objects.all():
            selected_tags = random.sample(tags, random.randint(1, len(tags)))
            question.tags.set(selected_tags)  # Используем метод set() для связи ManyToMany
            question.save()

        # Создаем ответы
        answers = []
        for question in Question.objects.all():
            for _ in range(question.answers_count):
                answers.append(Answer(
                    text=f'This is an answer for question {question.id}.',
                    question=question,
                    author=random.choice(users),
                    likes_count=random.randint(0, ratio * 20)
                ))
        Answer.objects.bulk_create(answers)

        # Обновляем поле answers для каждого вопроса
        for question in Question.objects.all():
            possible_answers = list(Answer.objects.exclude(question=question))
            selected_answers = random.sample(possible_answers, min(question.answers_count, len(possible_answers)))
            question.allanswers.set(selected_answers)  # Устанавливаем случайные ответы
            question.save()

        self.stdout.write(self.style.SUCCESS('Database successfully filled with test data'))
