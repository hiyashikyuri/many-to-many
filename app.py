from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.json import jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/many-to-many'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

subs = db.Table(
    'subs',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
    db.Column('channel_id', db.Integer, db.ForeignKey('channel.channel_id'))
)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    subscriptions = db.relationship('Channel', secondary=subs, backref=db.backref('subscribers', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.user_id,
            'name': self.name,
            'channels': [Channel.to_dict(c) for c in self.subscriptions]
        }


class Channel(db.Model):
    channel_id = db.Column(db.Integer, primary_key=True)
    channel_name = db.Column(db.String(20))

    def to_dict(self):
        return {
            'id': self.channel_id,
            'channel_name': self.channel_name,
        }


@app.route('/')
def index():
    return jsonify({"data": [User.to_dict(u) for u in User.query.all()]})


@app.route('/channels')
def channels():
    return jsonify({"data": [Channel.to_dict(c) for c in Channel.query.all()]})


if __name__ == '__main__':
    app.run()
