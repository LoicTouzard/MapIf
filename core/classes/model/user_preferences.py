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
from core.classes.model.session import session
from core.modules               import logger
#===============================================================================
# GLOBALS
#===============================================================================
modlgr = logger.get('mapif.user_preferences')
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
    uid = Column(Integer, ForeignKey('user.id'), primary_key=True)
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
#-------------------------------------------------------------------------------
# UserPreferencesCRUD
#-------------------------------------------------------------------------------
class UserPreferencesCRUD:
    ATTRIBUTES = [
        'uid',
        'new_user_notif',
        'near_user_notif'
    ]
    #---------------------------------------------------------------------------
    # __apply_filters
    #---------------------------------------------------------------------------
    @staticmethod
    def __apply_filters(q, **kwargs):
        for key, val in kwargs.items():
            if val is not None:
                if key == 'uid': 
                    q = q.filter(UserPreferences.uid == val)
                elif key == 'new_user_notif':
                    q = q.filter(UserPreferences.new_user_notif == val)
                elif key == 'near_user_notif':
                    q = q.filter(UserPreferences.near_user_notif == val)
                else:
                    modlgr.warning('retrieve() argument "{0}" will be ignored.'.format(
                        key))
        return q
    #---------------------------------------------------------------------------
    # create 
    #---------------------------------------------------------------------------
    @staticmethod
    def create(uid, new_user_notif, near_user_notif):
        s = session()
        s.add(UserPreferences(uid=uid, 
            new_user_notif=new_user_notif, 
            near_user_notif=near_user_notif))
        s.commit()
        s.close()
    #---------------------------------------------------------------------------
    # retrieve 
    #---------------------------------------------------------------------------
    @staticmethod
    def retrieve(**kwargs):
        s = session()
        q = s.query(UserPreferences)
        q = UserPreferencesCRUD.__apply_filters(q, **kwargs)
        return (s, q)
    #---------------------------------------------------------------------------
    # update
    #---------------------------------------------------------------------------
    @staticmethod
    def update(uid, **kwargs):
        state = False
        s = session()
        pref = s.query(UserPreferences).filter(UserPreferences.uid == uid).one_or_none()
        if pref is not None:
            for key, val in kwargs.items():
                if val is not None and key in UserPreferencesCRUD.ATTRIBUTES:
                    if key == 'uid':
                        modlgr.warning('update() cannot update uid.')
                        continue
                    setattr(pref, key, val)
            s.add(pref)
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
        q = s.query(UserPreferences)
        q = UserPreferencesCRUD.__apply_filters(q, **kwargs)
        q.delete()
        s.commit()
        s.close()
