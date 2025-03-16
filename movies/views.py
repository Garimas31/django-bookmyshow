from django.shortcuts import render, redirect ,get_object_or_404
from .models import Movie,Theater,Seat,Booking, Genre, Language
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Q
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required  # Only admin can access
def admin_dashboard(request):
    total_revenue = Booking.objects.count() * 250 # Example price per ticket
    most_popular_movies = Movie.objects.annotate(ticket_count=Count('bookings')).order_by('-ticket_count')[:5]
    busiest_theaters = Theater.objects.annotate(booked_seats=Count('seats', filter= Q(seats__is_booked=True))).order_by('-booked_seats')[:5]

    context = {
        'total_revenue': total_revenue,
        'most_popular_movies': most_popular_movies,
        'busiest_theaters': busiest_theaters
    }
    return render(request, 'movies/admin_dashboard.html', context)
def movie_list(request):
    movies = Movie.objects.all()

    # Filtering based on search, genre, and language
    if 'search' in request.GET:
        search_term = request.GET['search']
        movies = movies.filter(name__icontains=search_term)

    if 'genre' in request.GET and request.GET['genre']:
        genre = request.GET['genre']
        movies = movies.filter(genre=genre)

    if 'language' in request.GET and request.GET['language']:
        language = request.GET['language']
        movies = movies.filter(language=language)

    return render(request, 'movies/movie_list.html', {
        'movies': movies,
        'genres': Movie.GENRE_CHOICES,
        'languages': Movie.LANGUAGE_CHOICES,
    })


def theater_list(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    theaters = Theater.objects.filter(movie=movie)

    # Fetch available seat count for each theater
    theaters_with_seats = [
        {
            "theater": theater,
            "available_seats": Seat.objects.filter(theater=theater, is_booked=False).count()
        }
        for theater in theaters
    ]

    return render(request, 'movies/theater_list.html', {'movie': movie, 'theaters': theaters_with_seats})

@login_required(login_url='/login/')

def book_seats(request, theater_id):
    theater = get_object_or_404(Theater, id=theater_id)
    seats = Seat.objects.filter(theater=theater)
    
    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')
        error_seats = []
        
        if not selected_seats:
            return render(request, "movies/seat_selection.html", {'theater': theater, "seats": seats, 'error': "No seat selected"})
        
        booked_seats = []
        for seat_id in selected_seats:
            seat = get_object_or_404(Seat, id=seat_id, theater=theater)
            if seat.is_booked:
                error_seats.append(seat.seat_number)
                continue
            try:
                booking = Booking.objects.create(
                    user=request.user,
                    seat=seat,
                    movie=theater.movie,
                    theater=theater
                )
                seat.is_booked = True
                seat.save()
                booked_seats.append(seat.seat_number)
            except IntegrityError:
                error_seats.append(seat.seat_number)

        if error_seats:
            error_message = f"The following seats are already booked: {', '.join(error_seats)}"
            return render(request, 'movies/seat_selection.html', {'theater': theater, "seats": seats, 'error': error_message})

        # ✅ Send Email Confirmation
        subject = "Booking Confirmation - BookMySeat 🎟️"
        context = {
            'user': request.user,
            'movie': theater.movie,
            'theater': theater,
            'seats': booked_seats,
        }
        html_message = render_to_string('movies/email_confirm.html', context)
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [request.user.email]
        print(f"Sending email to: {recipient_list}") 
        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)

        return redirect('profile')  # Redirect to profile after booking

    return render(request, 'movies/seat_selection.html', {'theater': theater, "seats": seats})
# cancel ticket
@login_required(login_url='/login/')
def cancel_ticket(request, booking_id):
    booking = Booking.objects.get(id=booking_id, user=request.user)

    if not booking:
        messages.error(request, "Booking not found!")
        return redirect('profile')  

    # Update seat status
    seat = booking.seat
    seat.is_booked = False
    seat.save()

    # Delete booking
    booking.delete()

    # ✅ Send Cancellation Email
    subject = "Ticket Cancellation Confirmation 🎟️"
    context = {
        'user': request.user,
        'movie': booking.movie,
        'theater': booking.theater,
        'seat': seat.seat_number,
    }
    html_message = render_to_string('movies/email_cancel.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [request.user.email]
    
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)

    messages.success(request, f"Your ticket for {booking.movie.name} (Seat {seat.seat_number}) has been canceled.")
    return redirect('profile')  # Redirect to profile page


# @login_required(login_url='/login/')

# def book_seats(request,theater_id):
#     theaters=get_object_or_404(Theater,id=theater_id)
#     seats=Seat.objects.filter(theater=theaters)
#     if request.method=='POST':
#         selected_Seats= request.POST.getlist('seats')
#         error_seats=[]
#         if not selected_Seats:
#             return render(request,"movies/seat_selection.html",{'theater':theaters,"seats":seats,'error':"No seat selected"})
#         for seat_id in selected_Seats:
#             seat=get_object_or_404(Seat,id=seat_id,theater=theaters)
#             if seat.is_booked:
#                 error_seats.append(seat.seat_number)
#                 continue
#             try:
#                 Booking.objects.create(
#                     user=request.user,
#                     seat=seat,
#                     movie=theaters.movie,
#                     theater=theaters
#                 )
#                 seat.is_booked=True
#                 seat.save()
#             except IntegrityError:
#                 error_seats.append(seat.seat_number)
#         if error_seats:
#             error_message=f"The following seats are already booked:{','.join(error_seats)}"
#             return render(request,'movies/seat_selection.html',{'theater':theaters,"seats":seats,'error':"No seat selected"})
#         return redirect('profile')
#     return render(request,'movies/seat_selection.html',{'theaters':theaters,"seats":seats})



# def movie_list(request):
#     search_query = request.GET.get('search')
#     genre_filter = request.GET.get('genre')
#     language_filter = request.GET.get('language')

#     # Get all genres and languages for filtering dropdown
#     genres = Genre.objects.all()
#     languages = Language.objects.all()

#     # Filter movies based on genre and language
#     movies = Movie.objects.all()

#     if genre_filter:
#         movies = movies.filter(genre__id=genre_filter)
    
#     if language_filter:
#         movies = movies.filter(language__id=language_filter)

#     if search_query:
#         movies = movies.filter(name__icontains=search_query)

#     return render(request, 'movies/movie_list.html', {
#         'movies': movies,
#         'genres': genres,
#         'languages': languages
#     })


# def movie_list(request):
#     search_query=request.GET.get('search')
#     if search_query:
#         movies=Movie.objects.filter(name__icontains=search_query)
#     else:
#         movies=Movie.objects.all()
#     return render(request,'movies/movie_list.html',{'movies':movies})

# def theater_list(request,movie_id):
#     movie = get_object_or_404(Movie,id=movie_id)
#     theater=Theater.objects.filter(movie=movie)
#     return render(request,'movies/theater_list.html',{'movie':movie,'theaters':theater})