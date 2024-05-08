import sys
sys.path.append('../../')
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_backend.settings')
django.setup()

import pandas as pd
from booking.models import Booking
from django.utils import timezone

def clear_bookings(days:int=7):
    # Clear bookings which are older than 7 days
    bookings = Booking.objects.all().filter(booking_time__lt=timezone.now()-timezone.timedelta(days=days))
    print(bookings)
    
if __name__ == "__main__":
    clear_bookings(days=7)