# app.py

from flask import Flask, render_template, request, redirect, url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os
import uuid  # Import the uuid module
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure image uploading
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads'
configure_uploads(app, photos)

# Load the trained model
model = load_model('food_recognition_model.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':
            filename = secure_filename(photo.filename)
            _, file_extension = os.path.splitext(filename)
            unique_filename = f"upload_{uuid.uuid4().hex}{file_extension}"
            photo_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], unique_filename)
            photo.save(photo_path)

            # Make predictions using the trained model
            img = image.load_img(photo_path, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            predictions = model.predict(img_array)

            print("Predictions:", predictions)

            def your_mapping_function(predictions):
                # Create a list of your food categories in the same order as your training data
                food_categories = ['Chicken Biryani', 'Chicken Curry', 'Dpsa', 'Fried Rice', 'Idly', 'Poori', 'Rice', 'Vada']
    
                # Use np.argmax() to find the index of the highest prediction value
                predicted_index = np.argmax(predictions)
    
                # Return the corresponding food item
                return food_categories[predicted_index]

                
            food_item = your_mapping_function(predictions)

            print("Predicted Food Item:", food_item)

            return {'photo_path': photo_path, 'food_item': food_item}

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)