from flask import Flask, render_template, request, flash
from flask.logging import create_logger
from wtforms import Form, FileField, validators
from werkzeug.utils import secure_filename

import os
import logging


class ReusableForm(Form):
   file_name = FileField("Select the file to upload:", validators=[validators.DataRequired()])


# Parameters
UPLOAD_FOLDER = os.environ["UPLOAD_FOLDER"]
STATIC_FOLDER = os.environ["STATIC_FOLDER"]
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

# Instantiate our application
app = Flask(__name__)

# Configure the app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER
app.config['SECRET_KEY'] = '20200504'

# Enable logging
LOG = create_logger(app)
LOG.setLevel(logging.INFO)


@app.route('/', methods = ['GET', 'POST'])
def upload():
   # Create reusable form
   form = ReusableForm(request.form)

   if (request.method == 'POST'):
      f = request.files['file_name']

      # Output file name for debugging
      LOG.info("POST request received for file %s" % (f.filename))

      if (f):         
         if (f.filename.split(".")[-1] in ALLOWED_EXTENSIONS):
            f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
            flash("File uploaded successfully.")
         else:
            flash("Please provide either JPG or JPEG file!")

      else:
         flash("Please provide the file name!")
   
   else:
      flash("...")

   # Get the files in the target folder and send their names to the template
   for file in os.listdir(STATIC_FOLDER):
      flash(os.path.join(STATIC_FOLDER, file))

   return render_template('upload.html', form=form)

		
if (__name__ == '__main__'):
   app.run(host='0.0.0.0', port=5000, debug=True)
