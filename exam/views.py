from django.core.exceptions import SuspiciousOperation
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from exam.models import Category, Test, TestImage, Progress
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from exam.exam_test.exam_test import *
from django.utils import timezone
import pickle


def index(request):
    return render(request, "exam/index.html")


@login_required(login_url='/')
def dashboard(request):
    if "delete" in request.POST:
        Test.objects.get(id=int(request.POST["delete"])).delete()
    test_list = Test.objects.filter(author=request.user)
    return render(request, "exam/dashboard.html", {"test_list": test_list})


def get_test_list(request):
    test_list = Test.objects.all()
    return render(request, "exam/test_list.html", {"test_list": test_list})


def start_test(request):
    """
    Starts selected test

    :param request: request for starting test
    :return: start_test_page.html
    """

    if "run" in request.POST:
        test = Test.objects.get(id=int(request.POST["run"]))
        if test.test:
            exem_test = pickle.loads(test.test)
            number_of_questions = len(exem_test.get_questions())
        else:
            number_of_questions = None
        progress = Progress.objects.filter(user=request.user, test=test)
        if not progress:
            Progress.objects.get_or_create(
                user=request.user,
                start_date=timezone.now(),
                end_date=None,
                test=test,
                current_result=None
            )
        else:
            progress.start_date = timezone.now()
            progress.end_date = None
            progress.current_result = None
        return render(
            request,
            "exam/start_test_page.html",
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

    if not progress.current_result:
        if (number == 1 and not ("answer" in request.POST)) or (number > 1):
            return HttpResponseRedirect(reverse("next_question", args=[test.id, 0]))
    else:
        result_list = pickle.loads(progress.current_result)
        if len(result_list) > number:
            return HttpResponseRedirect(reverse("next_question", args=[test.id, len(result_list)]))
        elif (len(result_list) + 1 == number and not ("answer" in request.POST)) or (len(result_list) + 1 < number):
            return HttpResponseRedirect(reverse("next_question", args=[test.id, len(result_list)]))

    if "answer" in request.POST:
        result_list.append(
            ""
        )
        progress.current_result = pickle.dumps(result_list)
        progress.save()
        number += 1
        return HttpResponseRedirect(reverse("next_question", args=[test.id, number]))

    exem_test = pickle.loads(test.test)
    question = exem_test.get_questions()[number]
    progress = 100/len(exem_test.get_questions()) * number
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
            "Вопрос со свободной формой ответа"
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