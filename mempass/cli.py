"""
Mempass password memorization helper

author: Terrel Shumway
website: https://geekspacenine.com/mempass/
"""

import sys
import os
import click

from mempass.ui import mainloop
from mempass.model import PassCheck


@click.command()
@click.option("--db", "-d", metavar="DB", default="mempass.db", type=click.Path(), help="read passwords from DB")
@click.argument("key", default="master")
def main(key, db=None):
    mainloop(db, key)
