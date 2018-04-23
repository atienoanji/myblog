from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import ReviewForm
from flask_login import login_required
from flask_login import UserMixin
from .. import db,photos
# Review = review.Review



#views
@main.route('/')
def index():

    title = 'blog'
    return render_template('index.html', title = title)

@main.route('/blog/review/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_review(id):
    form = ReviewForm()
    blog = get_blog(id)
    if form.validate_on_submit():
        title = form.title.data
        review = form.review.data

        # update review instances
        new_review = Review(blog_id=blog.id,blog_title=title,image_path=blog.poster,blog_review=review,user=current_user)

        # save review method
        new_review.save_review()
        return redirect(url_for('.blog',id = blog.id ))

    title = f'{blog.title} review'
    return render_template('new_review.html',title = title, review_form=form, blog=blog)

# @main.route('/blog/<int:blog_id>')
# def blog(blog_id):

#     blog = blog_id
#     title = f'{blog.title}'
#     review = Review.get_reviews(blog_id)
#     return render_template('blog.html', id = blog_id,title = title,reviews = reviews)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)
    0
@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

# @main.route('/blog/review/new/<int:id>' )
# def new_review(id):
#     form = ReviewForm()
#     blog = get_blog(id)

#     if form.validate_on_submit():
#         title = form.title.data
#         review = form.review.data
#         new_review = Review(blog_id,title,blog.poster,review)
#         new_review.save_review()
#         return redirect(url_for('blog',id =blog_id))

#     title = f'{blog.title} review'
#     return render_template('new_review',title = title, ReviewForm = form, blog = blog) 
