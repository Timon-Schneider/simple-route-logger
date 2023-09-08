import csv
from flask import Flask, render_template, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import googlemaps
from dotenv import load_dotenv
from datetime import datetime  
import pytz
import os

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment
api_key = os.getenv("API_KEY")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Initialize the Google Maps client with API key
gmaps = googlemaps.Client(key=api_key)  

class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    street = db.Column(db.String(255))
    house_number = db.Column(db.String(255))
    town = db.Column(db.String(255))
    postcode = db.Column(db.String(255))
    driving_distance = db.Column(db.String(255))
    timezone = pytz.timezone('Europe/Berlin')  # Set the timezone to Berlin
    timestamp = db.Column(db.String(16), default=datetime.now(timezone).strftime("%d.%m.%Y %H:%M"))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])

        # Perform reverse geocoding to get street, house_number, town, and postcode
        location_data = reverse_geocode(latitude, longitude)
        street = location_data.get('street', 'N/A')
        house_number = location_data.get('house_number', 'N/A')
        town = location_data.get('town', 'N/A')
        postcode = location_data.get('postcode', 'N/A')

        # Calculate driving distance to the previous location
        previous_position = Position.query.order_by(Position.id.desc()).first()
        if previous_position:
            previous_latlng = (previous_position.latitude, previous_position.longitude)
            current_latlng = (latitude, longitude)
            distance = calculate_driving_distance(previous_latlng, current_latlng)
        else:
            distance = 'N/A'

        position = Position(latitude=latitude, longitude=longitude, street=street, house_number=house_number, town=town, postcode=postcode, driving_distance=distance)
        db.session.add(position)
        db.session.commit()

        return redirect(url_for('index'))

    positions = Position.query.all()
    return render_template('index.html', positions=positions)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_position(id):
    position = Position.query.get_or_404(id)
    db.session.delete(position)
    db.session.commit()

    return redirect(url_for('index'))  

@app.route('/delete_all', methods=['GET', 'POST'])
def delete_all_positions():
    if request.method == 'POST':
        # Delete all positions from the database
        Position.query.delete()
        db.session.commit()

        return redirect(url_for('index'))  # Redirect back to the index page

    return render_template('delete_all.html')  # Render a confirmation page

@app.route('/export_csv', methods=['GET'])
def export_csv():
    positions = Position.query.all()

    # Create a CSV string from the database entries (including date and time)
    csv_data = "Datum und Uhrzeit,Straße,Hausnummer,Ort,Fahrt­weg\n"
    for position in positions:
        csv_data += f"{position.timestamp},{position.street},{position.house_number},{position.postcode} {position.town},{position.driving_distance}\n"

    # Create a response with the CSV data and appropriate headers
    response = Response(csv_data, content_type='text/csv')
    response.headers["Content-Disposition"] = "attachment; filename=positions.csv"

    return response


@app.route('/export_pdf', methods=['GET'])
def export_pdf():
    positions = Position.query.all()

    # Create a PDF document
    pdf_buffer = BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    elements = []

    # Define table data and style
    table_data = [["Datum und Uhrzeit", "Straße", "Haus\nnummer", "Ort", "Fahrt­weg"]]
    total_distance_km = 0  # Initialize total distance in kilometers

    for position in positions:
        table_data.append([
            position.timestamp,
            position.street,
            position.house_number,
            f"{position.postcode} {position.town}",
            position.driving_distance
        ])
        
        # Calculate total distance
        if position.driving_distance != 'N/A':
            distance_parts = position.driving_distance.split(' ')
            value = float(distance_parts[0])
            unit = distance_parts[1]
            
            if unit == 'km':
                total_distance_km += value
            elif unit == 'm':
                # Convert meters to kilometers (fraction of a kilometer)
                total_distance_km += value / 1000

    table = Table(table_data, colWidths=[95, 200, 45, 160, 55])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    elements.append(Spacer(1, 20))

    # Add the total kilometers driven
    total_distance_paragraph = Paragraph(f"Kilometer Gesamt: {total_distance_km:.2f} km", getSampleStyleSheet()['Normal'])
    elements.append(total_distance_paragraph)

    pdf.build(elements)

    # Move the file pointer to the beginning of the buffer
    pdf_buffer.seek(0)

    # Create a response with the PDF data and appropriate headers
    response = Response(pdf_buffer.read(), content_type='application/pdf')
    response.headers["Content-Disposition"] = "attachment; filename=positions.pdf"

    return response

@app.route('/edit/<int:id>', methods=['POST'])
def edit_position(id):
    if request.method == 'POST':
        edited_timestamp = request.form['edited_timestamp']
        edited_street = request.form['edited_street']
        edited_house_number = request.form['edited_house_number']
        edited_town = request.form['edited_town']
        edited_postcode = request.form['edited_postcode']

        position = Position.query.get_or_404(id)
        position.timestamp = edited_timestamp
        position.street = edited_street
        position.house_number = edited_house_number
        position.town = edited_town
        position.postcode = edited_postcode

        # Perform geocoding to obtain the latitude and longitude based on the modified address
        updated_address = f"{edited_street} {edited_house_number}, {edited_postcode} {edited_town}"
        latlng = geocode_address(updated_address)
        if latlng:
            position.latitude, position.longitude = latlng

        # Calculate driving distance from the entry before the one being edited
        previous_position = Position.query.filter(Position.id < id).order_by(Position.id.desc()).first()
        if previous_position:
            previous_latlng = (previous_position.latitude, previous_position.longitude)
            current_latlng = (position.latitude, position.longitude)
            distance = calculate_driving_distance(previous_latlng, current_latlng)
            position.driving_distance = distance
        db.session.commit()

        return redirect(url_for('index'))
    
def geocode_address(address):
    try:
        # Use the Google Maps Geocoding API to obtain latitude and longitude based on the address
        geocode_result = gmaps.geocode(address)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            return location['lat'], location['lng']
    except Exception as e:
        print(f"Error geocoding address: {str(e)}")
    return None

def reverse_geocode(latitude, longitude):
    try:
        # Use the Google Maps Geocoding API for reverse geocoding
        location = gmaps.reverse_geocode((latitude, longitude))[0]
        components = location['address_components']

        street = next((comp['long_name'] for comp in components if 'route' in comp['types']), 'N/A')
        house_number = next((comp['long_name'] for comp in components if 'street_number' in comp['types']), 'N/A')
        town = next((comp['long_name'] for comp in components if 'locality' in comp['types']), 'N/A')
        postcode = next((comp['long_name'] for comp in components if 'postal_code' in comp['types']), 'N/A')

        return {'street': street, 'house_number': house_number, 'town': town, 'postcode': postcode}
    except Exception as e:
        print(f"Error in reverse geocoding: {str(e)}")
        return {'street': 'N/A', 'house_number': 'N/A', 'town': 'N/A', 'postcode': 'N/A'}

def calculate_driving_distance(origin, destination):
    try:
        # Use the Google Maps Directions API to calculate driving distance
        directions = gmaps.directions(origin, destination, mode="driving")
        if directions and 'legs' in directions[0]:
            return directions[0]['legs'][0]['distance']['text']
        else:
            return 'N/A'
    except Exception as e:
        print(f"Error calculating driving distance: {str(e)}")
        return 'N/A'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=80)