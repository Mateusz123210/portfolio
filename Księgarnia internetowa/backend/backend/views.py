from django.shortcuts import render
from database.database_module import database_executor as db
from django.http import HttpResponse

def return_page(request):
    if request.method == "GET":
        return render(request, "index.html")
    return HttpResponse(status=403)

def get_start_page_data(request):
    if request.method == "GET":
        page =db.get_start_page_data()
        if len(page) != 0:
            return HttpResponse(page, status=200)
        else:
            return HttpResponse(status=204)
    return HttpResponse(status=403)


def find_books(request, title: str, genre: str, authorfirstname: str,authorsurname: str, publisher: str, release: str, min: str, max: str, check: str):
    if request.method == "GET":
        resp = db.find_books( title, genre, authorfirstname, authorsurname, publisher, release, min, max, check)
        if len(resp) > 2:
            return HttpResponse(resp, status=200)
        else:
            return HttpResponse(status=204)
    return HttpResponse(status=403)


def get_book(request, id: int):
    if request.method == "GET":
        resp = db.get_book(id)
        if len(resp) != 0:
            return HttpResponse(resp, status=200)
        else:
            return HttpResponse(status=204)
    return HttpResponse(status=403)




