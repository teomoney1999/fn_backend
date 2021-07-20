""" Module represents a User. """

from sqlalchemy import (
    Column, String, Integer,
    DateTime, Date, Boolean,
    ForeignKey
)

from sqlalchemy import (
    Column, String, Integer, DateTime, Date, Boolean, DECIMAL, ForeignKey, Text
)
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship, backref

from application.database import db
from application.database.model import CommonModel, default_uuid


# class HoaDon(CommonModel):
#     __tablename__ = 'hoadon'
#     id = db.Column(Integer, primary_key=True)
#     ma = db.Column(String(255), unique=True)
#     ghichu = db.Column(String(255))
#     khachhang_id = db.Column(Integer, ForeignKey('khachhang.id'), nullable=False)
#     tenkhachhang = db.Column(String(255))
#     ngaymua = db.Column(DateTime)

#     thanhtien = db.Column(DECIMAL)
#     vat = db.Column(Integer, default=10)
#     tongtien = db.Column(DECIMAL)

#     chitiethoadon = db.relationship("ChiTietHoaDon", order_by="ChiTietHoaDon.id", cascade="all, delete-orphan", lazy='dynamic')

# class ChiTietHoaDon(CommonModel):
#     __tablename__ = 'chitiethoadon'
#     id = db.Column(Integer, primary_key=True)
#     hoadon_id = db.Column(Integer, ForeignKey('hoadon.id'), nullable=False)

#     hanghoa_id = db.Column(Integer, ForeignKey('hanghoa.id'), nullable=False)
#     mahanghoa = db.Column(String(255))
#     tenhanghoa = db.Column(String(255))

#     soluong = db.Column(Integer)
#     dongia = db.Column(Integer)
#     thanhtien = db.Column(Integer)


# AUTH 
roles_users = db.Table('roles_users',
                       db.Column('user_id', String, db.ForeignKey('user.id', ondelete='cascade'), primary_key=True),
                       db.Column('role_id', String, db.ForeignKey('role.id', onupdate='cascade'), primary_key=True))


class User(CommonModel): 
    __tablename__ = 'user'
    username =  db.Column(String(255), nullable=False, index=True)
    password = db.Column(String(255), nullable=False)
    salt = db.Column(String(255))

    # Relationship
    roles = db.relationship("Role", secondary=roles_users, single_parent=True)

    userinfo = db.relationship('UserInfo', back_populates='user', cascade='all, delete-orphan')
    # userinfo_id = db.Column(String, db.ForeignKey('userinfo.id'), index=True)

    # balance = db.relationship("Balance", cascade='all, delete-orphan')

    # transaction = db.relationship("Transaction", cascade='all, delete-orphan')


class UserInfo(CommonModel):
    __tablename__ = 'userinfo'
    fullname = db.Column(String(255))
    email = db.Column(String(255))
    gender = db.Column(String(255))
    phone = db.Column(String(255))
    img = db.Column(String(255)) 


    # Relationship
    user = db.relationship("User", back_populates='userinfo')
    user_id = db.Column(String, db.ForeignKey('user.id'), index=True)




class Role(CommonModel): 
    __tablename__ = 'role'
    name = db.Column(String(255), nullable=False, index=True, unique=True)
    display_name = db.Column(String(255))
    description = db.Column(String(255))

    # Relationship
    # user = db.relationship("User", secondary=roles_users, single_parent=True)


# APP
class Balance(CommonModel): 
    __tablename__ = 'balance'
    amount = db.Column(String(255))

    # Relationship
    # user = db.relationship("User")
    user_id = db.Column(String, db.ForeignKey('user.id'), nullable=False, index=True)


class Transaction(CommonModel): 
    __tablename__ = 'transaction'
    name = db.Column(String(255))
    transaction_type = db.Column(String(255))
    amount = db.Column(String(255))
    balance_before_transaction = db.Column(String(255))
    balance_after_transaction = db.Column(String(255))
    description = db.Column(String(255))

    # Relationship
    user_id = db.Column(String, db.ForeignKey('user.id'), nullable=False, index=True)








