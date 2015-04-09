from django.core.exceptions import SuspiciousOperation
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from exam.models import Category, Test, TestImage
from django.http import HttpResponseRedirect
import pickle


def index(request):
    return render(request, "exam/index.html")


@login_required(login_url='/')
def dashboard(request):
    return render(request, "exam/dashboard.html")

@login_required(login_url='/')
def create_new_test(request):
    """
    Creates new test,
    :param request:
    :return:
    """
    if "name" and "description" and "category" in request.POST:
        category = Category.objects.get(name=request.POST["category"])
        if request.POST["isPublic"] == 'public':
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
        return HttpResponseRedirect("/create_new_question/" + str(test.id) + "/")
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
            json_test = []
        else:
            json_test = pickle.loads(test.test)
        question_type = int(request.POST["type"])
        image = TestImage.objects.get_or_create(image=request.FILES["image"])
        answers = None
        if question_type == 1:
            answers = []
            i = 1
            while ("answer"+str(i) in request.POST):
                answers.append({
                    "answer": request.POST["answer"+str(i)],
                    "is_correct": str(i) in request.POST.getlist("trueAnswer")
                })
                i += 1
        elif question_type == 2:
            pass
        elif question_type == 3:
            answers = request.POST["openAnswer"]
        question = {
            "number_of_question": len(json_test) + 1,
            "question": request.POST["question"],
            "type": question_type,
            "image": image[0].id,
            "answers": answers
        }
        json_test.append(question)
        test.test = pickle.dumps(json_test)
        test.save()
        return render(
            request,
            "exam/create_new_question.html",
            {
                "number_of_question": len(json_test) + 1,
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