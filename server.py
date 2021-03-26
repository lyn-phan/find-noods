from flask import Flask, render_template, redirect
import jinja2


app = Flask(__name__)
app.secret_key = 'sendNoodsNow'
# app.jinja_env.undefined = StrictUndefined

#### NAVIGATION ####
@app.route('/')
def homepage():

    return render_template('home.html')

if __name__ == '__main__':
    # connect_to_db(app)
    app.run(debug=True, host="0.0.0.0") 