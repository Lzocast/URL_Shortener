# URL_Shortener
Basic CRUD app, made to test/learn flask implementation.

Another sprawling learning project. This takes several techniques in flask implementation for beginners and merges them. You'll see some basic jinja usage, some
intermediary html, and of course, flask. To attempt to make use of as many of flask's inbuilt features as possible the web app features some odds and ends that would
probably be trimmed out of a production grade application, and is not configured for use beyond the device it is run on.

This project also aims to act as a learning exercise for CSS class implementation.


< ============ General Setup =========== >

Download the files, place them in a new, blank, directory, and enable a virtual environment within that directory.

I'd recommend using the pipenv python package, though so long as you can install Flask into the virtual env all should be fine.

Run your virtual env i.e. 'pipenv shell'

Test if Flask installed correctly by typing 'flask' and seeing if pushing enter gets you the default, "How to use this package" text.

Set your environment variables to tell flask what app you want it to run when activated (defaults to anything in the main directory called 'app.py' if you don't want
to change anything) and if it should run in Production or Development Mode. I'd recommend the latter as it reacts to changes made in the app and updates live.

N/B: if you choose to do this on Windows, the PowerShell commands for setting environment variables will need to be in the format $env:FLASK_APP='app-name.py'
Otherwise the Export command on Linux or macOS.



< ======== Current Features ========== >

App currently allows the user to create a self named short URL for any regular URL they enter. App does not validate the URL in any way.

App can locally store a file under a unique name which may be retrieved using that name.

App displays the short URL that links to the user given URL or file.

App stores URL/Short-name and File/Unique-name in a nested dictionary JSON file that stores this key/value pair as the value in a key/value pair of object type i.e.
File or URL, and content.

App tracks the user session using a secret key and will display quick links to the user on the home page that correspond to any short-URL names created and/or files
saved.

App can display user input error messages flashed to jinja.



< ========== Planned to implement ============== > 

Copy button on the 'Your_URL' page to let user copy paste the created short link easily.

Network mode - access the app across local network safely and securely





App has been tested on macOS Monatery and Windows 11
