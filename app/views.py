import os

from flask import render_template, redirect, request, url_for, flash, session
import json

from flask_wtf import file
from sqlalchemy import Integer, or_
from werkzeug.utils import secure_filename

from app import app
from .models import User

from . import db
from flask_login import login_user, logout_user, current_user, login_required

from flask_login import current_user

from .models import Films, FilmSchedule
from .forms import UploadForm, SearchForm, TimeForm, FilmScheduleForm


# home page
@app.route('/')
def homepage():
    film_info = []
    films = Films.query.all()#这种都是对象
    for film in films:
        genre = ''
        for tag in film.Genre.all():
            genre += tag.name + ' '
        afilm = [film.image, film.FilmName, film.Blurb, film.Certificate, film.Director, film.LeadActors,
                 film.FilmLength, genre, film.Ranking, film.FilmID]
        film_info.append(afilm)
        print(genre)
    return render_template('index.html', title='homepage', films=film_info)


@app.route('/search_schedule', methods=['GET', 'POST'])
def search_schedule():
    film_info = []
    form = TimeForm()
    if form.validate_on_submit():
        schedules = FilmSchedule.query.filter_by(Date=form.Date.data).all()
        for schedule in schedules:
            afilm = [schedule.film.FilmName, schedule.Room, schedule.Date, schedule.Time, schedule.film.image]
            film_info.append(afilm)
        return render_template('search.html', title='schedules', schedules=film_info, form=form)
    return render_template('search.html', title='search book', form=form)


@app.route('/<id>/<Name>')
def findall(id, Name):
    Filmimage = Films.query.get(id)
    schedules = FilmSchedule.query.filter(FilmSchedule.FID == id).all()
    film_info = []
    for schedule in schedules:
        afilm = [schedule.film.FilmName, schedule.Room, schedule.Date, schedule.Time, schedule.ScheduleID]
        film_info.append(afilm)
    print(film_info)
    return render_template('ScheduleForEach.html', title='homepage', schedules=film_info, id=id, Name=Name,
                           Film=Filmimage)


@app.route('/delete/<id>')
def delete(id):
    Film = Films.query.get(id)
    db.session.delete(Film)
    db.session.commit()
    return redirect(url_for('homepage'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if request.method == 'POST' and form.validate_on_submit():
        file = request.files['file']
        basepath = os.path.dirname(__file__)
        upload_path = os.path.join(basepath, 'static', secure_filename(file.filename))
        file.save(upload_path)

        t = Films(FilmName=form.FilmName.data,
                  Blurb=form.Blurb.data,
                  Certificate=form.Certificate.data,
                  Director=form.Director.data,
                  LeadActors=form.LeadActors.data,
                  FilmLength=form.FilmLength.data,
                  Ranking=form.Ranking.data,
                  image=file.filename)
        #append 添加多对多关系 在第三个表中
        for tag in form.Genre.data:
            t.Genre.append(tag)

        db.session.add(t)
        db.session.commit()
        flash('Upload Sccusss')
        return redirect(url_for('homepage'))

    return render_template('UploadNewFilm.html', title='homepage', form=form)


# 上架时间段
@app.route('/upload1/<id>/<Name>', methods=['GET', 'POST'])
def FilmScheduleArrange(id, Name):
    films = Films.query.get(FilmID=id)
    form = FilmScheduleForm()
    if request.method == 'POST' and form.validate_on_submit():
        t = FilmSchedule(FID=id,
                         Room=form.Room.data,
                         Date=form.Date.data,
                         Price=form.Price.data,
                         Time=form.Time.data)
        db.session.add(t)
        db.session.commit()
        flash('Upload Sccusss')
        return redirect(url_for('findall', id=id, Name=Name))

    return render_template('ScheduleUpload.html', title='Upload', form=form)


# 下架某一时间段
@app.route('/delete/schedule/<SchedulID>')
def deleteSchedul(SchedulID):
    Schedule = FilmSchedule.query.get(SchedulID)
    db.session.delete(Schedule)
    db.session.commit()
    return redirect(url_for('homepage'))
