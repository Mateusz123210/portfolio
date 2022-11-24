import MySQLdb as mc
from database.models import *
from database.serializers import BooksSerializer,BooksSerializer2, BookAuthorshipsSerializer, BookCategoriesSerializer
import json
import datetime


def get_start_page_data():
    all_entries = Books.objects.filter(is_available = 1)
    list1 = []
    dict1 = {}
    serializer = BooksSerializer(all_entries, many = True)
    res = json.dumps(serializer.data)
    dict1["books"] = res
    list1.append(dict1)
    

    dict2 = {}
    all_categories = BookCategories.objects.all()
    serializer = BookCategoriesSerializer(all_categories, many = True)
    res = json.dumps(serializer.data)
    dict2["categories"] = res
    list1.append(dict2)    
    ret = json.dumps(list1)
    return ret
    


def find_books(title1: str, genre1: str, author1: str, author2:str, publisher1: str, release1: str, min1: str, max1: str, check: str):

    if len(check) != 7:
        return ""
    for a in check:
        if a != '0' and a != '1':
            return ""
    all_entries = None
    dict1 = {}
    dict1['is_available'] = 1
    if check[0] == '1':
        dict1['title__icontains'] = title1
    if check[4] == '1':
        format = '%Y-%m-%d'
        try:
            date = datetime.datetime.strptime(release1, format).date()
        except ValueError:
            return ""
        dict1['release_date__exact'] = date
    if check[5] == '1':
        min2 = float(min1)
        dict1['price__gte'] = min2
    if check[6] == '1':
        max2 = float(max1)
        dict1['price__lte'] = max2
    all_entries = Books.objects.filter(**dict1).select_related('book_category','publisher')
    list1 = []
    for i in all_entries:
        good = True
        if check[1] == '1':
            if genre1 != i.book_category.name:
                good = False
        if good is True and check[3] == '1':
            if publisher1 != i.publisher.name:
                good = False
        if good is True:
            if check[2] == '1':
                authors = BookAuthorships.objects.select_related('book_author').filter(book = i.id)
                contains = False
                for j in authors:
                    if j.book_author.firstname == author1 and j.book_author.surname == author2:
                        contains = True
                        break                
                if contains is True:
                    serializer = BooksSerializer(i)
                    res = json.dumps(serializer.data)
                    list1.append(res)
            else:
                serializer = BooksSerializer(i)
                res = json.dumps(serializer.data)
                list1.append(res)
    return json.dumps(list1)

def get_book(id: int):
    all_entries = Books.objects.filter(is_available = 1, id = id).select_related('book_category','publisher','book_cover','language')
    list1 = []
    if (not(all_entries is None)) and len(all_entries) > 0:
        dict1 = {}
        serializer = BooksSerializer2(all_entries[0])
        res = json.dumps(serializer.data)
        dict1["book"] = res
        authors = BookAuthorships.objects.select_related('book_author').filter(book = all_entries[0].id)
        serializer2 = BookAuthorshipsSerializer(authors, many = True)
        res2 = json.dumps(serializer2.data)
        dict1["authors"] = res2
        list1.append(dict1)

        ret = json.dumps(list1)
        return ret
    return ""


