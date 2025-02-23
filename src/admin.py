import os
from flask_admin import Admin
from models import db, User, People, Planets, Favs_planets, Favs_people
from flask_admin.contrib.sqla import ModelView

class FavsPlanetsView(ModelView):
    column_list = ('users_id', 'planets_id')
    form_columns = ('users_id', 'planets_id')

class FavsPeopleView(ModelView):
    column_list = ('users_id', 'people_id')
    form_columns = ('users_id', 'people_id')

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(People, db.session))
    admin.add_view(ModelView(Planets, db.session))
    admin.add_view(FavsPlanetsView(Favs_planets, db.session))
    admin.add_view(FavsPeopleView(Favs_people, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))