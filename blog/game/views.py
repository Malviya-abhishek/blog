from django.shortcuts import render

# Create your views here.

def game_list_view(request):
    template = "game\index.html"
    context = {"game1":"game\index.html"}
    return render(request,template,context)

def game_detail_view(request):
    template = "game\list.html"
    context = {"game1":"index.html"}
    return render(request,template,context)


def js_view(request):
    template = "game\script.js"
    context = {}
    return render(request,template,context)