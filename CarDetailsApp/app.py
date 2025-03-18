import os
from flask import Flask, render_template, request, send_from_directory
import csv

app = Flask(__name__)

# Serve the style.css file from the templates folder
@app.route('/static/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(app.root_path, 'templates'), filename)

# Function to read car data from CSV
def read_car_data():
    car_data = []
    with open('assets/csv/cars.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            car_data.append(row)
    return car_data

# Get unique brands from CSV data, sorted alphabetically
def get_brands():
    cars = read_car_data()
    brands = list(set(car['brand'] for car in cars))
    brands.sort()  # Sorting the list alphabetically
    return brands

# Get models based on selected brand, sorted alphabetically
def get_models(brand):
    cars = read_car_data()
    models = list(set(car['model'] for car in cars if car['brand'] == brand))
    models.sort()  # Sorting the list alphabetically
    return models

# Get production years based on selected brand and model, sorted alphabetically
def get_production_years(brand, model):
    cars = read_car_data()
    years = list(set(car['production_years'] for car in cars if car['brand'] == brand and car['model'] == model))
    years.sort()  # Sorting the list alphabetically
    return years

@app.route('/', methods=['GET', 'POST'])
def index():
    brands = get_brands()  # Get the list of car brands
    user_image_url = None

    # Initialize the top and bottom banner URLs as None
    top_banner_url = None
    bottom_banner_url = None

    if request.method == 'POST':
        selected_brands = request.form.getlist('brand')  # Multiple brands can be selected
        selected_model = request.form.get('model')
        selected_year = request.form.get('production_year')
        pcd = request.form.get('pcd')
        cb = request.form.get('cb')
        et = request.form.get('et')
        contact = request.form.get('contact')
        MAIL = request.form.get('MAIL')
        FEEDBACK = request.form.get('FEEDBACK')
        Spedizione = request.form.get('Spedizione')
        user_type = request.form.get('user_type')  # Get selected user type

        # Set the image URL based on the selected user type
        if user_type == 'mondoruote':
            top_banner_url = "https://i.postimg.cc/tCg0SSqm/mondoruote-top.png"
            bottom_banner_url = "https://i.postimg.cc/RVYYPvbN/Untitled-design-4.png"
        elif user_type == 'teamvegliante':
            top_banner_url = "https://i.postimg.cc/QtjYBCVn/top-banner.png"
            bottom_banner_url = "https://i.postimg.cc/xTBsvtcm/bottom-banner.png"

        # Filter car data based on user selections
        cars = read_car_data()
        selected_cars = [car for car in cars if car['brand'] in selected_brands and
                         car['model'] == selected_model and car['production_years'] == selected_year]

        # Prepare the list of image URLs for each selected car
        image_urls = []
        for selected_car in selected_cars:
            image_urls += selected_car['image_urls'].split(',')  # Split image URLs if they're comma-separated

        return render_template('index.html', brands=brands, selected_cars=selected_cars, 
                               image_urls=image_urls, pcd=pcd, cb=cb, et=et, contact=contact, 
                               MAIL=MAIL, FEEDBACK=FEEDBACK, Spedizione=Spedizione, 
                               user_type=user_type, top_banner_url=top_banner_url, bottom_banner_url=bottom_banner_url)

    return render_template('index.html', brands=brands, user_image_url=user_image_url)

# Get models dynamically via AJAX
@app.route('/get_models', methods=['POST'])
def get_models_ajax():
    brand = request.form.get('brand')
    models = get_models(brand)
    return {'models': models}

# Get production years dynamically via AJAX
@app.route('/get_years', methods=['POST'])
def get_years_ajax():
    brand = request.form.get('brand')
    model = request.form.get('model')
    years = get_production_years(brand, model)
    return {'years': years}

if __name__ == '__main__':
    app.run(debug=True)
