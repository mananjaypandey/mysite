from flask import *
from flask_sqlalchemy import *
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'xxxx'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/mananjay"
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/category", methods=['GET', 'POST'])
def category():
    if 'email_id' in session:
        if request.method == 'GET':
            category=db.session.query(Category.name).all()
            return render_template("category.html",cat=category)
        elif request.method == 'POST':
            try:
                name=request.form['name']
                cat=Category(name=name)
                db.session.add(cat)
                db.session.commit()

                category=db.session.query(Category.name).all()
                return render_template("category.html",cat=category)
            except:
                db.session.rollback()
                return render_template('category.html',msg='<script>window.alert("error")</script>')
    else:
        return render_template('login.html')

@app.route("/addcategory",methods=['GET','POST'])
def addcategory():
    if 'email_id' in session:
        if request.method=='GET':
            return render_template('addcategory.html')
        elif request.method=='POST':
            try:
                category=Category(request.form['category'])
                db.session.add(category)
                db.session.commit()
                return render_template('addcategory.html',msg='<script>window.alert("error")</script>',cat=category)
            except:
                db.session.rollback()
                return render_template('addcategory.html',msg='<script>window.alert("error")</script>')
    else:
        return render_template('login.html')


@app.route("/post", methods=['GET', 'POST'])
def post():
    if request.method=='GET':
        posts = db.session.query(Posts).all()
        return render_template('post.html',Posts=posts)
    elif request.method=='POST':
        post= db.session.query(Posts).all()
        return render_template("post.html",post=post)

@app.route("/add_newpost", methods=['GET', 'POST'])
def add_newpost():
    if request.method == 'GET':
        category= db.session.query(Category.name).all()
        return render_template('add_newpost.html',cat=category)
    elif request.method == 'POST':
        try:
            category =Category.query.filter_by(name=request.form['category']).first()

            mypost = Posts(request.form['name'], request.form['title'], request.form['Date'], request.form['content'])
            mypost.blogger.append(category)
            db.session.add(mypost)
            db.session.commit()
            return redirect('/post')
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template('post.html')




@app.route("/contact")
def contact():
    return render_template("contact.html")


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mananjaypandey8519@gmail.com'
app.config['MAIL_PASSWORD'] = 'chotu123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route("/sender", methods=['GET', 'POST'])
def sender():
    if request.method == 'GET':
        return render_template('contact.html')
    elif request.method == 'POST':
        student = Students(request.form['firstname'], request.form['lastname'], request.form['email_id'],
                           request.form['country'], request.form['subject'])
        db.session.add(student)
        db.session.commit()

        msg = Message(request.form['email_id'], sender='mananjaypandey8519@gmail.com',
                      recipients=['nikcompany8@gmail.com'])
        msg.body = request.form['subject']

        mail.send(msg)
        return render_template("contact.html", msg='<script> alert("success")</script>')

    else:
        return render_template("contact.html", msg='<script>alert("invalid query");</script>')


@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        email_id = request.form['email_id']
        password = request.form['password']
        name = db.session.query(Login.password,Login.email_id).filter(Login.password==password,Login.email_id==email_id).first()
        if name:
            session['email_id']=email_id
            session['password']=password
            return render_template("Dashboard.html")
        else:
            return 'Invalid password'
    else:
        return render_template("login.html", msg='invalid')

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session.pop('email_id')
    session.pop('password')
    return render_template('login.html')


@app.route('/loginform')
def loginform():
    return render_template('login.html')


@app.route('/viewpost')
def viewpost():
    return render_template('viewPost.html',posts=Posts.query.all())

from models import *

@app.route("/subscribe",methods=['GET','POST'])
def subscribe():
    if request.method=='GET':
        return render_template("contact.html")
    if request.method=='POST':
        try:
            name=request.form["name"]
            email=request.form["email"]
            s=Subscribe(name=name,email_id=email)
            db.session.add(s)
            db.session.commit()
            msg=Message(subject='subscription email_id',sender='mananjaypandey8519@gmail.com',
                        recipients=[request.form['email_id']])
            msg.body='you have subscribe to mjblog'
            mail.send(msg)
            return render_template("contact.html",msg='<script>alert("successfully subscribed")</script>')
        except:
            db.session.rollback()
            return ('error', e)


@app.route('/view-post/',methods=['GET','POST'])
def viewPost():
    if request.args.get('cat_id'):
        id = int(request.args.get('cat_id'))
        cat = Category.query.filter_by(id=id).first()
        posts = cat.relation
    else:
        posts=Posts.query.all()
    return  render_template('view-post.html', posts=posts,categories = Category.query.all())

@app.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
    if request.method=='GET':
        return render_template('editPost.html',post=Posts.query.filter_by(id=id).first())
    elif request.method == 'POST':
        post = Posts.query.filter_by(id=id).first()
        post.title=request.form['title']
        post.content=request.form['content']
        db.session.add(post)
        db.session.commit()
        return redirect('/post')

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=80)
