import json
import os
import threading
import time
from flask import Flask, render_template
from request import write_to_file
app = Flask(__name__, static_url_path='/static')



@app.before_first_request
def activate_job():
    def run_job():
        while True:
            write_to_file("foo.txt")
            time.sleep(72000) #Call Github to update file every 20 hours

    thread = threading.Thread(target=run_job)
    thread.start()

@app.route('/', methods=['GET'])
def home():
    obj = json.load(open('foo.txt'))
    return render_template('home.html', obj=obj)

@app.route('/l/<lang>', methods=['GET'])
def results(lang):
    return render_template('home.html', obj=obj)

# ======== Main ============================================================== #
if __name__ == "__main__":
  app.run(debug=True, use_reloader=True)
