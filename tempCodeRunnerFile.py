
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
