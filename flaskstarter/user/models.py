# flaskstarter/user/models.py

# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, DateTime, SmallInteger
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from ..extensions import db
from ..utils import get_current_time, STRING_LEN
from .constants import USER, USER_ROLE, ADMIN, INACTIVE, USER_STATUS
from flask_admin.contrib import sqla

class DenormalizedText(db.TypeDecorator):
    """
    Stores denormalized primary keys that can be
    accessed as a set.
    """
    impl = db.Text

    def __init__(self, coerce=int, separator=" ", **kwargs):
        self.coerce = coerce
        self.separator = separator
        super(DenormalizedText, self).__init__(**kwargs)

    def process_bind_param(self, value, dialect):
        if value is not None:
            items = [str(item).strip() for item in value]
            value = self.separator.join(item for item in items if item)
        return value

    def process_result_value(self, value, dialect):
        if not value:
            return set()
        return set(self.coerce(item) for item in value.split(self.separator))

    def copy_value(self, value):
        return set(value)

class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    nom = Column(String(STRING_LEN))
    email = Column(String(STRING_LEN), unique=True)
    email_activation_key = Column(String(STRING_LEN))
    created_time = Column(DateTime, default=get_current_time)
    _password_hash = Column('password', String(128), nullable=False)

    @property
    def password(self):
        return self._password_hash

    @password.setter
    def password(self, password):
        self._password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password_hash, password)

    role_code = Column(SmallInteger, default=USER, nullable=False)

    @property
    def role(self):
        return USER_ROLE[self.role_code]

    def is_admin(self):
        return self.role_code == ADMIN

    def is_authenticated(self):
        return True

    status_code = Column(SmallInteger, default=INACTIVE)

    @property
    def status(self):
        return USER_STATUS[self.status_code]

    @classmethod
    def authenticate(cls, login, password):
        user = cls.query.filter(cls.email.ilike(login)).first()
        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False
        return user, authenticated

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first_or_404()

    def check_email(self, email):
        return Users.query.filter(Users.email == email).count() == 0

    def __str__(self):
        return f'{self.id}. {self.nom}'

# Administration des utilisateurs
class UsersAdmin(sqla.ModelView):
    column_list = ('id', 'nom', 'email', 'role_code', 'status_code', 'created_time', 'email_activation_key')
    column_sortable_list = ('id', 'nom', 'email', 'created_time', 'role_code', 'status_code')
    column_searchable_list = ('email',)
    column_filters = ('id', 'nom', 'email', 'created_time', 'role_code')

    form_excluded_columns = ('password',)

    form_choices = {
        'role_code': [
            (2, 'User'),
            (0, 'Admin')
        ],
        'status_code': [
            (0, 'Inactive Account'),
            (1, 'New Account'),
            (2, 'Active Account')
        ]
    }

    def __init__(self, session):
        super(UsersAdmin, self).__init__(Users, session)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()
