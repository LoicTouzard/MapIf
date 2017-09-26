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
from sqlalchemy                     import func
from sqlalchemy                     import Text
from sqlalchemy                     import Column
from sqlalchemy                     import Integer
from sqlalchemy                     import Boolean
from sqlalchemy                     import DateTime
from sqlalchemy                     import ForeignKey
from sqlalchemy.ext.declarative     import declarative_base
#===============================================================================
# GLOBALS / CONFIG
#===============================================================================
Base = declarative_base()
#===============================================================================
# CLASSES
#===============================================================================
#-------------------------------------------------------------------------------
# PasswordReset
#-------------------------------------------------------------------------------
class PasswordReset(Base):
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
        return "<PasswordReset(user='{0}', token='{1}', timestamp='{2}', used='{3}')>".format(
            self.uid, self.token, self.timestamp, self.used)