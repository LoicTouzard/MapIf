#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: user_preferences.py
#    date: 2017-09-28
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
from sqlalchemy                 import Boolean
from sqlalchemy                 import ForeignKey
from core.classes.model.base    import MapifBase
#===============================================================================
# CLASSES
#===============================================================================
#-------------------------------------------------------------------------------
# UserPreferences
#-------------------------------------------------------------------------------
class UserPreferences(MapifBase):
    __tablename__ = 'user_preferences'
    __table_args__ = {
        'useexisting': True, 
        'sqlite_autoincrement': True # <!> SQLITE <!>
    }
    #---------------------------------------------------------------------------
    # attributes
    #---------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, nullable=False)
    uid = Column(Integer, ForeignKey('user.id'))
    # preferences
    # -- be notified when a new user subscribes to MapIF
    new_user_notif = Column(Boolean, nullable=False, default=False)
    # -- be notified if a user arrives close to your location
    near_user_notif = Column(Boolean, nullable=False, default=False)
    #---------------------------------------------------------------------------
    # as_dict
    #---------------------------------------------------------------------------
    def as_dict(self):
        return {
            'uid': self.uid,
            'new_user_notif': self.new_user_notif,
            'near_user_notif': self.near_user_notif
        }
    #---------------------------------------------------------------------------
    # __repr__
    #---------------------------------------------------------------------------
    def __repr__(self):
        return """<UserPreferences(id='{0}', uid='{1}', 
    new_user_notif='{2}', 
    near_user_notif='{3}'
)>""".format(self.id, self.uid, self.new_user_notif, self.near_user_notif)