from django.shortcuts import render


# Create your views here.
def back_index(request):
    return render(request, 'err/back_index.html')


def not_found(request, e):
    e = {'e': e}
    return render(request, 'err/not_found.html', e)
