"""
Data model for password checker
"""
# --*-- coding: utf-8 --*--



from os.path import commonprefix as _cp
import random
import yaml
import traceback


class PassDB:
    """Persistent storage for passwords being memorized

    TODO: replace this with something sensible
    TODO: consider how to encrypt secret material
    """
    def __init__(self, dbpath):
        self.dbpath = dbpath
        self.data = None
        self.load()

    def load(self):
        """Read data from persistent storage."""
        try:
            with open(self.dbpath, "rt") as fi:
                d = yaml.load(fi.read())
            self.data = d
        except:
            traceback.print_exc()

    def save():
        """Write changes to persistent storage."""
        #!!!

    def getChecker(self, key="master"):
        pc = self.data.get(key)
        return PassCheck(key, pc)


class PassCheck:
    PROMPT_TEMPLATE = "<b style='background-color:green;'>{0}</b><b style='color:red;'>{1}</b>{2}"

    def __init__(self, key, ds, dot="·"):
        self.key = key
        self.realm = ds.get("realm", "unspecified")
        self.user = ds.get("user", "unspecified")

        password = ds["password"]
        lp = len(password)
        self.__pw = password

        hidecount = ds["history"][-1]["hidden"]
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
        ok = self.__pw == text
        if ok:
            self.__hc = min(len(self.__pw), self.__hc + self.__hi)
        else:
            self.__hc = max(0, self.__hc - self.__hi)
        self.__prompt = self._obscure()
        return ok

    def prompt(self, proposed):
        """return a prompt based on how well proposed matches password."""
        return self._prefix(proposed, self.__pw, self.__prompt)

    def save():
        """Write changes to persistent storage."""
        #!!!
