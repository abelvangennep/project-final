from django.http import HttpResponse
from django.shortcuts import render
from apiclient.discovery import build
import pickle

# Create your views here.

def index(request):
    return HttpResponse("hello world")

def get_booking(request):
    credentials = pickle.load(open("/Users/abelvangennep/Desktop/Programmeren/project-sintanna/app/googleapi-setup/token.pkl", "rb"))
    service = build("calendar", "v3", credentials=credentials)
    result = service.calendarList().list().execute()
    print(result)
    result = service.events().list(calendarId='uhtbefspsip0e23u07cspnj2r4@group.calendar.google.com', timeZone="Europe/Amsterdam").execute()
    items = result['items']
    for item in items:
        if 'bookingtype=website' in item['description']:
            print(item)
    


    
    





