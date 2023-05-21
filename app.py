from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exhibitions.db'
db = SQLAlchemy(app)

class Exhibition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    participants = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    exhibitions = Exhibition.query.all()
    return render_template('index.html', exhibitions=exhibitions)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    date = request.form.get('date')
    location = request.form.get('location')
    participants = request.form.get('participants')

    exhibition = Exhibition(name=name, date=date, location=location, participants=participants)
    db.session.add(exhibition)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete():
    exhibition_id = request.form.get('exhibition_id')

    Exhibition.query.filter_by(id=exhibition_id).delete()
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    exhibition_id = request.form.get('exhibition_id')
    name = request.form.get('name')
    date = request.form.get('date')
    location = request.form.get('location')
    participants = request.form.get('participants')

    exhibition = Exhibition.query.get(exhibition_id)
    exhibition.name = name
    exhibition.date = date
    exhibition.location = location
    exhibition.participants = participants

    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
