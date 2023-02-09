from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.gtwbood.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    #db.movies.remove({})
    #db.movies.deleteMany({})

    movies = soup.select('body > div.content > div > div.movie-list.slider-type1 > ul > li')
    top10_count = 1
    for movie in movies:
        a = movie.select_one('div > a > div.info > div.subj')
        if a is not None:
            title = a.text
            image = movie.select_one('div > a > div.img > img')['src']
            age = movie.select_one('div > a > div.img > span > i')['class']
            etc = movie.select_one('div > a > div.info > div.etc').text
            actor = movie.select_one('div > a > div.info > div.actor').text
            print(title, image, age, etc, actor)

        doc = {
            'title': title,
            'image': image,
            'age': age,
            'etc': etc,
            'actor': actor
        }
        db.movies.insert_one(doc)

        top10_count += 1
        if top10_count > 10:
            break

    return jsonify({'msg':'저장 완료!'})

@app.route("/movie", methods=["GET"])
def movie_get():
    movie_list = list(db.movies.find({}, {'_id':False}))
    return jsonify({'movies':movie_list})

@app.route("/movie", methods=["GET"])
def detail(id):
    # DB 조회하도록 하는 로직 작성
    # 예시: movie = db.collection.find_one({"_id": ObjectId(id)})
    # DB 조회 결과를 detail.html에 전달
    movie = db.collection.find_one({"_id": ObjectId(id)})

    return render_template("detail.html", movie=movie)

@app.route("/")
def index(id):
    # DB 조회하도록 하는 로직 작성
    # 예시: movies = db.collection.find({})
    # DB 조회 결과를 detail.html에 전달
    movies = db.collection.find({})
    return render_template("index.html", movies=movies)


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)