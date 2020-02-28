from BooksApp import app, db
from flask import render_template, url_for, redirect, request
from BooksApp.models import Reviews
from BooksApp.forms import ReviewForm, UpdateForm
import secrets
import os
from PIL import Image
from bs4 import BeautifulSoup
import requests


@app.route('/books')
def books():
    db.create_all()
    reviews = Reviews.query.paginate(page=1, per_page=50)
    return render_template('home.html', reviews=reviews)

@app.route('/')
@app.route('/home')
def home():
    return render_template('intro.html')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/cover_pics', picture_fn)
    output_size = (210, 325)
    i = Image.open(form_picture)
    i2 = i.resize(output_size)
    i2.save(picture_path)
    return picture_fn


def find_link(book_title, book_author):
    plus_title = book_title.replace(' ', '+')
    plus_author = book_author.replace(' ', '+')
    link = 'https://www.goodreads.com/search?utf8=%E2%9C%93&query=' + plus_title + '+' + plus_author
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'lxml')
    list_of_books = soup.find('tr')
    singular_book_article = list_of_books.find('a')
    string_html = str(singular_book_article)
    split_html1 = string_html.split('href="')
    split_html2 = split_html1[1].split('" title=')
    link_final = 'https://goodreads.com'+split_html2[0]
    return link_final

def find_picture(link_final):
    random_hex = secrets.token_hex(8)
    source = requests.get(link_final).text
    soup = BeautifulSoup(source, 'lxml')
    image = soup.find(class_='bookCoverPrimary')
    a_class = image.find('a')
    b_class = str(a_class)
    link_p1 = b_class.split('src="')
    link_p2 = link_p1[1].split('"/></a>')
    image_link = link_p2[0]
    print(image_link)
    PICS2 = image_link
    picture_fn = random_hex + '.jpg'
    picture_path = os.path.join(app.root_path, 'static/cover_pics', picture_fn)
    output_size = (210, 325)
    f = open(picture_path, 'wb')
    f.write(requests.get(PICS2).content)
    f.close()
    i = Image.open(picture_path)
    i2 = i.resize(output_size)
    i2.save(picture_path)
    return random_hex + '.jpg'


@app.route('/review/new', methods=['GET', 'POST'])
def create_review():
    form = ReviewForm()
    if form.validate_on_submit():
        link = find_link(form.title.data, form.author.data)
        if form.cover.data:
            picture_file = save_picture(form.cover.data)
            Reviews.image_file = picture_file
            next_review = Reviews(title=form.title.data, rating=form.rating.data, content=form.content.data,
                                  image_file=Reviews.image_file, author=form.author.data, link=link)
        else:
            image_file = find_picture(link)
            next_review = Reviews(title=form.title.data, rating=form.rating.data, content=form.content.data,
                                  image_file=image_file, author=form.author.data, link=link)

        db.session.add(next_review)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_review.html', form=form)

@app.route('/<int:book_id>', methods=['GET', 'POST'])
def book_route(book_id):
    book = Reviews.query.get_or_404(book_id)
    return render_template('book_route.html', book=book)


@app.route('/<int:book_id>/update', methods=['GET', 'POST'])
def update_book(book_id):
    form = UpdateForm()
    book = Reviews.query.get_or_404(book_id)
    if form.validate_on_submit():
        book.title = form.title.data
        book.rating = form.rating.data
        book.content = form.content.data
        if form.cover.data:
            picture_file = save_picture(form.cover.data)
            book.image_file = picture_file
        db.session.commit()
        return redirect(url_for('book_route', book_id=book.id))
    elif request.method == 'GET':
        form.content.data = book.content
        form.title.data = book.title
        form.rating.data = book.rating
        form.author.data = book.author
    return render_template('update_book.html', form=form, book=book)

@app.route('/<int:book_id>/delete', methods=['GET', 'POST'])
def delete_book(book_id):
    book = Reviews.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))