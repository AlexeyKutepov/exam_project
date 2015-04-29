from django.core.exceptions import SuspiciousOperation
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import Context
from django.template.loader import get_template
from exam.models import Category, Test, TestImage, Progress, Journal
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from exam.exam_test.exam_test import *
from django.utils import timezone
import pickle


def index(request):
    return render(request, "exam/index.html")


def prepare_test_html(id):
    """
    Prepares the interactive html-file containing test for download
    :param id: id of the test
    :return:
    """
    test = Test.objects.get(id=id)
    if test.test:
        exem_test = pickle.loads(test.test)
    else:
        exem_test = None

    template = get_template("exam/test_template.html")
    context = Context(
        {
            "test": test,
            "question_list": exem_test.get_questions()
        }
    )
    html = template.render(context)

    response = HttpResponse(html, content_type='application/html')
    response['Content-Disposition'] = 'attachment; filename="test_' + str(id) + '.html"'

    return response

@login_required(login_url='/')
def dashboard(request):
    if "delete" in request.POST:
        Test.objects.get(id=int(request.POST["delete"])).delete()
        request.user.rating -= 10
        request.user.save()
        return HttpResponseRedirect(reverse('dashboard'))
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


def get_test_list(request):
    if "search" in request.GET:
        search_query = request.GET["search"]
        query_set = Q()
        for term in search_query.split():
            query_set |= Q(name__contains=term)
        test_list = Test.objects.filter(query_set)
    else:
        test_list = Test.objects.order_by('-date_and_time', '-rating')
    return render(request, "exam/test_list.html", {"test_list": test_list})


def start_test(request):
    """
    Starts selected test

    :param request: request for starting test
    :return: start_test.html
    """

    if "run" in request.POST:
        test = Test.objects.get(id=int(request.POST["run"]))
        if test.test:
            exem_test = pickle.loads(test.test)
            number_of_questions = len(exem_test.get_questions())
        else:
            number_of_questions = 0
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
            progress.current_result=0
            progress.save()
        return render(
            request,
            "exam/start_test.html",
            {
                "test": test,
                "number_of_questions": number_of_questions
            }
        )
    else:
        return HttpResponseRedirect(reverse("get_test_list"))


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
    exem_test = pickle.loads(test.test)

    if not progress.result_list:
        if number > 1:
            return HttpResponseRedirect(reverse("next_question", args=[test.id, 1]))
    else:
        result_list = pickle.loads(progress.result_list)
        if len(result_list) > number - 1:
            return HttpResponseRedirect(reverse("next_question", args=[test.id, len(result_list) + 1]))
        elif len(result_list) + 1 < number:
            return HttpResponseRedirect(reverse("next_question", args=[test.id, len(result_list) + 1]))
        elif number > len(exem_test.get_questions()):
            return HttpResponseRedirect(reverse("get_test_list"))


    question = exem_test.get_questions()[number - 1]

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

        if number == len(exem_test.get_questions()):
            progress.end_date = timezone.now()
            progress.save()

            result_of_test = int(100/len(exem_test.get_questions()) * progress.current_result)
            journal = Journal.objects.create(
                user=request.user,
                test=test,
                start_date=progress.start_date,
                end_date=progress.end_date,
                number_of_questions=len(exem_test.get_questions()),
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

    progress = 100/len(exem_test.get_questions()) * (number - 1)
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
        return render(request, "exam/create_new_test.html", {"category_list": category_list})


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
    type_list = [
            "Содержит один или несколько правильных вариантов ответа",
            "Содержит только один правильный вариант ответа",
            "Вопрос со свободной формой ответа",
        ]
    if "type" in request.POST and int(request.POST["type"]) in (1, 2, 3):
        if test.test is None or test.test == b'':
            exem_test = ExamTest()
        else:
            exem_test = pickle.loads(test.test)
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

        exem_test.add_question(question)
        test.test = pickle.dumps(exem_test)
        test.save()
        request.user.rating += 1
        request.user.save()
        if "complete" in request.POST:
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return render(
                request,
                "exam/create_new_question.html",
                {
                    "number_of_question": len(exem_test.get_questions()) + 1,
                    "type_list": type_list,
                    "test_id": id
                }
            )
    else:
        return render(
            request,
            "exam/create_new_question.html",
            {
                "type_list": type_list,
                "test_id": id
            }
        )