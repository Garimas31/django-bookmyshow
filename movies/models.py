from django.db import models
from django.contrib.auth.models import User 


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    GENRE_CHOICES = [
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('horror', 'Horror'),
    ]

    LANGUAGE_CHOICES = [
        ('hindi', 'Hindi'),
        ('english', 'English'),
        ('telugu', 'Telugu'),
    ]
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="movies/")
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    cast = models.TextField()
    description = models.TextField(blank=True, null=True)  # optional
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES,null=True)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, null=True)

    def __str__(self):
        return self.name

class Theater(models.Model):
    name = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='theaters')
    time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=250.00) 
    def available_seats(self):
        return self.seats.filter(is_booked=False).count()

    def total_revenue(self):
        return self.seats.filter(is_booked=True).count() * self.price 
    def __str__(self):
        available = "Seats Available" if self.available_seats() > 0 else "Fully Booked"
        return f'{self.name} - {self.movie.name} at {self.time} ({available})'


class Seat(models.Model):
    theater = models.ForeignKey(Theater,on_delete=models.CASCADE,related_name='seats')
    seat_number = models.CharField(max_length=10)
    is_booked=models.BooleanField(default=False)

    def __str__(self):
        return f'{self.seat_number} in {self.theater.name}'

class Booking(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="bookings")
    seat=models.OneToOneField(Seat,on_delete=models.CASCADE, related_name="bookings")
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE, related_name="bookings")
    theater=models.ForeignKey(Theater,on_delete=models.CASCADE, related_name="bookings")
    booked_at=models.DateTimeField(auto_now_add=True)
    user_email = models.EmailField(null=True, blank = True)  # Add this if user emails aren't in the User model
    def __str__(self):
        return f'Booking by{self.user.username} for {self.seat.seat_number} at {self.theater.name}'
    
# from cloudinary.models import CloudinaryField
  #    image = CloudinaryField('image')  
# class Movie(models.Model):
#     name= models.CharField(max_length=255)
#     image= models.ImageField(upload_to="movies/")
#     rating = models.DecimalField(max_digits=3,decimal_places=1)
#     cast= models.TextField()
#     description= models.TextField(blank=True,null=True) # optional

#     def __str__(self):
#         return self.name

# class Theater(models.Model):
#     name = models.CharField(max_length=255)
#     movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='theaters')
#     time= models.DateTimeField()

#     def __str__(self):
#         return f'{self.name} - {self.movie.name} at {self.time}'