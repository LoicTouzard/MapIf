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