from django.http import HttpRequest, HttpResponse


def greetings(request: HttpRequest) -> HttpResponse:
    username = 'Serhii'
    return HttpResponse(f"Hello, {username}!")
