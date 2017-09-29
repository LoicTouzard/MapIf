#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: user.py
#    date: 2017-09-26
#  author: paul.dautry
# purpose:
#   
# license:
#    MapIF - Where are INSA de Lyon IF students right now ?
#    Copyright (C) 2017  Loic Touzard
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#===============================================================================
# IMPORTS
#===============================================================================
import bcrypt
from sqlalchemy                 import Column
from sqlalchemy                 import Integer
from sqlalchemy                 import String
from core.classes.model.base    import MapifBase
from core.classes.model.session import session
from core.modules               import logger 
#===============================================================================
# GLOBALS
#===============================================================================
modlgr = logger.get('mapif.user')
#===============================================================================
# CLASSES
#===============================================================================
#-------------------------------------------------------------------------------
# User
#-------------------------------------------------------------------------------
class User(MapifBase):
    __tablename__ = 'user'
    __table_args__ = {
        'useexisting': True, 
        'sqlite_autoincrement': True # <!> SQLITE <!>
    }
    #---------------------------------------------------------------------------
    # attributes
    #---------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, nullable=False)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True, nullable=False)
    pwd = Column(String)
    promo = Column(Integer)
    #---------------------------------------------------------------------------
    # as_dict
    #---------------------------------------------------------------------------
    def as_dict(self):
        return {
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'promo': self.promo
        }
    #---------------------------------------------------------------------------
    # __repr__
    #---------------------------------------------------------------------------
    def __repr__(self):
        return """<User(id='{0}',
    firstname='{1}',
    lastname='{2}',
    email='{3}',
    promo='{4}'
)>""".format(self.id, self.firstname, self.lastname, self.email, self.promo)
#-------------------------------------------------------------------------------
# UserCRUD
#-------------------------------------------------------------------------------
class UserCRUD:
    ATTRIBUTES = [
        'firstname',
        'lastname',
        'email',
        'pwd',
        'promo'
    ]
    #---------------------------------------------------------------------------
    # __apply_filters
    #---------------------------------------------------------------------------
    @staticmethod
    def __apply_filters(q, **kwargs):
        for key, val in kwargs.items():
            if val is not None:
                if key == 'uid': 
                    q = q.filter(User.id == val)
                elif key == 'firstname':
                    q = q.filter(User.firstname == val)
                elif key == 'lastname':
                    q = q.filter(User.lastname == val)
                elif key == 'email':
                    q = q.filter(User.email == val)
                elif key == 'promo':
                    q = q.filter(User.promo == val)
                else:
                    modlgr.warning('retrieve() argument "{0}" will be ignored.'.format(
                        key))
        return q
    #---------------------------------------------------------------------------
    # create 
    #---------------------------------------------------------------------------
    @staticmethod
    def create(firstname, lastname, email, pwd, promo):
        s = session()
        s.add(User(firstname=firstname, lastname=lastname, email=email, 
            pwd=pwd, promo=promo))
        s.commit()
        s.close()
    #---------------------------------------------------------------------------
    # retrieve 
    #---------------------------------------------------------------------------
    @staticmethod
    def retrieve(**kwargs):
        s = session()
        q = s.query(User)
        q = UserCRUD.__apply_filters(q, **kwargs)
        return (s, q)
    #---------------------------------------------------------------------------
    # search
    #---------------------------------------------------------------------------
    @staticmethod
    def search(firstname_filter, lastname_filter, promo_filter):
        s = session()
        res = s.query(User).filter(
            User.firstname.ilike(firstname),
            User.lastname.ilike(lastname_filter),
            User.promo.ilike(promo_filter)).all()
        s.close()
        return res
    #---------------------------------------------------------------------------
    # update
    #---------------------------------------------------------------------------
    @staticmethod
    def update(uid, **kwargs):
        state = False
        s = session()
        usr = s.query(User).filter(User.id == uid).one_or_none()
        if usr is not None:
            for key, val in kwargs.items():
                if val is not None and key in UserCRUD.ATTRIBUTES:
                    if key == 'id':
                        modlgr.warning('update() cannot update id.')
                        continue
                    if key == 'pwd':
                        val = bcrypt.hashpw(val.encode(), bcrypt.gensalt()).decode()
                    setattr(usr, key, val)
            s.add(usr)
            s.commit()
            state = True
        s.close()
        return state
    #---------------------------------------------------------------------------
    # delete 
    #---------------------------------------------------------------------------
    @staticmethod
    def delete(**kwargs):
        s = session()
        q = s.query(User)
        q = UserCRUD.__apply_filters(q, **kwargs)
        q.delete()
        s.commit()
        s.close()
