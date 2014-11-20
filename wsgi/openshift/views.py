from django.shortcuts import render_to_response

def home(request):
     return render_to_response('blog/index.html')


def blog(request):
     return render_to_response('blog/blog.html')