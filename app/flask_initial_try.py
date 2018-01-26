from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def hello():
    return 'This might be a webpage'


if __name__ == "__main__":
    app.run(debug=True)

