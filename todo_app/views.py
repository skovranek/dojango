import datetime
import uuid

# from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.staticfiles.storage import staticfiles_storage
# decorators
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_protect
# login required superclass for class views
from django.contrib import messages


from todo_app.models import Category, Task, SubTask, Counter, Question, Answer, Motto
from todo_app.forms import CategoryForm, TaskForm, SubTaskForm, QuestionForm, AnswerForm, MottoForm, DateForm


class HomeView(generic.ListView):
    # access 'request' as 'self.request'
    template_name = 'home.html'
    context_object_name = 'tasks'

    def get(self, *args, **kwargs):
        if self.request.session.get('user_id') is None:
            self.request.session['user_id'] = str(uuid.uuid4())
            return redirect('introduction')
        else:
            return super(HomeView, self).get(*args, **kwargs)

    def get_queryset(self):
        if self.request.session.get('user_id') is not None:
            today = timezone.localtime(timezone.now())
            return Task.objects.filter(start__date=today).filter(user=self.request.session['user_id']).order_by('priority', 'due')

    def get_context_data(self):
        if self.request.session.get('user_id') is not None:
            context = super().get_context_data()
            questions = Question.objects.filter(date__date=timezone.localtime(timezone.now())).filter(user=self.request.session['user_id']).order_by('priority')
            if len(questions) > 0:
                context['question'] = questions[0]
            if Motto.objects.filter(user=self.request.session['user_id']).exists():
                context['motto'] = Motto.objects.filter(user=self.request.session['user_id']).latest()
            return context


def introduction(request):
    return render(request, 'introduction.html')


def archive_get(request, year, month, day):
    tasks = Task.objects.filter(start__day=day, start__month=month, start__year=year).filter(user=request.session['user_id']).order_by('priority')
    date = timezone.datetime(year, month, day)
    return render(request, 'archive.html', {'tasks': tasks, 'date': date})


@csrf_protect
def archive(request):
    if request.method == 'POST':
        if 'date' in request.POST:
            form = DateForm(request.POST)
            if form.is_valid():
                date = form.cleaned_data['date']
                day = date.day
                month = date.month
                year = date.year
        else:
            day = request.POST['day']
            month = request.POST['month']
            year = request.POST['year']
        return redirect(reverse('archive_get', args=[year, month, day]))
    else:
        return render(request, 'archive.html')


def copy_yesterday(request):
    now = timezone.localtime(timezone.now())
    yesterday = now - datetime.timedelta(1)
    tomorrow = now + datetime.timedelta(1)
    yesterday_tasks = Task.objects.filter(start__day=yesterday.day, start__month=yesterday.month, start__year=yesterday.year).filter(user=request.session['user_id'])
    if len(yesterday_tasks) > 0:
        for task in yesterday_tasks:
            # fields = ['user', 'category', 'start', 'due', 'name', 'finished', 'priority']
            data = {'user': task.user, 'category': task.category.id, 'start': now, 'due': tomorrow, 'name': task.name, 'finished': False, 'priority': task.priority}
            form = TaskForm(data)
            if form.is_valid():
                messages.success(request, 'Copied \'%s\' from yesterday.' % task)
                new_task = form.save()
                if task.subtask_set.all():
                    for subtask in task.subtask_set.all():
                        subtask_data = {'task': new_task.id, 'name': subtask.name, 'finished': False, 'priority': subtask.priority}
                        subtask_form = SubTaskForm(subtask_data)
                        if subtask_form.is_valid():
                            new_subtask = subtask_form.save()
                            if subtask.counter_set.all():
                                counter = Counter(subtask=new_subtask)
                                counter.save()
    messages.success(request, 'Done copying yesterday\'s Tasks.')
    return redirect(request.META.get('HTTP_REFERER'))


def copy_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    now = timezone.localtime(timezone.now())
    # fields = ['user', 'category', 'start', 'due', 'name', 'finished', 'priority']
    data = {'user': task.user, 'category': task.category.id, 'start': now, 'due': now + datetime.timedelta(1), 'name': task.name, 'finished': False, 'priority': task.priority}
    form = TaskForm(data)
    if form.is_valid():
            new_task = form.save()
            if task.subtask_set.all():
                for subtask in task.subtask_set.all():
                    subtask_data = {'task': new_task.id, 'name': subtask.name, 'finished': False, 'priority': subtask.priority}
                    subtask_form = SubTaskForm(subtask_data)
                    if subtask_form.is_valid():
                        new_subtask = subtask_form.save()
                        if subtask.counter_set.all():
                            counter = Counter(subtask=new_subtask)
                            counter.save()
    messages.success(request, 'Copied \'%s\' from yesterday.' % task)
    return redirect(request.META.get('HTTP_REFERER'))


def previous_days(request, days):
    now = timezone.localtime(timezone.now())
    today = timezone.make_aware(datetime.datetime(day=now.day, month=now.month, year=now.year))
    data = dict()
    for i in range(days):
        if Task.objects.filter(start__date=today-datetime.timedelta(i)).filter(user=request.session['user_id']):
            data['day_' + str(i)] = today - datetime.timedelta(i)
    # data = {str(i): today - datetime.timedelta(i) for i in range(last)}
    messages.success(request, 'Viewing which of the previous ' + str(days) + ' days had Tasks started.')
    return render(request, 'previous_days.html', {'days': days, 'data': data})


def library_get(request, object_type):
        if object_type == 'Categories & Projects':
            object_list = Category.objects.filter(user=request.session['user_id'])
        elif object_type == 'Tasks':
            object_list = Task.objects.filter(user=request.session['user_id']).order_by('category')
        elif object_type == "Unfinished Tasks":
            object_list = Task.objects.filter(user=request.session['user_id']).exclude(finished=True).order_by('category')
        elif object_type == 'Mottos':
            object_list = Motto.objects.filter(user=request.session['user_id'])
        elif object_type == 'Questions':
            object_list = Question.objects.filter(user=request.session['user_id'])
        return render(request, 'library.html', {'object_type': object_type, 'object_list': object_list})


@csrf_protect
def library(request):
    if request.method == 'POST':
        if request.POST['object_type'] == 'no_choice':
            return render(request, 'library.html')
        object_type = request.POST['object_type']
        return redirect(reverse('library_get', args=[object_type]))
    else:
        return render(request, 'library.html')


def projects_get(request, category_id):
    categories = Category.objects.filter(user=request.session['user_id']).exclude(project=False)
    project = Category.objects.get(pk=category_id)
    if request.session['user_id'] == project.user:
        return render(request, 'projects.html', {'categories': categories, 'project': project})
    else:
        messages.error(request, 'You may only view your own Projects.')
        return render(request, 'projects.html', {'categories': categories})


@csrf_protect
def projects(request):
    categories = Category.objects.filter(user=request.session['user_id']).exclude(project=False)
    if 'category_id' in request.POST:
        if request.POST['category_id'] == 'no_choice':
            return render(request, 'projects.html', {'categories': categories})
        else:
            category_id = request.POST['category_id']
            return redirect(reverse('projects_get', args=[category_id]))
    else:
        return render(request, 'projects.html', {'categories': categories})


def deadlines(request):
    now = timezone.localtime(timezone.now())
    today = timezone.make_aware(datetime.datetime(day=now.day, month=now.month, year=now.year))
    tomorrow = today + datetime.timedelta(1)
    days_left_in_week = 6 - today.weekday()
    week = today + datetime.timedelta(days_left_in_week)
    sunday_of_next_week = week + datetime.timedelta(7)
    thirty_days = today + datetime.timedelta(30)
    # after same year, more than thirty days
    future_tasks = Task.objects.filter(due__gt=today).exclude(due__year__lte=today.year).exclude(due__lte=thirty_days).filter(user=request.session['user_id']).order_by('due')
    # same year, more than thirty days
    year_tasks = Task.objects.filter(due__year=today.year).exclude(due__lte=thirty_days).filter(user=request.session['user_id']).order_by('due')
    # more than next week, less than 30 days
    thirty_days_tasks = Task.objects.filter(due__gt=sunday_of_next_week).exclude(due__month=today.month).exclude(due__gt=thirty_days).filter(user=request.session['user_id']).order_by('due')
    # same month, more than next week
    month_tasks = Task.objects.filter(due__year=today.year).filter(due__month=today.month).exclude(due__lte=sunday_of_next_week).filter(user=request.session['user_id']).order_by('due')
    # next week
    next_week_tasks = Task.objects.filter(due__gt=week).exclude(due__gt=sunday_of_next_week).filter(user=request.session['user_id']).order_by('due')
    # more than tomorrow, less than week
    week_tasks = Task.objects.filter(due__gt=tomorrow).exclude(due__gt=week).filter(user=request.session['user_id']).order_by('due')
    # tomorrow
    tomorrow_tasks = Task.objects.filter(due__date=tomorrow).filter(user=request.session['user_id']).order_by('priority')
    # today
    today_tasks = Task.objects.filter(due__date=today).filter(user=request.session['user_id']).order_by('priority')
    return render(request, 'deadlines.html', {
        'today': today,
        'tomorrow': tomorrow,
        'next_week': sunday_of_next_week,
        'today_tasks': today_tasks,
        'tomorrow_tasks': tomorrow_tasks,
        'week_tasks': week_tasks,
        'next_week_tasks': next_week_tasks,
        'month_tasks': month_tasks,
        'thirty_days_tasks': thirty_days_tasks,
        'year_tasks': year_tasks,
        'future_tasks': future_tasks
        })


@csrf_protect
def add_category(request):
    if request.method == 'POST':
        if request.session['user_id'] == request.POST['user']:
            form = CategoryForm(request.POST or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Category/Project created.')
                categories = Category.objects.filter(user=request.session['user_id'])
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                for error in form.errors:
                    for err in form.errors[error]:
                        messages.error(request, '\'' + error.capitalize() + '\'' + err)
                return render(request, 'add_pages/add_category.html')
        else:
            messages.error(request, 'You may not add Categories/Projects to other Users.', extra_tags='Easter Egg:')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'add_pages/add_category.html')


@csrf_protect
def add_task(request):
    categories = Category.objects.filter(user=request.session['user_id'])
    if request.method == 'POST':
        if request.session['user_id'] == request.POST['user']:
            form = TaskForm(request.POST or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Task created.')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                for error in form.errors:
                    for err in form.errors[error]:
                        messages.error(request, '\'' + error.capitalize() + '\' ' + err)
                return render(request, 'add_pages/add_task.html', {'categories': categories})
        else:
            messages.error(request, 'You may not add Tasks to other Users.', extra_tags='Easter Egg:')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'add_pages/add_task.html', {'categories': categories})


@csrf_protect
def add_subtask(request, task_id):
    task = Task.objects.get(pk=task_id)
    if task.user == request.session['user_id']:
        if request.method == 'POST':
            form = SubTaskForm(request.POST or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'SubTask created.')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                for error in form.errors:
                    for err in form.errors[error]:
                        messages.error(request, '\'' + error.capitalize() + '\'' + err)
                return render(request, 'add_pages/add_subtask.html', {'task': task})
        else:
            return render(request, 'add_pages/add_subtask.html', {'task': task})
    else:
        messages.error(request, 'You may only add SubTasks to your own Tasks.')
        return redirect(request.META.get('HTTP_REFERER'))


@csrf_protect
def add_counter(request, subtask_id):
    subtask = SubTask.objects.get(pk=subtask_id)
    if subtask.task.user == request.session['user_id']:
        counter = Counter(subtask=subtask)
        messages.success(request, 'Counter created.')
        counter.save()
    else:
        messages.error(request, 'You may only add Counters to your own SubTasks.')
    return redirect(request.META.get('HTTP_REFERER'))


@csrf_protect
def add_question(request):
    if request.method == 'POST':
        if request.session['user_id'] == request.POST['user']:
            form = QuestionForm(request.POST or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Question created.')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                for error in form.errors:
                    for err in form.errors[error]:
                        messages.error(request, '\'' + error.capitalize() + '\' ' + err)
                return render(request, 'add_pages/add_question.html')
        else:
            messages.error(request, 'You may not add Questions to other Users.')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'add_pages/add_question.html')


@csrf_protect
def add_answer(request, question_id):
    question = Question.objects.get(pk=question_id)
    if question.user == request.session['user_id']:
        if request.method == 'POST':
            form = AnswerForm(request.POST or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Answer created.')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                for error in form.errors:
                    for err in form.errors[error]:
                        messages.error(request, '\'' + error.capitalize() + '\' ' + err)
                return render(request, 'add_pages/add_answer.html', {'question': question})
        else:
            return render(request, 'add_pages/add_answer.html', {'question': question})
    else:
        messages.error(request, 'You may only add Answers to other your own Questions.')
        return redirect(request.META.get('HTTP_REFERER'))


@csrf_protect
def add_motto(request):
    if request.method == 'POST':
        if request.POST['user'] == request.session['user_id']:
            form = MottoForm(request.POST or None)
            if form.is_valid():
                form.save()
                messages.success(request, 'Motto created.')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                for error in form.errors:
                    for err in form.errors[error]:
                        messages.error(request, '\'' + error.capitalize() + '\' ' + err)
                return render(request, 'add_pages/add_motto.html')
        else:
            messages.error(request, 'You may not add Mottos to other Users.')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'add_pages/add_motto.html')


@csrf_protect
def edit_category(request):
    categories = Category.objects.filter(user=request.session['user_id'])
    if request.method == 'POST':
        if request.session['user_id'] == request.POST['user']:
            category = Category.objects.get(pk=request.POST['id'])
            form = CategoryForm(request.POST or None, instance=category)
            if form.is_valid():
                form.save()
                messages.success(request, 'Category/Project edited.')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                for error in form.errors:
                        for err in form.errors[error]:
                            messages.error(request, '\'' + error.capitalize() + '\'' + err)
                return render(request, 'edit_pages/edit_category.html', {'categories': categories})
        else:
            messages.error(request, 'You may not edit Categories/Projects of other Users.')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'edit_pages/edit_category.html', {'categories': categories})


@csrf_protect
def edit_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    categories = Category.objects.filter(user=request.session['user_id'])
    if request.method == 'POST':
        if request.session['user_id'] == request.POST['user'] and request.session['user_id'] == task.user:
            form = TaskForm(request.POST or None, instance=task)
            if form.is_valid():
                form.save()
                messages.success(request, 'Task edited.')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                for error in form.errors:
                        for err in form.errors[error]:
                            messages.error(request, '\'' + error.capitalize() + '\' ' + err)
                return render(request, 'edit_pages/edit_task.html', {'task': task, 'categories': categories})
        else:
            messages.error(request, 'You may not edit Tasks of other Users.', extra_tags='Easter Egg:')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'edit_pages/edit_task.html', {'task': task, 'categories': categories})


@csrf_protect
def edit_subtask(request, subtask_id):
    subtask = SubTask.objects.get(pk=subtask_id)
    if subtask.task.user == request.session['user_id']:
        if request.method == 'POST':
            form = SubTaskForm(request.POST or None, instance=subtask)
            if form.is_valid():
                form.save()
                messages.success(request, 'SubTask edited.')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                for error in form.errors:
                    for err in form.errors[error]:
                        messages.error(request, '\'' + error.capitalize() + '\'' + err)
                return render(request, 'edit_pages/edit_subtask.html', {'subtask': subtask})
        else:
            return render(request, 'edit_pages/edit_subtask.html', {'subtask': subtask})
    else:
        messages.error(request, 'You may only edit SubTasks of your own Tasks.')
        return redirect(request.META.get('HTTP_REFERER'))


@csrf_protect
def edit_question(request, question_id):
    question = Question.objects.get(pk=question_id)
    if request.method == 'POST':
        if request.session['user_id'] == request.POST['user'] and request.session['user_id'] == question.user:
            form = QuestionForm(request.POST or None, instance=question)
            if form.is_valid():
                form.save()
                messages.success(request, 'Question edited.')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                for error in form.errors:
                    for err in form.errors[error]:
                        messages.error(request, '\'' + error.capitalize() + '\' ' + err)
                return render(request, 'edit_pages/edit_question.html', {'question':question})
        else:
            messages.error(request, 'You may not edit Questions of other Users.')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'edit_pages/edit_question.html', {'question': question})


@csrf_protect
def edit_answer(request, answer_id):
    answer = Answer.objects.get(pk=answer_id)
    if answer.question.user == request.session['user_id']:
        if request.method == 'POST':
            form = AnswerForm(request.POST or None, instance=answer)
            if form.is_valid():
                form.save()
                messages.success(request, 'Answer edited.')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                for error in form.errors:
                    for err in form.errors[error]:
                        messages.error(request, '\'' + error.capitalize() + '\' ' + err)
                return render(request, 'edit_pages/edit_answer.html', {'answer': answer})
        else:
            return render(request, 'edit_pages/edit_answer.html', {'answer': answer})
    else:
        messages.error(request, 'You may not edit Answers of other Users.')
        return redirect(request.META.get('HTTP_REFERER'))


@csrf_protect
def edit_motto(request):
    mottos = Motto.objects.filter(user=request.session['user_id'])
    if request.method == 'POST':
        motto = Motto.objects.get(pk=request.POST['id'])
        if request.session['user_id'] == request.POST['user'] and request.session['user_id'] == motto.user:
            form = MottoForm(request.POST or None, instance=motto)
            if form.is_valid():
                form.save()
                messages.success(request, 'Motto edited.')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                for error in form.errors:
                    for err in form.errors[error]:
                        messages.error(request, '\'' + error.capitalize() + '\' ' + err)
                return render(request, 'edit_pages/edit_motto.html', {'mottos': mottos})
        else:
            messages.error(request, 'You may not edit Mottos of other Users.')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'edit_pages/edit_motto.html', {'mottos': mottos})


@csrf_protect
def delete(request):
    if request.method == 'POST':
        if request.POST['id']:
            if request.POST['object_type'] == 'category':
                category = Category.objects.get(pk=request.POST['id'])
                if request.session['user_id'] == category.user:
                    category.delete()
                    messages.success(request, '\'%s\' deleted.' % category)
                else:
                    messages.error(request, 'You may only delete your own Categories/Projects.')
            elif request.POST['object_type'] == 'task':
                task = Task.objects.get(pk=request.POST['id'])
                if request.session['user_id'] == task.user:
                    task.delete()
                    messages.success(request, '\'%s\' deleted.' % task)
                else:
                    messages.error(request, 'You may only delete your own Tasks.')
            elif request.POST['object_type'] == 'subtask':
                subtask = SubTask.objects.get(pk=request.POST['id'])
                if request.session['user_id'] == subtask.task.user:
                    subtask.delete()
                    messages.success(request, '\'%s\' deleted.' % subtask)
                else:
                    messages.error(request, 'You may only delete your own SubTasks.')
            elif request.POST['object_type'] == 'counter':
                counter = Counter.objects.get(pk=request.POST['id'])
                if request.session['user_id'] == counter.subtask.task.user:
                    counter.delete()
                    messages.success(request, '\'%s\' Counter deleted.' % counter.subtask)
                else:
                    messages.error(request, 'You may only delete your own Counters.')
            elif request.POST['object_type'] == 'question':
                question = Question.objects.get(pk=request.POST['id'])
                if request.session['user_id'] == question.user:
                    question.delete()
                    messages.success(request, '\'%s\' deleted.' % question)
                else:
                    messages.error(request, 'You may only delete your own Questions.')
            elif request.POST['object_type'] == 'answer':
                answer = Answer.objects.get(pk=request.POST['id'])
                if request.session['user_id'] == answer.question.user:
                    answer.delete()
                    messages.success(request, '\'%s\' deleted.' % answer)
                else:
                    messages.error(request, 'You may only delete your own Answers.')
            elif request.POST['object_type'] == 'motto':
                motto = Motto.objects.get(pk=request.POST['id'])
                if request.session['user_id'] == motto.user:
                    motto.delete()
                    messages.success(request, '\'%s\' deleted.' % motto)
                else:
                    messages.error(request, 'You may only delete your own Mottos.')
            else:
                messages.error(request, 'No object specified for deletion.')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'No object id specified for deletion.')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))


@csrf_protect
def delete_category(request):
    categories = Category.objects.filter(user=request.session['user_id'])
    return render(request, 'delete_category.html', {'categories': categories})


def task_finished(request, task_id):
    task = Task.objects.get(pk=task_id)
    if task.user == request.session['user_id']:
        task.finished = True
        task.save()
        messages.success(request, '%s finished.' % task)
    else:
        messages.error(request, 'You may not edit the Tasks of other Users.')
    return redirect(request.META.get('HTTP_REFERER'))


def task_not_finished(request, task_id):
    task = Task.objects.get(pk=task_id)
    if task.user == request.session['user_id']:
        task.finished = False
        task.save()
        messages.success(request, '%s not finished.' % task)
    else:
        messages.error(request, 'You may not edit the Tasks of other Users.')
    return redirect(request.META.get('HTTP_REFERER'))


def subtask_finished(request, subtask_id):
    subtask = SubTask.objects.get(pk=subtask_id)
    if subtask.task.user == request.session['user_id']:
        subtask.finished = True
        subtask.save()
        messages.success(request, '%s finished.' % subtask)
    else:
        messages.error(request, 'You may not edit the SubTasks of other Users.')
    return redirect(request.META.get('HTTP_REFERER'))


def subtask_not_finished(request, subtask_id):
    subtask = SubTask.objects.get(pk=subtask_id)
    if subtask.task.user == request.session['user_id']:
        subtask.finished = False
        subtask.save()
        messages.success(request, '%s not finished.' % subtask)
    else:
        messages.error(request, 'You may not edit the SubTasks of other Users.')
    return redirect(request.META.get('HTTP_REFERER'))


def increment_counter(request, counter_id):
    counter = Counter.objects.get(pk=counter_id)
    if counter.subtask.task.user == request.session['user_id']:
        counter.increment()
        counter.save()
    else:
        messages.error(request, 'You may only increment your own Counters.')
    return redirect(request.META.get('HTTP_REFERER'))


def decrement_counter(request, counter_id):
    counter = Counter.objects.get(pk=counter_id)
    if counter.subtask.task.user == request.session['user_id']:
        counter.decrement()
        counter.save()
    else:
        messages.error(request, 'You may only decrement your own Counters.')
    return redirect(request.META.get('HTTP_REFERER'))


def task_priority_increment(request, task_id):
    task = Task.objects.get(pk=task_id)
    if task.user == request.session['user_id']:
        task.increment()
        task.save()
    else:
        messages.error(request, 'You may only increment the priority of your own Tasks.')
    return redirect(request.META.get('HTTP_REFERER'))


def task_priority_decrement(request, task_id):
    task = Task.objects.get(pk=task_id)
    if task.user == request.session['user_id']:
        task.decrement()
        task.save()
    else:
        messages.error(request, 'You may only decrement the priority of your own Tasks.')
    return redirect(request.META.get('HTTP_REFERER'))


def subtask_priority_increment(request, subtask_id):
    subtask = SubTask.objects.get(pk=subtask_id)
    if subtask.task.user == request.session['user_id']:
        subtask.increment()
        subtask.save()
    else:
        messages.error(request, 'You may only increment the priority of your own SubTasks.')
    return redirect(request.META.get('HTTP_REFERER'))


def subtask_priority_decrement(request, subtask_id):
    subtask = SubTask.objects.get(pk=subtask_id)
    if subtask.task.user == request.session['user_id']:
        subtask.decrement()
        subtask.save()
    else:
        messages.error(request, 'You may only decrement the priority of your own SubTasks.')
    return redirect(request.META.get('HTTP_REFERER'))


def question_priority_increment(request, question_id):
    question = Question.objects.get(pk=question_id)
    if question.user == request.session['user_id']:
        question.increment()
        question.save()
    else:
        messages.error(request, 'You may only increment the priority of your own Questions.')
    return redirect(request.META.get('HTTP_REFERER'))


def question_priority_decrement(request, question_id):
    question = Question.objects.get(pk=question_id)
    if question.user == request.session['user_id']:
        question.decrement()
        question.save()
    else:
        messages.error(request, 'You may only decrement the priority of your own Questions.')
    return redirect(request.META.get('HTTP_REFERER'))
