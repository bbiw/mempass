import os
import math
import pkg_resources


def slurp(fname):
    """read the contents of a file into a list of lines"""
    with open(fname, "rt") as fi:
        return fi.read().splitlines()


def bignumber(cbytes):
    """return a big random number of cbytes*8 bits"""
    return int.from_bytes(os.urandom(cbytes), 'big')


def genpass(big, *wordlists):
    """generate a sequence of words selected from wordlists

    `big` ought to be a large random number
    """
    while True:
        for wl in wordlists:
            big, small = divmod(big, len(wl))
            yield wl[small]
            if big <= 0:
                return


def getwords(wordlist):
    """return a list of all unique words in all specified files"""
    words = []
    for wl in wordlist:
        if os.path.exists(wl):
            words.extend(slurp(wl))
            continue
        rp = 'wordlists/' + wl
        if pkg_resources.resource_exists(__name__, rp):
            words.extend(pkg_resources.resource_string(
                __name__, rp).decode("utf-8").splitlines())
            continue
        click.echo('cannot find word list "{}"'.format(wl))
    return list(set(words))


def gp(words, bits, sep):
    wc = len(words)
    bitsperword = math.log(wc, 2)
    cbytes = math.ceil(bits / 8)
    ww = []
    big = bignumber(cbytes)
    bitsleft = bits
    while bitsleft > 0 and big > 0:
        big, small = divmod(big, wc)
        ww.append(words[small])
        bitsleft -= bitsperword
    return sep.join(ww), bitsperword * len(ww)

import click


@click.command()
@click.option('--wordlist', '-w', default=['default'], multiple=True)
@click.option('--count', '-c', type=int, default=8)
@click.option('--bits', '-b', type=int, default=90)
@click.option('--join', '-j', default=' ')
@click.option('--verbose/--quiet', '-v', default=False)
def cli(wordlist, count, bits, join, verbose):
    if verbose:
        click.echo('wordlists: {} count: {} bits: {}'.format(
            wordlist, count, bits))
    words = getwords(wordlist)
    for i in range(count):
        w, b = gp(words, bits, join)
        if verbose:
            print('{} bits'.format(b))
        print(w)
