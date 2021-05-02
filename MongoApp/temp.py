from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.edit import FormView

import os
from mongoengine import connect
from datetime import datetime

from .forms import DateForm



def query_mongo(start_time, end_time):
    my_client = connect('test')

    my_db = my_client["test"]
    my_col = my_db["people"]
    # print('type input: ', type(start_time))
    # date_from= '2008/03/28'
    # date_to= '2008/03/28'
    date_from = start_time
    date_to = end_time

    date_from = str(start_time).replace('/','-')
    date_from = date_from +'T00:00:00.000Z'
    # print(type(date_from))
    date_to = str(end_time).replace('/','-')
    date_to = date_to +'T23:59:59.000Z'
    print('date_from: ',date_from)
    print('date_to: ',date_to)

    # -------------- working in right way ---------------
    # date_from = '2008-03-22T00:00:00.000Z'
    # date_to = '2008-03-22T23:59:59.000Z'

    results = my_col.find(
        {'$and': [{'signup': {'$gte': date_from}}, {'signup': {'$lte': date_to}}]})

    try:
        today = datetime.today()
        today = today.strftime("%d%m%y-%H%M")
        file_name = 'query-result-' + today + '.csv'
        output_file = os.path.join(os.getcwd(), file_name)
        print('===============')
        print(output_file)
        print(file_name)
        print('===============')
        if results.count() :
            # print(type(results[0]))
            with open(output_file, 'w') as reader:
                for result in results:
                    reader.write(str(result)+'\n')
        return output_file,file_name
    except:
        print(" no result found!")


@csrf_exempt
def home(request):
    context_post = "post request"
    context_get = "get request"
    if request.method == "GET":
        return render(request,'home.html')

    elif request.method == "POST":
        from_date = request.POST.get('date_from')
        print(from_date,'************************')
        to_date = request.POST.get('date_to')
        print(to_date,'************************')
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
        return render(request, self.template_name, {'form': form})
    
    # @method_decorator(csrf_exempt)
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data1=form.cleaned_data.get('from_date')
            data2=form.cleaned_data.get('to_date')
            query_link,file_name = query_mongo(data1,data2)
            # print(query_link)
            # /home/adel/DjangoCRUDMongoDB/DjangoCrudMongoDB/query-result-010521-1355.csv
            dl_link = os.path.dirname((os.path.abspath(__file__))) + '/static/'
            # print(dl_link)
            context={
                'data1':str(data1),
                'data2': data2,
                'query_link' :query_link,
                'dl_link':dl_link,
                'fname': file_name
            }
            # print('befor ',content['data1'])
            # print('after ',context['data2'])
            # query = 
            return render(request,'result.html', context=context)

        return render(request, self.template_name, {'form': form})


import mimetypes
import os
from django.http.response import HttpResponse
from django.shortcuts import render


def download_file(request, filename=''):
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    # filename = 'query-result-010521-1512.csv'
    filename = filename

    # Define the full file path
    # filepath = BASE_DIR + '/MongoApp/Files/' + filename
    filepath = BASE_DIR  +'/'+ filename
    print('**********************************')
    print('base dir : ', BASE_DIR)
    print(filename)
    print('filepath in  download = ', filepath)
    print('**********************************')
    # /home/adel/DjangoCRUDMongoDB/DjangoCrudMongoDB/query-result-010521-1512.csv
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





# # -----------my form --------------
# class DateForm(forms.Form):
#     from_date = forms.DateTimeField(widget=forms.DateInput(
#         attrs={'type': 'date'}), input_formats=['%Y/%m/%d'], label='از تاریخ')
#     to_date = forms.DateField(widget=forms.DateInput(
#         attrs={'type': 'date'}), input_formats=['%Y/%m/%d'], label='تا تاریخ')

# # ---------- my view -------------
# def post(self, request, *args, **kwargs):
#     form = self.form_class(request.POST)
#     print(form.is_valid()) # returned false
#     print(request.POST.get('from_date')) # return valid value
#     print(type(request.POST.get('from_date'))) # return <str class>
#     if form.is_valid():
#         data1 = form.cleaned_data.get('from_date')
#         data2 = form.cleaned_data.get('to_date')
#         # do something....
#         return render(request, 'result.html', context=context)

#     return render(request, self.template_name, {'form': form})