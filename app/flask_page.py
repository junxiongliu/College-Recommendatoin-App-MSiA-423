from flask import Flask, flash, redirect, render_template, request, session, abort

app = Flask(__name__)
 
@app.route("/home")
def home_page():
  return render_template(
    'layout_homepage.html',**locals())

@app.route("/recommendation")
def recommendation_page():
  pass
 
if __name__ == "__main__":
  app.run(use_reloader=True, debug=True)

# host='0.0.0.0'