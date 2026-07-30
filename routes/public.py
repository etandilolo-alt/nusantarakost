from flask import Blueprint, render_template
from database.db import fetch_rooms

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def home():
    rooms = fetch_rooms()
    available_rooms = [r for r in rooms if r.status == 'Tersedia']
    total_rooms = len(rooms)
    total_available = len(available_rooms)
    total_occupied = total_rooms - total_available
    
    # Latest 3 available rooms for landing page
    featured_rooms = available_rooms[:3]
    
    return render_template('public/index.html', 
                           rooms=featured_rooms, 
                           total_rooms=total_rooms, 
                           total_available=total_available, 
                           total_occupied=total_occupied)

@public_bp.route('/kamar')
def room_catalog():
    rooms = fetch_rooms()
    return render_template('public/kamar.html', rooms=rooms)

@public_bp.route('/about')
def about():
    return render_template('public/about.html')

@public_bp.route('/contact')
def contact():
    return render_template('public/contact.html')
@public_bp.route('/facilities')
def facilities():
    return render_template('public/facilities.html')

