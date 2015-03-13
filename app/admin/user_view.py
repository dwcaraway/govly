__author__ = 'dave'
from . import MyModelView
from ..models.users import User

class UserView(MyModelView):

    column_exclude_list = ('password', 'secret')


    def __init__(self, session):
        """
        Creates a new user view.

        :param session: An SQLAlchemy session object e.g. db.session
        :return: the created instance
        """
        return super(UserView, self).__init__(User, session)