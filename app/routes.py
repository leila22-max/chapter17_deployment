from app import app, db
from app.models import User, Post
from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template, flash, redirect, url_for, request
from flask import render_template
from app.forms import RegisterForm, AddProductForm, LoginForm, RegisterForm, EditProfileForm, PostForm, ResetPasswordRequestForm,ResetPasswordForm
from datetime import datetime
from app.email import send_password_reset_email

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()

@app.route('/reset-password/<token>', methods=['GET','POST'])
def reset_password(token):
    """Reset password URL"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your Password Has Been Reset ")
        return redirect(url_for('login'))
    return render_template(
       'reset_password.html',
        title='Reset Password',
        form=form
)

@app.route('/',  methods=['GET', 'POST'])
def landing_page():
    """Landing page URL"""
    return render_template('landing_page.html', title='Welcome')


@app.route('/home', methods=['GET', 'POST'])
@login_required
def index():
    """Index URL"""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post Is Live Now!')
        return redirect (url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page,
        per_page=app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    my_posts = Post.query.filter_by(author=current_user).order_by(Post.timestamp.desc()).paginate(
        page=page,
        per_page=app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    next_url = url_for('index', page=posts.next_num) \
    if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
    if posts.has_prev else None

    my_next_url = url_for('index', page=my_posts.next_num) \
        if posts.has_next else None
    my_prev_url = url_for('index', page=my_posts.prev_num) \
        if posts.has_prev else None
    return render_template(
        'index.html',
        title='Home',
        form=form,
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url,
        my_posts=my_posts.items,
        my_prev_url=my_prev_url,
        my_next_url=my_next_url
                                  )


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form= EditProfileForm( current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your Changes Have Been Saved')
        return redirect(url_for('profile', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',title= 'Edit Proflie',form=form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()

@app.route('/<username>/profile', methods=['GET', 'POST'])
@login_required
def profile(username):
    """Profile page """
    form= PostForm()
    user = User.query.filter_by(username=username).first_or_404()
    posts = current_user.posts.all()
    page = request.args.get('page', 1, type=int)
    posts = current_user.posts.paginate(
        page=page,
        per_page=app.config['POSTS_PER_PAGE'],
        error_out=False)
    return render_template(
        'profile.html',
        title = 'Proflie',
        user=user,
        form=form,
        post=posts.items )

  
        
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login URL"""
    if current_user.is_authenticated: 
        return redirect(url_for('index'))
    form = LoginForm() 
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid User Name Or Password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash(f'Welcome {form.username.data} ')
        return redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register URL"""
    form= RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'You Have Been Successfuly Registered! ')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)








@app.route('/request-password-reset', methods=['GET','POST'])
def request_password_reset():
    
    
    """Request Password Reset URL"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash("Kindly Check your email adress for further instructions")
        return redirect(url_for('login'))
    return render_template(
        'request_password_reset.html',
        title="Request Password Reset",
        form=form
    )


