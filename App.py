from click import style
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"  # Optional

# Configuring SqlAlchemy Database With Mysql -->  'mysql://root:''@localhost/Name_of_Database (If pswd present)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/Exp10'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model of the Database


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    style = db.Column(db.String(100))
    country = db.Column(db.String(100))

    def __init__(self, name, email, phone, style, country):
        self.name = name
        self.email = email
        self.phone = phone
        self.style = style
        self.country = country


# Route-->Query on Artist Data
@app.route('/')
def Index():
    all_data = Data.query.all()
    return render_template("index.html", employees=all_data)


# Route-->Inserting Data to mysql db via html forms (Can be done using flask )
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        style = request.form['style']
        country = request.form['country']

        my_data = Data(name, email, phone, style, country)
        db.session.add(my_data)
        db.session.commit()

# Command to be executed on Python Terminal
# $python
# >>>from App import db
# >>>db.create_all()

        flash("Artist Details Inserted Successfully")

        return redirect(url_for('Index'))


# Route-->Update Artists Details
@app.route('/update', methods=['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        my_data.style = request.form['style']
        my_data.country = request.form['country']

        db.session.commit()
        flash("Artist Details Updated Successfully")

        return redirect(url_for('Index'))


# Route-->Deleting Artists Details
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Artist Details Deleted Successfully")

    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)
