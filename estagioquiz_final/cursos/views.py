from django.shortcuts import render



def home(request):
    return render(request, 'cursos/index.html')

def informatica(request):
    return render(request, 'cursos/informatica.html')

def mecatronica(request):
    return render(request, 'cursos/mecatronica.html')

def edificacoes(request):
    return render(request, 'cursos/edificacoes.html')
