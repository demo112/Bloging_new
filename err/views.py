from django.shortcuts import render


# Create your views here.
def back_index(request):
    return render(request, 'err/back_index.html')
