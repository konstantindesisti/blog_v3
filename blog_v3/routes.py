from datetime import date
from flask import abort, render_template, redirect, url_for, flash, Blueprint, request
from flask_login import login_required, login_user, logout_user, current_user
from . import db
from .models import BlogPost, Users, Comments
from .forms import CreatePostForm, UserForm, LoginForm, CommentForm
from functools import wraps
from .helpers import strip_html, gravatar_url

main = Blueprint('main', __name__)


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        if not db.session.query(Users).filter(Users.email == form.email.data).one_or_none():
            user = Users(
                name=form.name.data,
                email=form.email.data.lower().strip()
            )
            user.set_password_hash(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash(f'The account for {form.name.data} has been created!\n'
                  f'You now may create blog posts and leave comments.')
            return redirect(url_for('main.get_all_posts'))
        else:
            flash(f'Email {form.email.data} is already registered. Please Log in!')
            return redirect(url_for('main.login'))
    return render_template("register.html", form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_check = db.session.query(Users).filter(Users.email == form.email.data).one_or_none()
        if user_check:
            if user_check.check_pass(form.password.data):
                login_user(user_check)
                return redirect(url_for('main.get_all_posts'))
            else:
                flash('Incorrect password for given email')
        else:
            flash(f'Email {form.email.data} is not registered.')
    return render_template("login.html", form=form)


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.get_all_posts'))


@main.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


@main.route("/post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    form = CommentForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            comment = Comments(
                text=strip_html(form.editor.data),
                author_id=current_user.id,
                blog_id=post_id
            )
            db.session.add(comment)
            db.session.commit()
        else:
            flash('You need to log in to leave a comment')
            return redirect(url_for('main.login'))
    return render_template("post.html", post=requested_post, form=form, gravatar_url=gravatar_url)


def admin_only(user_check):
    @wraps(user_check)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.id == 1:
            return user_check(*args, **kwargs)
        else:
            return abort(403)

    return wrapper


@main.route("/new-post", methods=["GET", "POST"])
@login_required
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("main.get_all_posts"))
    return render_template("make-post.html", form=form)


@main.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("main.show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


@main.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('main.get_all_posts'))


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/contact")
def contact():
    return render_template("contact.html")


# ------------ Error Handlers ------------ #
@main.errorhandler(403)
def not_authorized(error):
    return render_template('errors/403.html', error=error)


@main.errorhandler(404)
def invalid_route(error):
    return render_template('errors/404.html', error=error)


@main.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', error=error)
