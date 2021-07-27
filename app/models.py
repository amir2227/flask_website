from app import db, login_manager, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(256), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inv_content = db.Column(db.Text, nullable=False)
    adv_content = db.Column(db.Text, nullable=False)
    bey_content = db.Column(db.Text, nullable=False)
    net_content = db.Column(db.Text, nullable=False)
    mor_content = db.Column(db.Text, nullable=False)
    inv_email = db.Column(db.String(50), nullable=False)
    inv_phone = db.Column(db.String(50), nullable=False)
    inv_address = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return super().__repr__()
