from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import CreatePostForm, EditPostForm, UserLoginForm, UserRegistrationForm
from app.models import Post, User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


# Decorators are wannabe emails! Look at them, with their @'s...
# I must name the app and then the method route.
# I think all of this comes from the Flask class, but I have no Idea actually.
# As a parameter, I must send the part of the url that comes after "localhost:5000".
# So, the function index() will be executed if I request "localhost:5000", "localhost:5000/", or
# "localhost:5000/index"
@app.route('/')
@app.route('/index')
# After the above mentioned requests, this function will be invoked/called, whetever.
def index():
    # I make some fake posts with the structure I'd like my posts to have.
    # Whenever I get to databases and shit. Fuck, why do I like this.
    # I couldn't just be a gardener?!
    # (This is now ancient technology.)
    #posts = [
    #    {'title': 'A Post',
    #     'body': 'Mi primer post!',
    #     'date': '28/5/2021',
    #     'time': '00:13'},
    #    {'title': 'Another Post',
    #     'body': 'Este post viene después del primero.',
    #     'date': '29/5/2021',
    #     'time': '10:33'}
    #]
    # Now that I have a db, I will abandon such list and make my own lists!
    # The next variable stores all posts through a SQLAlchemy query.
    # The all() function returns a list (or array, no idea really) with every row of that model.
    posts = Post.query.all()
    # For my next trick, I'll reverse the list:
    for i in range(len(posts)//2):
        aux = posts[i]
        posts[i] = posts[-1-i]
        posts[-1-i] = aux
    # I think every view function must end rendering something or requesting another URL,
    # which would lead to another view function which hopefully renders some shit.
    # The render_template() function here renders the template in the first parameter.
    # You may ask: How tf does the function know where the template is?? You just said the name
    # of the file, you absolute dingus!
    # Well, the function automatically looks for a directory in the app directory named "template" or
    # "templates".
    # What are the other parameters? those are the variables requested by the template.
    # Go to index.html and you'll see.
    return render_template('index.html', title='Home Page', posts=posts)


@app.route('/post', methods=['GET', 'POST'])
# This decorator required that current_user.is_authenticated = True. Otherwise
# it will redirect the client to de login view (set in __init__.py.)
@login_required
def post():
    # The view function for a form is pretty simple, except it isn't.
    # First, we create a variable and assign to it the class we created in the forms module.
    # The request object is a global instance of the Request class, it access the incoming request data.
    # The form property returns the form parameters.
    # Why we return the form parameters to the Form class? No idea, just... no fing clue.
    form = CreatePostForm()
    # We check whether the request method is POST, that is, if the user clicked the submit button.
    # If the method is GET it returns false, this happens when the page is loaded for the first time.
    # If the method is POST it will return true, this happens when the user clicks the submit button.
    # The validate on submit function checks whether the method is POST and the validators if the form
    # and returns True or False.
    if form.validate_on_submit():
        # If the method is POST, we will process the form data.
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        
        # Then we redirect the user to the index page
        return redirect(url_for('index'))
    # If the method is GET, it means the user is loading the page for the first time or
    # one of the form validators returned an error, which returned False in the above if.
    # In any case, we will just render the template for the form.
    # The template itself will manage the error handleing if needed.
    return render_template('post.html', title='Create Post', form=form)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    # When first requesting the function, it will be done so with an argument that indicates
    # the id of the post the user wishes to edit.
    # The get method of the args object of the request object takes as a parameter a string with the
    # name of the argument, and returns the value of said argument.
    id = request.args.get('p')
    # Now we get store the post in a variable for future handeling.
    # The get method takes an integer and returns an object from the db which primary key corresponds
    # with said integer.
    post = Post.query.get(id)

    # Just in case the client user and the user that created the post are different, I redirect
    # them to the index page. I'm not InfoSec so I don't know if this is possible, but I feel
    # that is awfully easy to type "/edit?p=" and a random number.
    if post.author.id != current_user.id:
        return redirect(url_for('index'))

    # Same as the create post function, we create an instance of the form class.
    # Again, I have no idea what the parameters do, I just do as the WTForms docs say.
    form = EditPostForm(obj=post)

    # In case the user clicked the submit button, the method shall be POST.
    # The user must also have passed all the tests presented by the validators.
    if form.validate_on_submit():
        # We replace the data in the db with what the user wrote.
        post.title = form.title.data
        post.body = form.body.data
        db.session.commit()
        # And redirect.
        return redirect(url_for('index'))
    # If the user is requesting the page for the first time, the method shall be GET.
    elif request.method == 'GET':
        # We shall sow the fields of thine form wif thine atributes from thine db.
        form.title.data = post.title
        form.body.data = post.body

    # If the user is requesting this page for the first time or \
    # the user did not fulfill the validators requirements:
    # The template will be rendered.
    return render_template('edit.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():

    # If a logged in user is trying to access the login form, redirect them to the index.
    # The is_authenticated() function is one of the properties added by the UserMixin class
    # to the User model in app.models.py.
    # The current user is a quick and usefull function to get the user object of the client.
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = UserLoginForm()

    # Validating the form on submit.
    if form.validate_on_submit():

        # We query a user instance through the username given in the form.
        user = User.query.filter_by(username=form.username.data).first()

        # This if checks whether the username or password are incorrect.
        if user is None or not user.check_password(form.password.data):
            flash('Nombre de usuario o contraseña incorrectos.')
            return redirect(url_for('login'))
        
        # If the user and password are correct, the user is loggend in through
        # the login_user() function, wich takes as parameters the user object and
        # I imagin the remember parameter must take a boolean value.
        login_user(user, remember=form.remember_me.data)

        # When a user is redirected to the login view through the @login_required decorator,
        # the URL request won't simply be /login, it'll be /login?next=/page_url.
        # This argument "next" must be retrieved so that we know where to redirect the client next.
        next_page = request.args.get('next')

        # In case there is no value for next page, the client will be redirected to the index.
        # If there is a value for next and this value is not a relative URL (e.g.: /index) but an
        # absolute one (e.g.: http://www.malicious.site), then the app will ignore said URL and
        # still redirect the client to the index.
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html', title='Ingresar', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = UserRegistrationForm()

    if form.validate_on_submit():

        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('¡Se creó la cuenta exitosamente!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Creación de cuenta', form=form)
