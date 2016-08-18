"""
ZetCode PySide tutorial

This example shows text which
is entered in a QtGui.QLineEdit
in a QtGui.QLabel widget.

author: Jan Bodnar
website: zetcode.com
last edited: August 2011
"""

import sys
import os
import click

from ui import mainloop
from model import PassCheck


@click.command()
@click.option("--db","-d",metavar="DB",default="mempass.db",type=click.Path(),help="read passwords from DB")
def cli(db=None):
    mainloop(db)
