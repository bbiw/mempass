"""
Data model for password checker
"""
# --*-- coding: utf-8 --*--


import os
from os.path import commonprefix as _cp
import random
import time
from datetime import datetime
import traceback
import yaml
import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import exc as orm



### SQLAlchemy models

Base = declarative_base()

class Secret(Base):
    __tablename__ = 'secrets'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    realm = Column(String)
    username = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<Secret(name='{}', realm='{}' username='{}', password='{}')>".format(
            self.name, self.realm, self.username, self.password)


class Attempt(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True)
    when = Column(DateTime)
    errors = Column(Integer)  # distance between entered and actual
    work = Column(Integer)    # (roughly) the number of keystrokes
    # milliseconds between first and final keystrokes
    elapsed = Column(Integer)
    secret_id = Column(Integer, ForeignKey('secrets.id'))

    secret = relationship("Secret", back_populates="history")

    def __repr__(self):
        return "<Attempt(when='{}', errors={}, work={}, elapsed={})>".format(
            self.when, self.errors, self.work, self.elapsed)

Secret.history = relationship(
        "Attempt", order_by=Attempt.when, back_populates="secret")




### Helper functions

try:
    tick = time.monotonic
except AttributeError:
    tick = time.time


def calculate_error_distance(actual,expected):
    """Return the Hamming distance between two strings

    if lengths are unequal, the shorter is padded with '\0'
    """
    l1 = len(actual)
    l2 = len(expected)
    if l1<l2:
        actual = actual + "\0"*(l2-l1)
    elif l2<l1:
        expected = expected + "\0"*(l1-l2)
    return sum(el1 != el2 for el1, el2 in zip(actual, expected))


### Domain models

class PassDB:
    """Persistent storage for passwords being memorized

    TODO: replace this with something sensible
    TODO: consider how to encrypt secret material
    """

    def __init__(self, dbpath):
        self.dbpath = dbpath
        self.engine = engine = sqlalchemy.create_engine("sqlite:///" + dbpath)
        Base.metadata.create_all(engine)
        self.Session = sqlalchemy.orm.session.sessionmaker(bind=self.engine)
        self.session = self.Session()

    def create(self):
        Secret.metadata.create_all(self.engine)

    def save(self):
        """Write changes to persistent storage."""
        self.session.commit()

    def getChecker(self, key="master"):
        try:
            it = self.session.query(Secret).filter(Secret.name == key).one()
        except orm.NoResultFound as e:
            from mempass import ui
            newpass = ui.NewPassDlg.doModal(key)
            it = Secret(**newpass)
            self.session.add(it)
        return PassCheck(self, it)


class PassCheck:
    PROMPT_TEMPLATE = "<b style='background-color:green;'>{0}</b><b style='color:red;'>{1}</b>{2}"

    def __init__(self, db, secret, dot="·"):
        self.db = db
        self.__secret = secret
        self.key = secret.name
        self.realm = secret.realm
        self.user = secret.username

        password = secret.password
        lp = len(password)
        self.__pw = password

        self.work = 0
        self.start = None

        hidecount = random.randint(1,lp) # !!! do better at this
        self.__hc = min(max(0, hidecount), lp)
        self.__hi = max(1, (lp - self.__hc) // 8)
        self.__dot = dot
        ho = list(range(lp))
        random.shuffle(ho)
        self.__horder = ho
        self.__prompt = self._obscure()

    def _obscure(self):
        """replace some characters in the prompt with a dot."""
        t = list(self.__pw)
        for i in self.__horder[:self.__hc]:
            t[i] = self.__dot
        return "".join(t)

    def _prefix(self, proposed, password, masked):
        """determine which parts of proposed are correct.

        TODO: Do better at detecting insertions and deletions.
            This will reduce visual exposure of correct material.
        TODO: Move PROPMT_TEMPLATE into the view: this function
              should return a sequence of tuple (category,text)
              where category is one of "good"|"fail"|"missing".
              The ui should figure out how to style these chunks.
        """
        p = _cp((proposed, password))
        l = len(p)
        good = "·" * l
        fail = proposed[l:]
        missing = masked[len(masked):]
        return self.PROMPT_TEMPLATE.format(good, fail, missing)

    def check(self, text):
        """return True if proposed matches the actual password.

        on success, increase the number of masked characters in the prompt
        on failure, decrease the number of masked characters in the prompt
        """
        end = tick()
        ok = self.__pw == text
        self.__secret.history.append(Attempt(when=datetime.utcnow(),
            errors=calculate_error_distance(text,self.__pw),
            work=self.work,
            elapsed=round((end-self.start)*1000)))
        self.db.save()
        if ok:
            self.__hc = min(len(self.__pw), self.__hc + self.__hi)
        else:
            self.__hc = max(0, self.__hc - self.__hi)
        self.__prompt = self._obscure()

        self.start = None
        self.work = 0
        return ok

    def prompt(self, proposed):
        """return a prompt based on how well proposed matches password."""
        if self.start:
            self.work+=1
        else:
            self.start = tick()
        return self._prefix(proposed, self.__pw, self.__prompt)
