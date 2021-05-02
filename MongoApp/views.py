from django.shortcuts import render
from django.http.response import HttpResponse
import mimetypes
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.edit import FormView

import os
from mongoengine import connect
from datetime import datetime

from .forms import DateForm


def query_mongo(start_time, h1, end_time, h2):
    my_client = connect('test')

    my_db = my_client["test"]
    my_col = my_db["people"]
    date_from = start_time
    date_to = end_time

    date_from = str(start_time).replace('/', '-')
    date_from = date_from[0:10] + 'T'+ h1+ '.000Z'
    date_to = str(end_time).replace('/', '-')
    date_to = date_to + 'T' + h2 + '.000Z'
    print('date_from: ', date_from)
    print('date_to: ', date_to)

    # -------------- working in right way ---------------
    results = my_col.find(
        {'$and': [{'signup': {'$gte': date_from}}, {'signup': {'$lte': date_to}}]})

    try:
        today = datetime.today()
        today = today.strftime("%d%m%y-%H%M")
        BASE_DIR = (os.path.dirname(os.path.abspath(__file__)))
        file_name = 'query-result-' + today + '.csv'
        save_dir = 'Files/' + file_name
        output_file = os.path.join(BASE_DIR, save_dir)
        print('===============')
        print(file_name)
        print(save_dir)
        print(BASE_DIR)
        print(output_file)
        print('===============')
        # print(results.count())
        if results.count():
            with open(output_file, 'w') as reader:
                for result in results:
                    reader.write(str(result)+'\n')
        return output_file, file_name
    except:
        print(" no result found!")


@csrf_exempt
def home(request):
    context_post = "post request"
    context_get = "get request"
    # print('im in home!6666666666666666666666666666666')
    if request.method == "GET":
        return render(request, 'home.html')

    elif request.method == "POST":
        from_date = request.POST.get('date_from')
        # print(from_date, '************************')
        # to_date = request.POST.get('date_to')
        # print(to_date, '************************')
        return HttpResponse(context_post)


class Contact(FormView):
    template_name = 'home.html'
    form_class = DateForm
    success_url = 'result'


class MyFormView(View):
    form_class = DateForm
    initial = {'key': 'value'}
    template_name = 'home.html'

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        print('im in home! 77777777777777777777')
        return render(request, self.template_name, {'form': form})

    # @method_decorator(csrf_exempt)
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print('im in home! 88888888 POST')
        print(form.is_valid())
        print(request.POST.get('from_date'))
        print(type(request.POST.get('from_date')))
        print(form.errors.values())
        if form.is_valid():
            data1 = form.cleaned_data.get('from_date')
            data2 = form.cleaned_data.get('to_date')
            h1 = form.cleaned_data.get('from_hour').time()
            h2 = form.cleaned_data.get('to_hour').time()
            # print('8888888888888888888888888888888888888')
            # print(data1)
            # print(data2)
            query_link, file_name = query_mongo(data1,str(h1), data2,str(h2))
            # print(query_link)
            # /home/adel/DjangoCRUDMongoDB/DjangoCrudMongoDB/query-result-010521-1355.csv
            # print(dl_link)
            print( '-----------sa@ check --------------')
            print(h1)
            print(h2)
            print(type(h1), type(h2))
            context = {
                'data1': data1,
                'data2': data2,
                'h1':h1,
                'h2':h2,
                'query_link': query_link,
                'fname': file_name
            }
            return render(request, 'result.html', context=context)

        return render(request, self.template_name, {'form': form})


def download_file(request, filename=''):
    # Define Django project base directory
    BASE_DIR = (os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    # filename = 'query-result-010521-1512.csv'
    filename = filename

    # Define the full file path

    filepath = BASE_DIR + '/Files/' + filename
    print('**********************************')
    print('base dir : ', BASE_DIR)
    print(filename)
    print('filepath in  download = ', filepath)
    print('**********************************')
    # Open the file for reading content
    path = open(filepath, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response
