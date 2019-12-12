from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages 
from apiclient.discovery import build
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import pickle
import smtplib

# Create your views here.

def index(request):
    return render(request, "bookings/index.html")

def indeling(request):
    return render(request, "bookings/indeling.html")

def contact(request):
    return render(request, "bookings/contact.html")

def book(request):

    if request.method == 'POST': 
        arrival_date = request.POST["arrival_date"]
        departure_date = request.POST.get("departure_date")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        telefoonnummer = request.POST.get("telefoonnummer")
        quest_number = request.POST.get("quest_number")
        comment = request.POST.get("comment")

        prijs = price(DateStringToObject(arrival_date), DateStringToObject(departure_date), quest_number)

        event = {
            'summary': f"{firstname} {lastname}",
            'description': f"booking=website telefoonnummer: {telefoonnummer} aantal gasten: {quest_number} opmerking:{comment} price:{prijs}",
            'start': {
                'date': arrival_date,
            },
            'end': {
                'date': departure_date,
            },
            'attendees': [
                {'email': email},
            ], 
        }

        if not dateisavailable(get_booking(), arrival_date, departure_date):
            credentials = pickle.load(open("/Users/abelvangennep/Desktop/Programmeren/project-sintanna/app/googleapi-setup/token.pkl", "rb"))
            service = build("calendar", "v3", credentials=credentials)
            event = service.events().insert(calendarId='uhtbefspsip0e23u07cspnj2r4@group.calendar.google.com', body=event).execute()
            subject = "Boekingsbevestiging"
            msg = "U boeking is in goede orde ontvangen en verwerkt."
            send_email(subject, msg, email)
            context = {
                "prijs": prijs,
                "aankomst": arrival_date,
                "vertrek": departure_date
            }

            return render(request, "bookings/confirmation.html", context)
        messages.error(request, "De boeking is niet gelukt, neem contact op met de verhuurder.")
        

    return render(request, "bookings/book.html")

def get_booking():
    credentials = pickle.load(open("/Users/abelvangennep/Desktop/Programmeren/project-sintanna/app/googleapi-setup/token.pkl", "rb"))
    service = build("calendar", "v3", credentials=credentials)
    result = service.calendarList().list().execute()
    result = service.events().list(calendarId='uhtbefspsip0e23u07cspnj2r4@group.calendar.google.com', timeZone="Europe/Amsterdam").execute()
    items = result['items']
    booking = []
    for item in items:
        if 'booking=website' in item['description']:
            booking.append(item)

    return booking
            
def price(arrival, departure, quest_number):
    days =(departure - arrival).days
    prijs = {}
    prijs["nachtprijs"] = days * 70
    prijs["schoonmaakprijs"] = 55
    prijs["linnengoedprijs"] = 12.50 * int(quest_number)
    if int(quest_number) > 4:
        prijs["toeslag_exta"] = (int(quest_number) - 4) * 10 * days 
    else:
        prijs["toeslag_exta"] = 0
    prijs["totaal"] = prijs["nachtprijs"] + prijs["schoonmaakprijs"] + prijs["linnengoedprijs"] + prijs["toeslag_exta"]

    return prijs

def DateStringToObject(datum):
    date = datetime.strptime(datum, '%Y-%m-%d').date()
    return date

def dateisavailable(bookings, arrival_date, departure_date):
    for booking in bookings:
        print(booking["start"]["date"] < departure_date and arrival_date < booking["end"]["date"])
        if (booking["start"]["date"] < departure_date and arrival_date < booking["end"]["date"]):
            return True
    return False

def send_email(subject, msg, email):
    try:
        user_email = "sintannaverhuur@gmail.com"
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login(user_email, "Vangennep1")
        message = 'Subject: {}\n\n{}'.format(subject,msg)
        server.sendmail(user_email, email, message)
        server.quit()
        print("Email is succesvol verzonden")
    except:
        print("EMAIL is niet verzonden")

