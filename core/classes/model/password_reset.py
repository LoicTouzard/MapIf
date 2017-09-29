#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: password_reset.py
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
from sqlalchemy                 import func
from sqlalchemy                 import Text
from sqlalchemy                 import Column
from sqlalchemy                 import Integer
from sqlalchemy                 import Boolean
from sqlalchemy                 import DateTime
from sqlalchemy                 import ForeignKey
from core.classes.model.base    import MapifBase
from core.classes.model.session import session
from core.modules               import logger
#===============================================================================
# GLOBALS
#===============================================================================
modlgr = logger.get('mapif.password_reset')
#===============================================================================
# CLASSES
#===============================================================================
#-------------------------------------------------------------------------------
# PasswordReset
#-------------------------------------------------------------------------------
class PasswordReset(MapifBase):
    __tablename__ = 'password_reset'
    __table_args__ = {
        'useexisting': True, 
        'sqlite_autoincrement': True # <!> SQLITE <!>
    }
    #---------------------------------------------------------------------------
    # attributes
    #---------------------------------------------------------------------------
    uid = Column(Integer, ForeignKey('user.id'), primary_key=True)
    token = Column(Text)
    timestamp = Column(DateTime, default=func.now())
    used = Column(Boolean)
    #---------------------------------------------------------------------------
    # __repr__
    #---------------------------------------------------------------------------
    def __repr__(self):
        return """<PasswordReset(uid='{0}', 
    token='{1}', 
    timestamp='{2}', 
    used='{3}'
)>""".format(self.uid, self.token, self.timestamp, self.used)
#-------------------------------------------------------------------------------
# PasswordResetCRUD
#-------------------------------------------------------------------------------
class PasswordResetCRUD:
    ATTRIBUTES = [
        'uid',
        'token',
        'timestamp',
        'used'
    ]
    #---------------------------------------------------------------------------
    # __apply_filters
    #---------------------------------------------------------------------------
    @staticmethod
    def __apply_filters(q, **kwargs):
        for key, val in kwargs.items():
            if val is not None:
                if key == 'uid': 
                    q = q.filter(PasswordReset.uid == val)
                elif key == 'token':
                    q = q.filter(PasswordReset.token == val)
                elif key == 'timestamp':
                    q = q.filter(PasswordReset.timestamp == val)
                elif key == 'used':
                    q = q.filter(PasswordReset.used == val)
                else:
                    modlgr.warning('retrieve() argument "{0}" will be ignored.'.format(
                        key))
        return q
    #---------------------------------------------------------------------------
    # create 
    #---------------------------------------------------------------------------
    @staticmethod
    def create(uid, token, timestamp, used):
        s = session()
        s.add(PasswordReset(uid=uid, token=token, timestamp=timestamp, used=used))
        s.commit()
        s.close()
    #---------------------------------------------------------------------------
    # retrieve 
    #---------------------------------------------------------------------------
    @staticmethod
    def retrieve(**kwargs):
        s = session()
        q = s.query(PasswordReset)
        q = PasswordResetCRUD.__apply_filters(q, **kwargs)
        return (s, q)
    #---------------------------------------------------------------------------
    # update
    #---------------------------------------------------------------------------
    @staticmethod
    def update(uid, **kwargs):
        state = False
        s = session()
        pwrst = s.query(PasswordReset).filter(PasswordReset.uid == uid).one_or_none()
        if pwrst is not None:
            for key, val in kwargs.items():
                if val is not None and key in PasswordResetCRUD.ATTRIBUTES:
                    if key == 'uid':
                        modlgr.warning('update() cannot update uid.')
                        continue
                    setattr(pwrst, key, val)
            s.add(pwrst)
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
        q = s.query(PasswordReset)
        q = PasswordResetCRUD.__apply_filters(q, **kwargs)
        q.delete()
        s.commit()
        s.close()
