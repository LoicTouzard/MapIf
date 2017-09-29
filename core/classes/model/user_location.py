#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: user_location.py
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
from sqlalchemy                 import String
from sqlalchemy                 import Integer
from sqlalchemy                 import DateTime
from sqlalchemy                 import ForeignKey
from sqlalchemy                 import UniqueConstraint
from core.classes.model.base    import MapifBase
from core.classes.model.session import session
from core.modules               import logger
#===============================================================================
# GLOBALS
#===============================================================================
modlgr = logger.get('mapif.user_location')
#===============================================================================
# CLASSES
#===============================================================================
#-------------------------------------------------------------------------------
# UserLocation
#-------------------------------------------------------------------------------
class UserLocation(MapifBase):
    __tablename__ = 'user_location'
    __table_args__ = (
        UniqueConstraint('uid', 'timestamp'),
        {
            'useexisting': True, 
            'sqlite_autoincrement': True # <!> SQLITE <!>
        }
    )
    #---------------------------------------------------------------------------
    # attributes
    #---------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, nullable=False)
    uid = Column(Integer, ForeignKey('user.id'))
    lid = Column(Integer, ForeignKey('location.id'))
    timestamp = Column(DateTime, default=func.now())
    meta = Column(Text, default='{}') # the ugliest thing ever => maybe we'll find another solution one day.
    #---------------------------------------------------------------------------
    # as_dict
    #---------------------------------------------------------------------------
    def as_dict(self):
        return {
            'ulid': self.id,
            'uid': self.uid,
            'lid': self.lid,
            'timestamp': self.timestamp,
            'meta': self.meta # the ugliest thing ever => maybe we'll find another solution one day.
        }
    #---------------------------------------------------------------------------
    # __repr__
    #---------------------------------------------------------------------------
    def __repr__(self):
        return """<UserLocation(id='{0}', uid='{1}', lid='{2}', 
    timestamp='{3}',
    meta='{4}'
)>""".format(self.id, self.uid, self.lid, self.timestamp, self.meta)
#-------------------------------------------------------------------------------
# UserLocationCRUD
#-------------------------------------------------------------------------------
class UserLocationCRUD:
    ATTRIBUTES = [
        'ulid',
        'uid',
        'lid',
        'timestamp',
        'meta'
    ]
    #---------------------------------------------------------------------------
    # __apply_filters
    #---------------------------------------------------------------------------
    @staticmethod
    def __apply_filters(q, **kwargs):
        for key, val in kwargs.items():
            if val is not None:
                if key == 'ulid': 
                    q = q.filter(UserLocation.id == val)
                elif key == 'uid':
                    q = q.filter(UserLocation.uid == val)
                elif key == 'lid':
                    q = q.filter(UserLocation.lid == val)
                elif key == 'timestamp':
                    q = q.filter(UserLocation.timestamp == val)
                elif key == 'meta':
                    q = q.filter(UserLocation.meta == val)
                else:
                    modlgr.warning('retrieve() argument "{0}" will be ignored.'.format(
                        key))
        return q
    #---------------------------------------------------------------------------
    # create 
    #---------------------------------------------------------------------------
    @staticmethod
    def create(uid, lid, timestamp, meta):
        s = session()
        s.add(UserLocation(uid=uid, lid=lid, timestamp=timestamp, meta=meta)) 
        s.commit()
        s.close()
    #---------------------------------------------------------------------------
    # retrieve 
    #---------------------------------------------------------------------------
    @staticmethod
    def retrieve(**kwargs):
        s = session()
        q = s.query(UserLocation)
        q = UserLocationCRUD.__apply_filters(q, **kwargs)
        return (s, q)
    #---------------------------------------------------------------------------
    # update
    #---------------------------------------------------------------------------
    @staticmethod
    def update(uid, ulid, **kwargs):
        state = False
        s = session()
        # SEC-NOTE: test ulid and uid, even if uid is a foreign key, to prevent a 
        #           user updating a record of another user.
        uloc = s.query(UserLocation).filter(
            UserLocation.id == ulid,
            UserLocation.uid == uid).one_or_none()
        if uloc is not None:
            for key, val in kwargs.items():
                if val is not None and key in UserLocationCRUD.ATTRIBUTES:
                    if key == 'id':
                        modlgr.warning('update() cannot update id.')
                        continue
                    setattr(uloc, key, val)
            s.add(uloc)
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
        q = s.query(UserLocation)
        q = UserLocationCRUD.__apply_filters(q, **kwargs)
        q.delete()
        s.commit()
        s.close()
