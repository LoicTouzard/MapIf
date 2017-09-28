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
from sqlalchemy                 import Column
from sqlalchemy                 import Integer
from sqlalchemy                 import String
from core.classes.model.base    import MapifBase
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