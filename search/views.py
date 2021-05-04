""" Search Directory for the Bisa Humad Jain Samaj
    Copyright (C) 2021  Varun Jain

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>."""

import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import openpyxl
from datetime import date
from dateutil.relativedelta import relativedelta

from .models import *

# Create your views here.
def index(request):
    return render(request, "search/index.html")

def sname(request):
    data = json.loads(request.body)
    name = data.get('name')
    mname = data.get('mname')
    lname = data.get('lname')
    if name:
        if mname:
            if lname:
                people = People.objects.filter(Name__startswith = name, MiddleName__startswith = mname, SurName__startswith = lname)
            else:
                people = People.objects.filter(Name__startswith = name, MiddleName__startswith = mname)
        else:
            if lname:
                people = People.objects.filter(Name__startswith = name, SurName__startswith = lname)
            else:
                people = People.objects.filter(Name__startswith = name)
    elif mname:
        if lname:
            people = People.objects.filter(MiddleName__startswith = mname, SurName__startswith = lname)
        else:
            people = People.objects.filter(MiddleName__startswith = mname)
    elif lname:
        people = People.objects.filter(SurName__startswith = lname)
    else:
        return JsonResponse({"error": "Atleast one field should be filled"}, status = 400, safe=False)
    if not people:
        return JsonResponse({"error": "No people Available"}, status = 200, safe=False)
    else:
        return JsonResponse([p.serialize() for p in people], status = 200, safe=False)

def sadv(request):
    data = json.loads(request.body)
    name = data.get('name')
    mname = data.get('mname')
    lname = data.get('lname')
    gender = data.get('gender')
    miage = data.get('miage')
    maage = data.get('maage')
    mstat = data.get('mstat')
    people = []
    if name == mname == lname == miage == maage == '' and gender == mstat == '#':
        return JsonResponse({"error": "Atleast one field should be filled"}, status = 400, safe=False)
    if miage != '':
        miage = int(miage)
    if maage != '':
        maage = int(maage)
    if name:
        people = People.objects.filter(Name__startswith = name)
        if mname:
            people = people.filter(MiddleName__startswith = mname)
        if lname:
            people = people.filter(SurName__startswith = lname)
    elif mname:
        people = People.objects.filter(MiddleName__startswith = mname)
        if lname:
            people = people.filter(SurName__startswith = lname)
    elif lname:
        people = People.objects.filter(SurName__startswith = lname)
    if not people:
        if gender != '#':
            people = People.objects.filter(Gender = gender)
            if mstat != '#':
                people = people.filter(MaritalStatus = mstat)
            if miage:
                people = people.filter(Age__range=(miage,relativedelta(datetime.now(), datetime(1900,1,1)).years))
            if maage:
                people = people.filter(Age__range=(0,maage))
        elif mstat != '#':
            people = People.objects.filter(MaritalStatus = mstat)
            if miage:
                people = people.filter(Age__range=(miage,relativedelta(datetime.now(), datetime(1900,1,1)).years))
            if maage:
                people = people.filter(Age__range=(0,maage))
        elif miage:
            if maage:
                people = People.objects.filter(Age__range=(miage,maage))
            else:
                people = People.objects.filter(Age__range=(miage,relativedelta(datetime.now(), datetime(1900,1,1)).years))
        elif maage:
            people = People.objects.filter(Age__range=(0,maage))
    else:
        if gender != '#':
            people = people.filter(Gender = gender)
        if mstat != '#':
            people = people.filter(MaritalStatus = mstat)
        if miage:
            people = people.filter(Age__range=(miage,relativedelta(datetime.now(), datetime(1900,1,1)).years))
        if maage:
            people = people.filter(Age__range=(0,maage))
    if not people:
        if miage and maage:
            if miage > maage:
                return JsonResponse({"error": "Minimum Age can't be greater than Maximum Age"})
        return JsonResponse({"error": "No people Available"}, status = 200, safe=False)
    else:
        return JsonResponse([p.serialize() for p in people], status = 200, safe=False)

def person(request, Id):
    p = People.objects.get(pk=Id)
    return render(request, 'search/person.html', {
        "p" : p.serialize(),
    })

def family(request, familyno):
    people = People.objects.filter(FamilyNo = familyno)
    return render(request, 'search/family.html', {
        "p" : [p.serialize() for p in people],
        "last" : people[people.count()-1].id
    })


def upload(request):
    People.objects.all().delete()
    wb = openpyxl.load_workbook("search/Bisa Humad Jain Samaj 2014.xlsx", data_only=True)
    sheet = wb.active
    for data in sheet.iter_rows(min_row=2):
        if data[3].value == None and data[5].value == None:
            if data[14].value == 'H':
                p = People(SurName=data[1].value, Name=data[2].value, Gender=data[10].value, MaritalStatus=data[12].value, FamilyNo=data[13].value, Head=True)
            else:
                p = People(SurName=data[1].value, Name=data[2].value, Gender=data[10].value, MaritalStatus=data[12].value, FamilyNo=data[13].value, Head=False)
        elif data[3].value == None:
            if data[14].value == 'H':
                p = People(SurName=data[1].value, Name=data[2].value, DOB=data[5].value.date(), Gender=data[10].value, MaritalStatus=data[12].value, FamilyNo=data[13].value, Head=True)
            else:
                p = People(SurName=data[1].value, Name=data[2].value, DOB=data[5].value.date(), Gender=data[10].value, MaritalStatus=data[12].value, FamilyNo=data[13].value, Head=False)
        elif data[5].value == None:
            if data[14].value == 'H':
                p = People(SurName=data[1].value, Name=data[2].value, MiddleName=data[3].value, Gender=data[10].value, MaritalStatus=data[12].value, FamilyNo=data[13].value, Head=True)
            else:
                p = People(SurName=data[1].value, Name=data[2].value, MiddleName=data[3].value, Gender=data[10].value, MaritalStatus=data[12].value, FamilyNo=data[13].value, Head=False)
        else:
            if data[14].value == 'H':
                p = People(SurName=data[1].value, Name=data[2].value, MiddleName=data[3].value, DOB=data[5].value.date(), Gender=data[10].value, MaritalStatus=data[12].value, FamilyNo=data[13].value, Head=True)
            else:
                p = People(SurName=data[1].value, Name=data[2].value, MiddleName=data[3].value, DOB=data[5].value.date(), Gender=data[10].value, MaritalStatus=data[12].value, FamilyNo=data[13].value, Head=False)
        p.save()
    return HttpResponseRedirect(reverse('home'))

def age(request):
    for p in People.objects.all():
        rdelta = relativedelta(date.today(),p.DOB)
        p.Age = rdelta.years
        p.save()
    return HttpResponseRedirect(reverse('home'))