from flask import Flask, render_template, request, json
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/salvador")
def salvador():
    return "Hello, Salvador"

@app.route('/upload_file', methods=['GET', 'POST'])
epp = Flask(__name__)
def parse_request():
    if request.method == 'POST':
        # force = True to ignore data type checks
        msg = request.get_json(force=False)
        return('POST msg received!\n')
        
        # TODO: Parse file
        # TODO: Push file into classifier
    elif request.method == 'GET':
        return('Hello there! GET received! \n')


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    # TODO: Load models
    app.run(debug=True)
