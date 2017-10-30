from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(1000))

    def __init__(self, title, content):
        self.title = title
        self.content = content


@app.route('/blog', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def index():
    posts = Blog.query.all()

    if request.args.get('id'):
        post_id = (request.args.get('id'))
        post = Post.query.filter_by(id=post_id).first()
        return render_template('singleblog.html', post=post)

    return render_template('blog.html', title="Build-A-Blog", posts=posts)


@app.route('/newpost', methods=['POST', 'GET'])
def create_new_post():
    if request.method == 'POST':
        post_name = request.form['title']
        post_content = request.form['content']
        new_post = Blog(post_name, post_content)
        db.session.add(new_post)
        db.session.commit()
        post = Blog.query.filter_by(id=new_post.id).first()
        return render_template('singleblog.html', post=post)
    else:
        return render_template('newpost.html', title='Add a Blog Entry')


if __name__ == '__main__':
    app.run()
