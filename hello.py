#!/usr/bin/env python3

from distutils.debug import DEBUG
from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
import json
import os.path
from werkzeug.utils import secure_filename

# Initialise flask with the name of the script
app = Flask(__name__)

# Create a secret key to keep session secure
app.secret_key = 'dhchgfkjscksjhckj'

# Define the home page 
@app.route('/')
# Define the function to be run on the home page
def home():
    return render_template('home.html', codes=session.keys()) # Loads the page as defined in html 
                                                              # and gives it to the user
                                                              # plus codes already use this session

# Define the url creation page
@app.route('/your-url', methods=['GET', 'POST']) # define that we can both pull and push information
def your_url():
    # When submitting information from the form on the home page, act as such:
    if request.method == 'POST':
        # open an empty dictionary
        urls = {}
        # Check if the json file used to save user submissions exists
        if os.path.exists('urls.json'):
            # Assuming it does, open the file under the name urls_file
            with open('urls.json') as urls_file:
                # load the content into the dictionary
                urls = json.load(urls_file)
        
        # Check if the url code is already in use
        if request.form['code'] in urls.keys():
            # flash to jinja function in home.html the following IF code is already taken
            flash('That short name has already been taken. Try again.')
            # Correct URL so user thinks they never left home page
            return redirect(url_for('home'))

        # Check if entry is a URL or File
        # Does the submission form contain the key value URL or File?
        if 'url' in request.form.keys():
            # Update urls.json file with new URL/code pairing - mark as url entry
            urls[request.form['code']] = {'url':request.form['url']}
        # If File, do below    
        else:
            # Create a temp variable to store the information about the file
            f = request.files['file']
            # Generate a unique storage name by merging the code the user entered
            # for the file and the file's original name
            # use Secure_filename python function to ID attempts to XSS or SQl inject
            full_name = request.form['code'] + secure_filename(f.filename)
            # Define the save location for the file and refernce the above to name it
            f.save('C:/Users/Mered/Documents/URL-Short/static/user_files/' + full_name)
            # Update the urls.json file with dictionary entries for this file/code pairing
            # - mark as File entry
            urls[request.form['code']] = {'file':full_name}
        
        # Write information out to json file
        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
            session[request.form['code']] = True # Cookie for code so user can ref later

        # Load your_url confirmation page for user
        return render_template('your_url.html', code=request.form['code'])
    else:
        # If all else fails, just reload the home page
        return redirect(url_for('home'))

# Define routes to allow user entered codes to redirect to linked sites
# This works by adding the code to the end of the homepage i.e. http://home/usercode
@app.route('/<string:code>')
def redirect_to(code):
    # Checks for our dump file
    if os.path.exists('urls.json'):
        # Opens file as new variable
        with open('urls.json') as urls_file:
            # Loads contents into dictionary
            urls = json.load(urls_file)
            # Check that the code is one saved in the json file contents
            if code in urls.keys():
                # Check that the code is tied to a url not a file entry
                if 'url' in urls[code].keys():
                    # Return to the user, broswer instructions to redirect to the value (URL) matching the
                    # key (code) so long as the entry is confirmed as a 'url' entry (avoids issues with the
                    # code also matching a file entry) - reference nested dictionaries for more details
                    return redirect(urls[code]['url'])
                # If user is trying to retrieve a file however...
                else:
                    # Return instructions to browser to load stored picture
                    return redirect (url_for('static', filename='user_files/' + urls[code]['file']))
    # If user enters nonsense code, 404
    return abort(404)

# Define how 404 is reported to user
@app.errorhandler(404)
def page_not_found(error):
    # Render and return custome 404 page from templates folder and pass 404 code to browser
    return render_template('404.html'), 404

# Turn the list of codes the user has made in their current session into a JSON API
@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))

# Just in case code becomes modular, set to run in secure mode i.e. with DEBUG off
if __name__ == '__main__':
    app.run(DEBUG=False)