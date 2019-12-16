# Sintannaverhuur
#
# mprog apps
# Abel van Gennep
#
# Sintannaverhuur is a bookings application for a rental house.
# De Calendar is synchronised with a google calendar and makes use of a javascript calendar, to
# display the booking dates.
# The website also gives an impression of the surroundings.
# ================================================================================================
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages 
from apiclient.discovery import build
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import os
import pickle
import smtplib

def index(request):
    # Make a list, which exists out of the names of all the files in the folder sfeer
    path="/Users/abelvangennep/Desktop/Programmeren/project-sintanna/app/sintannaverhuur/bookings/static/bookings/afbeeldingen/sfeer"  # insert the path to your directory   
    sfeer_afbeeldingen = os.listdir(path)   
    sfeer_afbeeldingen.pop(0)
    
    context = {
        'sfeer_afbeeldingen': sfeer_afbeeldingen,
    }
    return render(request, "bookings/index.html", context)

def indeling(request):
    # Make a list, which exists out of the names of all the files in the folder inrichting
    path="/Users/abelvangennep/Desktop/Programmeren/project-sintanna/app/sintannaverhuur/bookings/static/bookings/afbeeldingen/inrichting"  # insert the path to your directory   
    inrichting_afbeeldingen = os.listdir(path)   
    inrichting_afbeeldingen.pop(0)

    context = {
        'inrichting_afbeeldingen': inrichting_afbeeldingen,
    }
    return render(request, "bookings/indeling.html", context)

def contact(request):
    return render(request, "bookings/contact.html")

def book(request):
    # If user submits a booking get their input
    if request.method == 'POST': 
        arrival_date = request.POST["arrival_date"]
        departure_date = request.POST.get("departure_date")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        telefoonnummer = request.POST.get("telefoonnummer")
        quest_number = request.POST.get("quest_number")
        comment = request.POST.get("comment")

        # Get the price of the stay
        price = pricecalculator(DateStringToObject(arrival_date), DateStringToObject(departure_date), quest_number)

        event = {
            'summary': f"{firstname} {lastname}",
            'description': f"booking=website telefoonnummer: {telefoonnummer} aantal gasten: {quest_number} opmerking:{comment} prijs:{price}",
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

        # Check whether date is available
        if dateisavailable(get_booking(), arrival_date, departure_date):
            # login to Google api
            service = google_service()

            # Insert event in the calendar "boekings"
            event = service.events().insert(calendarId='uhtbefspsip0e23u07cspnj2r4@group.calendar.google.com', body=event).execute()
            
            # Sent bookings confirmation
            subject = "Boekingsbevestiging"
            msg = f"U boeking is in goede orde ontvangen en verwerkt. De aankomst datum van u boeking is: {arrival_date} na 16:00. U vertrekdatum is: {departure_date} voor 10:00"
            send_email(subject, msg, email)
            
            context = {
                "prijs": price,
                "aankomst": arrival_date,
                "vertrek": departure_date
            }

            return render(request, "bookings/confirmation.html", context)
        # Als datum niet beschikbaar is, verstuur error
        messages.error(request, "De boeking is niet gelukt, neem contact op met de verhuurder.")
        

    return render(request, "bookings/book.html")

def get_booking():
    # login to Google api
    service = google_service()

    # Get all events of the calendar "boekings"
    result = service.events().list(calendarId='uhtbefspsip0e23u07cspnj2r4@group.calendar.google.com', timeZone="Europe/Amsterdam").execute()
    booking = []

    # Filter events which have booking=website in their description
    for item in result['items']:
        if 'booking=website' in item['description']:
            booking.append(item)
    return booking
            
def pricecalculator(arrival, departure, quest_number):
    # Calculate of nights of a specific stay 
    days =(departure - arrival).days
    
    # Create a dictionary price and calculate the prices of all the components
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
    # convert date string in a date object of the module datetime
    date = datetime.strptime(datum, '%Y-%m-%d').date()
    return date

def dateisavailable(bookings, arrival_date, departure_date):
    # Check whether dat the booked date has overlap with one of the bookings 
    for booking in bookings:
        if (booking["start"]["date"] < departure_date and arrival_date < booking["end"]["date"]):
            return False
    return True

def send_email(subject, msg, email):
    try:
        # Use the SMTP module to send an email
        user_email = "sintannaverhuur@gmail.com"
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login(user_email, "Vangennep1")
        message = 'Subject: {}\n\n{}'.format(subject,msg)
        server.sendmail(user_email, email, message)
        server.quit()

    except:
        pass

def google_service():
    # Use credentials to log in to the google service API
    credentials = pickle.load(open("/Users/abelvangennep/Desktop/Programmeren/project-sintanna/app/googleapi-setup/token.pkl", "rb"))
    service = build("calendar", "v3", credentials=credentials)
    return service

