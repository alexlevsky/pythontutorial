from django.http import HttpResponse
from django.template import RequestContext, loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Choice, Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

# Create your views here.

from django import forms
from django.contrib.sessions.backends.db import SessionStore

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

# робота з сессиями
def form(request):
    f = ContactForm()
    request.session['0']='bar'
    request.session['1']='navi'
    request.session['2'] = 'enter'
    request.session['3'] = 'docum' #  запись в сессию
    print(request.session['0'])
    print('dddddddddddd')
    print(request.session['1'])
    print(request.session['2'])
    print(request.session['3'])
    request.session.set_test_cookie()  # ставим тестовую куку
    print(request.session.test_cookie_worked())  # проверяем ёё
    return render(request, 'polls/form.html', {'form': f} ) #  связиваем форму со значением ф


from django.core import serializers
JSONSerializer = serializers.get_serializer("json")
json_serializer = JSONSerializer()

with open("file.json", "w") as out:
    json_serializer.serialize(Question.objects.all(), stream=out)


def masterone():
    print('masterone')

def one():
    print('one')
def two():
    print('two')
def tree():
    print('tree')


import csv


# робота з csv скачиваеться файл somefilename.csv на компютер пользователя
def somev(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])   # запись в первую строчку файла
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response



# робота з пдф  нужно перед использованием сделать pip install reportlab
from reportlab.pdfgen import canvas
def somePDF(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response