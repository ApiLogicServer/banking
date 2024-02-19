# coding: utf-8
from sqlalchemy import Column, DECIMAL, Date, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  February 18, 2024 15:52:42
# Database: sqlite:////Users/val/Desktop/banking/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################

from safrs import SAFRSBase
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class AccountType(SAFRSBase, Base):
    __tablename__ = 'AccountType'
    _s_collection_name = 'AccountType'  # type: ignore
    __bind_key__ = 'None'

    Name = Column(String(25), primary_key=True)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    AccountList : Mapped[List["Account"]] = relationship(back_populates="AccountType1")

    @jsonapi_attr
    def _check_sum_(self):  # type: ignore [no-redef]
        return None if isinstance(self, flask_sqlalchemy.model.DefaultMeta) \
            else self._check_sum_property if hasattr(self,"_check_sum_property") \
                else None  # property does not exist during initialization

    @_check_sum_.setter
    def _check_sum_(self, value):  # type: ignore [no-redef]
        self._check_sum_property = value

    S_CheckSum = _check_sum_


class Branch(SAFRSBase, Base):
    __tablename__ = 'Branch'
    _s_collection_name = 'Branch'  # type: ignore
    __bind_key__ = 'None'

    BranchID = Column(Integer, primary_key=True)
    Name = Column(String(100), server_default=text("NULL"))
    Office = Column(String(15), server_default=text("NULL"))
    Address = Column(String(100), server_default=text("NULL"))
    OpenDate = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    # parent relationships (access parent)

    # child relationships (access children)
    CustomerList : Mapped[List["Customer"]] = relationship(back_populates="Branch")
    EmployeeList : Mapped[List["Employee"]] = relationship(back_populates="Branch1")

    @jsonapi_attr
    def _check_sum_(self):  # type: ignore [no-redef]
        return None if isinstance(self, flask_sqlalchemy.model.DefaultMeta) \
            else self._check_sum_property if hasattr(self,"_check_sum_property") \
                else None  # property does not exist during initialization

    @_check_sum_.setter
    def _check_sum_(self, value):  # type: ignore [no-redef]
        self._check_sum_property = value

    S_CheckSum = _check_sum_


class Customer(SAFRSBase, Base):
    __tablename__ = 'Customer'
    _s_collection_name = 'Customer'  # type: ignore
    __bind_key__ = 'None'

    CustomerID = Column(Integer, primary_key=True)
    FirstName = Column(String(50), server_default=text("NULL"))
    LastName = Column(String(50), server_default=text("NULL"))
    Email = Column(String(100), server_default=text("NULL"))
    PhoneNumber = Column(String(20), server_default=text("NULL"))
    Address = Column(String(200), server_default=text("NULL"))
    BirthDate = Column(Date, server_default=text("NULL"))
    RegistrationDate = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    UserName = Column(String(64), nullable=False)
    Password = Column(String(64), nullable=False)
    BranchID = Column(ForeignKey('Branch.BranchID'), server_default=text("NULL"))

    # parent relationships (access parent)
    Branch : Mapped["Branch"] = relationship(back_populates=("CustomerList"))

    # child relationships (access children)
    AccountList : Mapped[List["Account"]] = relationship(back_populates="Customer")

    @jsonapi_attr
    def _check_sum_(self):  # type: ignore [no-redef]
        return None if isinstance(self, flask_sqlalchemy.model.DefaultMeta) \
            else self._check_sum_property if hasattr(self,"_check_sum_property") \
                else None  # property does not exist during initialization

    @_check_sum_.setter
    def _check_sum_(self, value):  # type: ignore [no-redef]
        self._check_sum_property = value

    S_CheckSum = _check_sum_


class Employee(SAFRSBase, Base):
    __tablename__ = 'Employees'
    _s_collection_name = 'Employee'  # type: ignore
    __bind_key__ = 'None'

    EmployeeID = Column(Integer, primary_key=True)
    LastName = Column(String(15), nullable=False)
    FirstName = Column(String(15), nullable=False)
    Branch = Column(ForeignKey('Branch.BranchID'), server_default=text("'1'"))
    BirthDate = Column(DateTime, server_default=text("NULL"))
    Photo = Column(String(25), server_default=text("NULL"))
    Notes = Column(String(1024), server_default=text("NULL"))

    # parent relationships (access parent)
    Branch1 : Mapped["Branch"] = relationship(back_populates=("EmployeeList"))

    # child relationships (access children)

    @jsonapi_attr
    def _check_sum_(self):  # type: ignore [no-redef]
        return None if isinstance(self, flask_sqlalchemy.model.DefaultMeta) \
            else self._check_sum_property if hasattr(self,"_check_sum_property") \
                else None  # property does not exist during initialization

    @_check_sum_.setter
    def _check_sum_(self, value):  # type: ignore [no-redef]
        self._check_sum_property = value

    S_CheckSum = _check_sum_


class Account(SAFRSBase, Base):
    __tablename__ = 'Account'
    _s_collection_name = 'Account'  # type: ignore
    __bind_key__ = 'None'

    AccountID = Column(Integer, primary_key=True)
    CustomerID = Column(ForeignKey('Customer.CustomerID'), server_default=text("NULL"))
    AccountType = Column(ForeignKey('AccountType.Name'), server_default=text("NULL"))
    AcctBalance : DECIMAL = Column(DECIMAL(15, 2), server_default=text("NULL"))
    OpenDate = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    # parent relationships (access parent)
    AccountType1 : Mapped["AccountType"] = relationship(back_populates=("AccountList"))
    Customer : Mapped["Customer"] = relationship(back_populates=("AccountList"))

    # child relationships (access children)
    TransactionLogList : Mapped[List["TransactionLog"]] = relationship(back_populates="Account")
    TransferList : Mapped[List["Transfer"]] = relationship(foreign_keys='[Transfer.FromAccountID]', back_populates="Account")
    TransferList1 : Mapped[List["Transfer"]] = relationship(foreign_keys='[Transfer.ToAccountID]', back_populates="Account1")

    @jsonapi_attr
    def _check_sum_(self):  # type: ignore [no-redef]
        return None if isinstance(self, flask_sqlalchemy.model.DefaultMeta) \
            else self._check_sum_property if hasattr(self,"_check_sum_property") \
                else None  # property does not exist during initialization

    @_check_sum_.setter
    def _check_sum_(self, value):  # type: ignore [no-redef]
        self._check_sum_property = value

    S_CheckSum = _check_sum_


class TransactionLog(SAFRSBase, Base):
    __tablename__ = 'TransactionLog'
    _s_collection_name = 'TransactionLog'  # type: ignore
    __bind_key__ = 'None'

    TransactionID = Column(Integer, primary_key=True)
    AccountID = Column(ForeignKey('Account.AccountID'), server_default=text("NULL"))
    TransactionType = Column(String(25), server_default=text("NULL"))
    TotalAmount : DECIMAL = Column(DECIMAL(15, 2), server_default=text("NULL"))
    Deposit : DECIMAL = Column(DECIMAL(15, 2), server_default=text("NULL"))
    Withdrawl : DECIMAL = Column(DECIMAL(15, 2), server_default=text("NULL"))
    ItemImage = Column(Text)
    TransactionDate = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    # parent relationships (access parent)
    Account : Mapped["Account"] = relationship(back_populates=("TransactionLogList"))

    # child relationships (access children)

    @jsonapi_attr
    def _check_sum_(self):  # type: ignore [no-redef]
        return None if isinstance(self, flask_sqlalchemy.model.DefaultMeta) \
            else self._check_sum_property if hasattr(self,"_check_sum_property") \
                else None  # property does not exist during initialization

    @_check_sum_.setter
    def _check_sum_(self, value):  # type: ignore [no-redef]
        self._check_sum_property = value

    S_CheckSum = _check_sum_


class Transfer(SAFRSBase, Base):
    __tablename__ = 'Transfer'
    _s_collection_name = 'Transfer'  # type: ignore
    __bind_key__ = 'None'

    TransactionID = Column(Integer, primary_key=True)
    FromAccountID = Column(ForeignKey('Account.AccountID'), server_default=text("NULL"))
    ToAccountID = Column(ForeignKey('Account.AccountID'), server_default=text("NULL"))
    Amount : DECIMAL = Column(DECIMAL(15, 2), server_default=text("NULL"))
    TransactionDate = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    # parent relationships (access parent)
    Account : Mapped["Account"] = relationship(foreign_keys='[Transfer.FromAccountID]', back_populates=("TransferList"))
    Account1 : Mapped["Account"] = relationship(foreign_keys='[Transfer.ToAccountID]', back_populates=("TransferList1"))

    # child relationships (access children)

    @jsonapi_attr
    def _check_sum_(self):  # type: ignore [no-redef]
        return None if isinstance(self, flask_sqlalchemy.model.DefaultMeta) \
            else self._check_sum_property if hasattr(self,"_check_sum_property") \
                else None  # property does not exist during initialization

    @_check_sum_.setter
    def _check_sum_(self, value):  # type: ignore [no-redef]
        self._check_sum_property = value

    S_CheckSum = _check_sum_
