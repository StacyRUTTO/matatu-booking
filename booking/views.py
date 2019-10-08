from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .forms import ticketForm, adminLoginForm, routesForm
from .models import Ticket, Pricing
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .render import Render
# Create your views here.


def book(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ticketForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            ticket = form.save(commit=False)
            form.save()
            return HttpResponseRedirect(reverse('ticket', args=(ticket.ticket_id,)))
    else:
        form = ticketForm()

    context = {
        'form': form
    }
    return render(request, 'book.html', context)


def seat(request):
    if request.method == "POST":
        to = request.POST.get('to')
        fr = request.POST.get('fr')
        date_d = request.POST.get('date_d')
        time_t = request.POST.get('time_t')
        total_no_seats = Ticket.objects.filter(
            to=to, origin=fr, date_of_departure=date_d, time_of_departure=time_t).count()
        full_cars = total_no_seats//11
        seats_on_full_cars = full_cars*11
        seats_taken_on_not_full_car = Ticket.objects.filter(
            to=to, origin=fr, date_of_departure=date_d, time_of_departure=time_t)[seats_on_full_cars:total_no_seats]
        seats = []
        for ticket in seats_taken_on_not_full_car:
            seats.append(ticket.seat_no)

    data = {
        'taken_seats': seats,
    }

    return JsonResponse(data, safe=False)


def price(request):
    if request.method == "POST":
        to = request.POST.get('to')
        fr = request.POST.get('fr')
        price = Pricing.objects.get(to=to, origin=fr)
        data = {
            'price': price.price,
        }
    return JsonResponse(data, safe=False)


def ticket(request, ticket_id):
    ticket_info = Ticket.objects.get(ticket_id=ticket_id)
    context = {
        'ticket_info': ticket_info,
    }
    return Render.render('ticket.html', context)
    

@login_required
def management(request):
    form = routesForm()
    return render(request, 'management.html',{'form':form})

@login_required
def ticket_data(request):
    times = [4, 6, 8, 10, 12, 20]
    ticket_data = []
    report = {}
    
    if request.method == "POST":
        date = request.POST.get('date')
        to = request.POST.get('to')
        origin = request.POST.get('origin')
        # query 
        tickets = Ticket.objects.filter(to=to, origin=origin, date_of_departure=date)
        # create the json data
        for time in times:
            count = Ticket.objects.filter(time_of_departure=time,to=to, origin=origin, date_of_departure=date).count()
            ticket_data.append(count)
        # ticket info
        tickets = Ticket.objects.filter(to=to, origin=origin, date_of_departure=date)
        number = Ticket.objects.filter(to=to, origin=origin, date_of_departure=date).count()
        for ticket in tickets:
            report[str(ticket.ticket_id)] ={
                "name": ticket.name,
                'phone_no': ticket.phone_no,
                'time': ticket.time_of_departure,
                'seat_no': ticket.seat_no
            }
        response = {
            'ticket_data': ticket_data, 
            'to': to,
            'origin': origin,
            'date': date,
            'report': report,
            'number': number
        }
        
    return JsonResponse(response, safe=False)


@login_required
def report(request,to,origin, date):
    tickets = Ticket.objects.filter(to=to, origin=origin, date_of_departure=date)
    number = Ticket.objects.filter(to=to, origin=origin, date_of_departure=date).count()
    context = {
        'tickets': tickets,
        'number':number,
        'to':to,
        'origin':origin,
        'date':date
    }
    return Render.render('report.html', context)