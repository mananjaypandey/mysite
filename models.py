from blg import db


class Students(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(20))
    email_id = db.Column(db.String(50))
    country = db.Column(db.String(20))
    subject = db.Column(db.String(50))

    def __init__(self,firstname="",lastname="",email_id="",country="",subject=""):
        self.firstname =firstname
        self.lastname =lastname
        self.email_id =email_id
        self.country =country
        self.subject =subject


class Login(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.String(40))
    password = db.Column(db.String(20))

    def __init__(self, email_id="", password=""):
        self.email_id = email_id
        self.password = password

blog=db.Table('blog',
              db.Column('cat_id',db.Integer,db.ForeignKey('category.id')),
              db.Column('post_id',db.Integer,db.ForeignKey('posts.id'))
                       )


class Category(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(20))
    relation=db.relationship('Posts',secondary=blog ,backref=db.backref('blogger',lazy='dynamic'))
    def __init__(self, name=""):
        self.name=name

class Subscribe(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    email_id=db.Column(db.String(50))

    def __init__(self,email_id=""):
        self.email_id=email_id


class Posts(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    title=db.Column(db.String(30))
    Date=db.Column(db.String(20))
    content=db.Column(db.String(1000))

    def __init__(self, name="",title="",Date="" , content=""):
        self.name=name
        self.title=title
        self.Date=Date
        self.content=content












