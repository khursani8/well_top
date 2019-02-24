from flask import Flask, render_template, request, json
from flask import jsonify
from base64 import b64encode
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/salvador")
def salvador():
    return "Hello, Salvador"


@app.route('/endpoint', methods=['GET', 'POST'])
def parse_request():
    if request.method == 'POST':
        # force = True to ignore data type checks
        msg = request.get_json(force=False)
        print(type(msg))
        print(msg.keys())
        cutoff = msg['GR_CUTOFF']
        files = msg['files']
        print(f'cutoff:{cutoff}, totalWell:{len(files)}')
        path_to_png = "data/mockuplog.jpeg"
        # model do something and generate image
        with open(path_to_png, 'rb') as f:
            binary_file = f.read()
        return b64encode(binary_file)
        # return('POST msg received!\n')

        # TODO: Parse file
        # TODO: Push file into classifier
    elif request.method == 'GET':
        return('Hello there! GET received! \n')


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    # TODO: Load models
    app.run(debug=True, host='0.0.0.0', port=5000)
