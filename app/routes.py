from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, abort, session, send_from_directory, send_file
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import requests
from io import BytesIO
from app import db
from app.models import User, Post
from app.forms import LoginForm, RegistrationForm, PostForm

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
admin = Blueprint('admin', __name__)

@main.route('/')
def home():
    featured_tools = Post.query.filter_by(category='tools').order_by(Post.id.desc()).limit(3).all()
    total_users = User.query.count()
    all_users = User.query.all()
    return render_template('home.html', featured_tools=featured_tools, total_users=total_users, all_users=all_users)

@main.route('/style.css')
def serve_css():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'style.css')

@main.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'app', 'static'), filename)

@main.route('/tools')
@login_required
def tools():
    posts = Post.query.filter_by(category='tools').all()
    return render_template('tools.html', posts=posts)

@main.route('/combo')
@login_required
def combo():
    posts = Post.query.filter_by(category='combo').all()
    return render_template('combo.html', posts=posts)

@main.route('/tutorials')
@login_required
def tutorials():
    posts = Post.query.filter_by(category='tutorials').all()
    return render_template('tutorials.html', posts=posts)

@main.route('/shop')
def shop():
    posts = Post.query.filter_by(category='shop').all()
    return render_template('shop.html', posts=posts)

@main.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        webhook_url = current_app.config['DISCORD_WEBHOOK_URL']
        data = {
            "content": f"New user registered: {form.username.data}"
        }
        requests.post(webhook_url, json=data)
        
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@admin.route('/Private/111111100000/Admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username'] == current_app.config['ADMIN_USERNAME'] and \
           request.form['password'] == current_app.config['ADMIN_PASSWORD']:
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid admin credentials', 'danger')
    return render_template('admin/login.html')

@admin.route('/admin/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('admin_logged_in'):
        abort(403)  # Forbidden

    form = PostForm()
    if form.validate_on_submit():
        thumbnail = form.thumbnail.data
        file = form.file.data
        thumbnail_filename = secure_filename(thumbnail.filename)
        file_filename = secure_filename(file.filename)
        
        thumbnail_data = thumbnail.read()
        file_data = file.read()
        
        post = Post(
            title=form.title.data,
            description=form.description.data,
            thumbnail=thumbnail_data,
            thumbnail_filename=thumbnail_filename,
            file=file_data,
            file_filename=file_filename,
            category=form.category.data,
            price=form.price.data if form.category.data == 'shop' else None,
            purchase_link=form.purchase_link.data if form.category.data == 'shop' else None
        )
        db.session.add(post)
        db.session.commit()
        
        flash('Post created successfully', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/dashboard.html', form=form)

@main.route('/uploads/<int:post_id>/<filename>')
def serve_file(post_id, filename):
    post = Post.query.get_or_404(post_id)
    if filename == post.thumbnail_filename:
        return send_file(BytesIO(post.thumbnail), mimetype='image/jpeg')
    elif filename == post.file_filename:
        return send_file(BytesIO(post.file), as_attachment=True, download_name=filename)
    abort(404)

@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500