from django.core.exceptions import SuspiciousOperation
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import Context
from django.template.loader import get_template
from exam.models import Category, Test, TestImage, Progress, Journal, UnregisteredUser
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from exam.exam_test.exam_test import *
from django.utils import timezone
import pickle
import math


TYPE_LIST = [
            "Содержит один или несколько правильных вариантов ответа",
            "Содержит только один правильный вариант ответа",
            "Вопрос со свободной формой ответа",
        ]

def prepare_test_html(id):
    """
    Prepares the interactive html-file containing test for download
    :param id: id of the test
    :return:
    """
    test = Test.objects.get(id=id)
    if test.test:
        exam_test = pickle.loads(test.test)
    else:
        exam_test = None

    template = get_template("exam/test_template.html")
    context = Context(
        {
            "test": test,
            "question_list": exam_test.get_questions()
        }
    )
    html = template.render(context)

    response = HttpResponse(html, content_type='application/html')
    response['Content-Disposition'] = 'attachment; filename="test_' + str(id) + '.html"'

    return response


def index(request):
    """
    Index page
    :param request:
    :return:
    """
    return render(request, "exam/index.html")

@login_required(login_url='/')
def dashboard(request):
    if "delete" in request.POST:
        Test.objects.get(id=int(request.POST["delete"])).delete()
        request.user.rating -= 10
        request.user.save()
        return HttpResponseRedirect(reverse('dashboard'))
    elif "edit" in request.POST:
        return HttpResponseRedirect(reverse("edit_test", args=[request.POST["edit"]]))
    elif "journal" in request.POST:
        return HttpResponseRedirect(reverse("journal", args=[request.POST["journal"]]))
    elif "save" in request.POST:
        return prepare_test_html(int(request.POST["save"]))
    else:
        test_list = Test.objects.filter(author=request.user)
        return render(
            request,
            "exam/dashboard.html",
            {
                "dashboard": True,
                "test_list": test_list
            }
        )

@login_required(login_url='/')
def dashboard_results(request):
    journal_list = Journal.objects.filter(user=request.user)
    return render(
        request,
        "exam/dashboard.html",
        {
            "dashboard": False,
            "journal_list": journal_list
        }
    )


@login_required(login_url='/')
def journal(request, id):
    if "delete" in request.POST:
        Journal.objects.get(id=int(request.POST["delete"])).delete()
        return HttpResponseRedirect(reverse('journal', args=[id]))
    else:
        test = Test.objects.get(id=id)
        journal_list = Journal.objects.filter(test=test)
        return render(
            request,
            "exam/journal.html",
            {
                "test": test,
                "journal_list": journal_list
            }
        )


def get_test_list_search(request, page, search):
    """
    Renders test list page with search query
    :param request: request
    :param page: current page
    :param search: search query
    :return:
    """
    page = int(page)
    if page < 1:
        return HttpResponseRedirect(reverse("get_test_list_search", args=[1, search]))
    query_set = Q()
    query_set |= Q(name__contains=search)
    test_list = Test.objects.filter(query_set)
    number_of_pages = math.ceil(len(test_list) / 20)

    if page > number_of_pages:
        return HttpResponseRedirect(reverse("get_test_list_search", args=[number_of_pages, search]))

    a = (page - 1) * 20
    b = page * 20

    start_page = int((page-1)/10) * 10
    end_page = start_page + 10
    if end_page > number_of_pages:
        end_page = number_of_pages
    return render(
        request,
        "exam/test_list.html",
        {
            "test_list": test_list[a: b],
            "search_query": search,
            "number_of_pages": [i+1 for i in range(start_page, end_page)],
            "current_page": page,
            "start_test_number": a
        }
    )


def get_test_list(request, page):
    """
    Renders test list page
    :param request: request
    :param page: current page
    :return:
    """
    page = int(page)
    if page < 1:
        return HttpResponseRedirect(reverse("get_test_list", args=[1]))
    search_query = None
    if "search" in request.GET:
        search_query = request.GET["search"]
        query_set = Q()
        query_set |= Q(name__contains=search_query)
        test_list = Test.objects.filter(query_set)
        number_of_pages = math.ceil(len(test_list) / 20)
    else:
        test_list = Test.objects.order_by('-date_and_time', '-rating')
        number_of_pages = math.ceil(len(test_list) / 20)
    if number_of_pages == 0:
        return render(
            request,
            "exam/test_list.html",
            {
                "test_list": None,
                "search_query": search_query,
                "number_of_pages": 1,
                "current_page": page,
                "start_test_number": 0
            }
        )
    if page > number_of_pages:
        return HttpResponseRedirect(reverse("get_test_list", args=[number_of_pages]))

    a = (page - 1) * 20
    b = page * 20

    start_page = int((page-1)/10) * 10
    end_page = start_page + 10
    if end_page > number_of_pages:
        end_page = number_of_pages
    return render(
        request,
        "exam/test_list.html",
        {
            "test_list": test_list[a: b],
            "search_query": search_query,
            "number_of_pages": [i+1 for i in range(start_page, end_page)],
            "current_page": page,
            "start_test_number": a
        }
    )


def start_test(request):
    """
    Starts selected test

    :param request: request for starting test
    :return: start_test.html
    """

    if "run" in request.POST:
        test = Test.objects.get(id=int(request.POST["run"]))
        if test.test:
            exam_test = pickle.loads(test.test)
            number_of_questions = len(exam_test.get_questions())
        else:
            number_of_questions = 0
        if request.user.is_authenticated():
            progress = Progress.objects.filter(user=request.user, test=test)
            if not progress:
                Progress.objects.get_or_create(
                    user=request.user,
                    start_date=timezone.now(),
                    end_date=None,
                    test=test,
                    result_list=None,
                    current_result=0
                )
            else:
                progress = progress[0]
                progress.start_date = timezone.now()
                progress.end_date = None
                progress.result_list = None
                progress.current_result = 0
                progress.save()
        return render(
            request,
            "exam/start_test.html",
            {
                "test": test,
                "number_of_questions": number_of_questions
            }
        )
    elif "start" and "email" and "firstName" and "lastName" in request.POST:
        test = Test.objects.get(id=int(request.POST["start"]))
        middle_name = None
        if "middleName" in request.POST:
            middle_name = request.POST["middleName"]
        unregistered_user = UnregisteredUser.objects.get_or_create(
            email=request.POST["email"],
            first_name=request.POST["firstName"],
            middle_name=middle_name,
            last_name=request.POST["lastName"]
        )
        progress = Progress.objects.filter(unregistered_user=unregistered_user[0], test=test)
        if not progress or len(progress) < 1:
                progress = Progress.objects.get_or_create(
                    unregistered_user=unregistered_user[0],
                    start_date=timezone.now(),
                    end_date=None,
                    test=test,
                    result_list=None,
                    current_result=0
                )
        else:
            progress[0].start_date = timezone.now()
            progress[0].end_date = None
            progress[0].result_list = None
            progress[0].current_result = 0
            progress[0].save()
        return HttpResponseRedirect(reverse("next_question_unregistered_user", args=[test.id, progress[0].id, 1]))
    else:
        return HttpResponseRedirect(reverse("get_test_list", args=[1]))


def next_question_unregistered_user(request, id, progress_id, number):
    """
    Shows the next question to unregistered user
    :param request:
    :param id:
    :param progress:
    :param number:
    :return:
    """
    id = int(id)
    progress_id = int(progress_id)
    number = int(number)
    test = Test.objects.get(id=id)
    progress = Progress.objects.get(id=progress_id)
    result_list = []
    exam_test = pickle.loads(test.test)

    if not progress.result_list:
        if number > 1:
            return HttpResponseRedirect(reverse("next_question_unregistered_user", args=[test.id, progress_id, 1]))
    else:
        result_list = pickle.loads(progress.result_list)
        if len(result_list) > number - 1:
            return HttpResponseRedirect(reverse("next_question_unregistered_user", args=[test.id, progress_id, len(result_list) + 1]))
        elif len(result_list) + 1 < number:
            return HttpResponseRedirect(reverse("next_question_unregistered_user", args=[test.id, progress_id, len(result_list) + 1]))
        elif number > len(exam_test.get_questions()):
            return HttpResponseRedirect(reverse("get_test_list", args=[1]))

    question = exam_test.get_questions()[number - 1]

    if "answer" in request.POST:
        is_correct = True
        if question.get_test_type() is TestType.OPEN_TYPE:
            if question.get_answers().get_answer() != request.POST["answer"]:
                is_correct = False
        elif question.get_test_type() is TestType.CLOSE_TYPE_SEVERAL_CORRECT_ANSWERS:
            correct_answer_list = []
            for item in range(len(question.get_answers())):
                if question.get_answers()[item].is_correct():
                    correct_answer_list.append(str(item + 1))
            is_correct = correct_answer_list == request.POST.getlist("answer")
        elif question.get_test_type() is TestType.CLOSE_TYPE_ONE_CORRECT_ANSWER:
            correct_answer = 1
            for item in range(len(question.get_answers())):
                if question.get_answers()[item].is_correct():
                    correct_answer = item + 1
                    break
            is_correct = str(correct_answer) == request.POST["answer"]

        if is_correct:
            progress.current_result += 1
        result_list.append(
            ExamResult(
                is_correct=is_correct,
                answer=request.POST["answer"]
            )
        )
        progress.result_list = pickle.dumps(result_list)
        progress.save()

        if number == len(exam_test.get_questions()):
            progress.end_date = timezone.now()
            progress.save()

            result_of_test = int(100/len(exam_test.get_questions()) * progress.current_result)
            journal = Journal.objects.create(
                unregistered_user=progress.unregistered_user,
                test=test,
                start_date=progress.start_date,
                end_date=progress.end_date,
                number_of_questions=len(exam_test.get_questions()),
                number_of_correct_answers=progress.current_result,
                result=result_of_test,
                report=progress.result_list
            )

            test.rating += 1
            test.save()

            return HttpResponseRedirect(reverse("end_test", args=[journal.id]))
        else:
            number += 1
            return HttpResponseRedirect(reverse("next_question_unregistered_user", args=[test.id, progress_id, number]))

    progress_value = 100/len(exam_test.get_questions()) * (number - 1)
    answers = question.get_answers()
    if question.get_image():
        image_test = TestImage.objects.get(id=question.get_image())
        image = image_test.image.url
    else:
        image = None
    if question.get_test_type() != TestType.OPEN_TYPE:
        variant_list = []
        for answer in answers:
            variant_list.append(answer.get_answer())
    else:
        variant_list = None

    return render(
        request,
        "exam/next_question.html",
        {
            "test_id": id,
            "progress": progress_value,
            "progress_id": progress_id,
            "number_of_question": number,
            "question": question.get_question(),
            "type": question.get_test_type().value,
            "variant_list": variant_list,
            "image": image
        }
    )

@login_required(login_url='/')
def next_question(request, id, number):
    """
    Shows next question
    :param request:
    :param id: - id of test
    :param number: number of question
    :return:
    """
    id = int(id)
    number = int(number)
    test = Test.objects.get(id=id)
    progress = Progress.objects.filter(user=request.user, test=test)[0]
    result_list = []
    exam_test = pickle.loads(test.test)

    if not progress.result_list:
        if number > 1:
            return HttpResponseRedirect(reverse("next_question", args=[test.id, 1]))
    else:
        result_list = pickle.loads(progress.result_list)
        if len(result_list) > number - 1:
            return HttpResponseRedirect(reverse("next_question", args=[test.id, len(result_list) + 1]))
        elif len(result_list) + 1 < number:
            return HttpResponseRedirect(reverse("next_question", args=[test.id, len(result_list) + 1]))
        elif number > len(exam_test.get_questions()):
            return HttpResponseRedirect(reverse("get_test_list", args=[1]))


    question = exam_test.get_questions()[number - 1]

    if "answer" in request.POST:
        is_correct = True
        if question.get_test_type() is TestType.OPEN_TYPE:
            if question.get_answers().get_answer() != request.POST["answer"]:
                is_correct = False
        elif question.get_test_type() is TestType.CLOSE_TYPE_SEVERAL_CORRECT_ANSWERS:
            correct_answer_list = []
            for item in range(len(question.get_answers())):
                if question.get_answers()[item].is_correct():
                    correct_answer_list.append(str(item + 1))
            is_correct = correct_answer_list == request.POST.getlist("answer")
        elif question.get_test_type() is TestType.CLOSE_TYPE_ONE_CORRECT_ANSWER:
            correct_answer = 1
            for item in range(len(question.get_answers())):
                if question.get_answers()[item].is_correct():
                    correct_answer = item + 1
                    break
            is_correct = str(correct_answer) == request.POST["answer"]

        if is_correct:
            progress.current_result += 1
        result_list.append(
            ExamResult(
                is_correct=is_correct,
                answer=request.POST["answer"]
            )
        )
        progress.result_list = pickle.dumps(result_list)
        progress.save()

        if number == len(exam_test.get_questions()):
            progress.end_date = timezone.now()
            progress.save()

            result_of_test = int(100/len(exam_test.get_questions()) * progress.current_result)
            journal = Journal.objects.create(
                user=request.user,
                test=test,
                start_date=progress.start_date,
                end_date=progress.end_date,
                number_of_questions=len(exam_test.get_questions()),
                number_of_correct_answers=progress.current_result,
                result=result_of_test,
                report=progress.result_list
            )

            test.rating += 1
            test.save()
            request.user.rating += 1
            request.user.save()

            return HttpResponseRedirect(reverse("end_test", args=[journal.id]))
        else:
            number += 1
            return HttpResponseRedirect(reverse("next_question", args=[test.id, number]))

    progress = 100/len(exam_test.get_questions()) * (number - 1)
    answers = question.get_answers()
    if question.get_image():
        image_test = TestImage.objects.get(id=question.get_image())
        image = image_test.image.url
    else:
        image = None
    if question.get_test_type() != TestType.OPEN_TYPE:
        variant_list = []
        for answer in answers:
            variant_list.append(answer.get_answer())
    else:
        variant_list = None

    return render(
        request,
        "exam/next_question.html",
        {
            "test_id": id,
            "progress": progress,
            "number_of_question": number,
            "question": question.get_question(),
            "type": question.get_test_type().value,
            "variant_list": variant_list,
            "image": image
        }
    )


def end_test(request, id):
    """
    Renders simple result form (without detail report)
    :param request:
    :param id: id of Journal field
    :return: end_test.html
    """
    journal = Journal.objects.get(id=id)
    if not journal:
        raise SuspiciousOperation("Некорректный запрос")
    elif not request.user.is_authenticated() and journal.user:
        raise SuspiciousOperation("Некорректный запрос")
    return render(
        request,
        "exam/end_test.html",
        {
            "journal": journal,
            "time_for_test": journal.end_date - journal.start_date
        }
    )



@login_required(login_url='/')
def create_new_test(request):
    """
    Creates new test,
    :param request:
    :return:
    """
    if "name" and "description" and "category" in request.POST:
        category = Category.objects.get(name=request.POST["category"])
        if "isPublic" in request.POST and request.POST["isPublic"] == 'public':
            is_public = True
        else:
            is_public = False
        test = Test.objects.create(
            name=request.POST["name"],
            description=request.POST["description"],
            category=category,
            author=request.user,
            is_public=is_public,
        )
        request.user.rating += 10
        request.user.save()
        return HttpResponseRedirect(reverse("create_new_question", args=[test.id]))
    else:
        category_list = Category.objects.all()
        return render(request, "exam/create_test.html", {"category_list": category_list})


@login_required(login_url='/')
def create_new_question(request, id):
    """
    Creates new question of the test of id
    :param request:
    :param id: id of the test
    :return:
    """
    test = Test.objects.get(id=id)
    if request.user != test.author:
        raise SuspiciousOperation("Некорректный id теста")
    if "type" in request.POST and int(request.POST["type"]) in (1, 2, 3):
        if test.test is None or test.test == b'':
            exam_test = ExamTest()
        else:
            exam_test = pickle.loads(test.test)
        question_type = TestType(int(request.POST["type"]))

        if "question" in request.POST:
            question = Question(request.POST["question"], question_type)
        else:
            question = Question(None, question_type)

        if "image" in request.FILES:
            image = TestImage.objects.get_or_create(image=request.FILES["image"])
            image_id = image[0].id
        else:
            image_id = None
        question.set_image(image_id)

        if question_type is TestType.CLOSE_TYPE_SEVERAL_CORRECT_ANSWERS:
            i = 1
            while "answer"+str(i) in request.POST:
                question.add_new_answer(
                    CloseAnswer(
                        answer=request.POST["answer"+str(i)],
                        is_correct=str(i) in request.POST.getlist("trueAnswer")
                    )
                )
                i += 1
        elif question_type is TestType.CLOSE_TYPE_ONE_CORRECT_ANSWER:
            i = 1
            while "answer"+str(i) in request.POST:
                question.add_new_answer(
                    CloseAnswer(
                        answer=request.POST["answer"+str(i)],
                        is_correct=str(i) == request.POST["trueAnswer"]
                    )
                )
                i += 1
        elif question_type is TestType.OPEN_TYPE:
            question.add_new_answer(
                Answer(
                    request.POST["openAnswer"]
                )
            )

        exam_test.add_question(question)
        test.test = pickle.dumps(exam_test)
        test.save()
        request.user.rating += 1
        request.user.save()
        if "complete" in request.POST:
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return render(
                request,
                "exam/create_question.html",
                {
                    "number_of_question": len(exam_test.get_questions()) + 1,
                    "type_list": TYPE_LIST,
                    "test_id": id
                }
            )
    else:
        return render(
            request,
            "exam/create_question.html",
            {
                "type_list": TYPE_LIST,
                "test_id": id
            }
        )

@login_required(login_url='/')
def edit_test(request, id):
    id = int(id)
    test = Test.objects.get(id=id)
    category_list = Category.objects.all()

    if "save" in request.POST:
        category = Category.objects.get(name=request.POST["category"])
        if "isPublic" in request.POST and request.POST["isPublic"] == 'public':
            is_public = True
        else:
            is_public = False

        test.name = request.POST["name"]
        test.description = request.POST["description"]
        test.category = category
        test.is_public = is_public
        test.save()
        return HttpResponseRedirect(reverse("dashboard"))

    if test.test:
        exam_test = pickle.loads(test.test)
        if "delete" in request.POST:
            exam_test.get_questions().pop(int(request.POST["delete"]) - 1)
            test.test = pickle.dumps(exam_test)
            test.save()
        question_list = exam_test.get_questions()
    else:
        question_list = None

    return render(
            request,
            "exam/edit_test.html",
            {
                "test": test,
                "category_list": category_list,
                "question_list": question_list
            }
        )


def add_question(request, id):
    test = Test.objects.get(id=id)
    if test.test is None or test.test == b'':
        exam_test = ExamTest()
    else:
        exam_test = pickle.loads(test.test)

    if request.user != test.author:
        raise SuspiciousOperation("Некорректный id теста")
    if "type" in request.POST and int(request.POST["type"]) in (1, 2, 3):
        question_type = TestType(int(request.POST["type"]))

        if "question" in request.POST:
            question = Question(request.POST["question"], question_type)
        else:
            question = Question(None, question_type)

        if "image" in request.FILES:
            image = TestImage.objects.get_or_create(image=request.FILES["image"])
            image_id = image[0].id
        else:
            image_id = None
        question.set_image(image_id)

        if question_type is TestType.CLOSE_TYPE_SEVERAL_CORRECT_ANSWERS:
            i = 1
            while "answer"+str(i) in request.POST:
                question.add_new_answer(
                    CloseAnswer(
                        answer=request.POST["answer"+str(i)],
                        is_correct=str(i) in request.POST.getlist("trueAnswer")
                    )
                )
                i += 1
        elif question_type is TestType.CLOSE_TYPE_ONE_CORRECT_ANSWER:
            i = 1
            while "answer"+str(i) in request.POST:
                question.add_new_answer(
                    CloseAnswer(
                        answer=request.POST["answer"+str(i)],
                        is_correct=str(i) == request.POST["trueAnswer"]
                    )
                )
                i += 1
        elif question_type is TestType.OPEN_TYPE:
            question.add_new_answer(
                Answer(
                    request.POST["openAnswer"]
                )
            )

        exam_test.add_question(question)
        test.test = pickle.dumps(exam_test)
        test.save()
        request.user.rating += 1
        request.user.save()

        return HttpResponseRedirect(reverse("edit_test", args=[id]))
    else:

        return render(
            request,
            "exam/question_editor.html",
            {
                "number_of_question": len(exam_test.get_questions()) + 1,
                "operation": "edit_test_add_question",
                "type_list": TYPE_LIST,
                "test_id": id
            }
        )


def edit_question(request, id, number):
    return None