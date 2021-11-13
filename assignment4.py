import SQLAlchemy as SQLAlchemy
from flask import Flask , render_template, redirect , url_for
from flask import request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0:@localhost/assignment4'
db = SQLAlchemy(app)

class Coin(db.Model):
    __tablename__ = 'coins'
    id = db.Column('id',db.Integer,primary_key=True)
    coin = db.Column('coin', db.Unicode)
    news = db.Column('news',db.Unicode)

    def __init__(self,coin,news):
        self.coin = coin
        self.news = news


class Scrap:
    
    def pars(self, cryptocoin):
        r = requests.get('https://cryptonews.com/news/' + cryptocoin + '-news/')
        with open("index.txt", "w", encoding='utf-8') as f:
            f.write(r.text)

        with open("index.txt", encoding='utf-8') as fp:
            soup = BeautifulSoup(fp, 'html.parser')
            for div in soup.find_all("div", {'class':'article__badge article__badge--md mb-10 pt-10'}): 
                div.decompose()
           

        paragraphs = soup.find_all("div", class_='col-12 col-md-7 column-45__right d-flex flex-column justify-content-center')
        
        coin_news=[]

        for item in paragraphs:
            coin_news.append(item.text)

           
 
        return coin_news
        
        
        
    
        

@app.route('/coin',methods=["POST","GET"])
def coin():
    if request.method == "POST":
        c = request.form['coin']
        data =Coin.query.filter_by(coin=c).first()
        if data:
            return redirect(url_for('crypto',crypto=c))
        scrap = Scrap()
        n=scrap.pars(c)
        coin = Coin(coin=c,news=n)
        db.session.add(coin)
        db.session.commit()
        return redirect(url_for('crypto',crypto=c))
    else:
        return render_template("coin.html")

@app.route('/<crypto>',methods=["POST","GET"])
def crypto(crypto):
    if request.method == "POST":
        c = request.form['coin']
        data =Coin.query.filter_by(coin=c).first()
        if data:
            new = str(data.news).replace('"', " ").replace("{"," ").replace("}"," ").replace("\\n",'')
            l = new.split(' , ')
            return render_template("crypto.html", values = l, title = data.coin)

        scrap = Scrap()
        n=scrap.pars(c)
        coin = Coin(coin=c,news=n)
        db.session.add(coin)
        db.session.commit()
        return redirect(url_for('crypto',crypto=c))
    
    coins = Coin.query.filter_by(coin = crypto).first()
    new = str(coins.news).replace('"', " ").replace("{"," ").replace("}"," ").replace("\\n",'')
    l = new.split(' , ')
    return render_template("crypto.html", values = l, title = coins.coin)


if __name__ == '__main__':  
    app.run(debug=True)
