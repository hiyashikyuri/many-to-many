from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.json import jsonify

app = Flask(__name__)

# sqlalchemの設定
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/many-to-many'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 中間テーブル
user_hobbies = db.Table(
    'user_hobbies',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('hobby_id', db.Integer, db.ForeignKey('hobby.id'))
)

"""
python コンソールで以下のコードを実行して、UserとHobby、中間テーブルのデータを作成

user1 = User(name='Bob')
user2 = User(name='John')
user3 = User(name='Mike')
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

h1 = Hobby(name='スノボ')
h2 = Hobby(name='野球')
h3 = Hobby(name='サッカー')
db.session.add(h1)
db.session.add(h2)
db.session.add(h3)

user1.subscriptions.append(h1)
user1.subscriptions.append(h2)
user1.subscriptions.append(h3)
user2.subscriptions.append(h1)
user2.subscriptions.append(h3)
user3.subscriptions.append(h3)

db.session.commit()

"""


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    subscriptions = db.relationship('Hobby', secondary=user_hobbies, backref=db.backref('subscribers', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'hobbies': [Hobby.to_dict(c) for c in self.subscriptions]
        }


class Hobby(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }


@app.route('/')
def index():
    return jsonify({"data": [User.to_dict(u) for u in User.query.all()]})


@app.route('/hobbies')
def hobbies():
    return jsonify({"data": [Hobby.to_dict(h) for h in Hobby.query.all()]})


if __name__ == '__main__':
    app.run()
