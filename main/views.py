from django.shortcuts import render

def show_main(request):
    context = {
        'npm': '2406496025',           
        'name': 'Raqilla Al-Abrar',   
        'class': 'PBP A'
    }
    return render(request, "main.html", context)
