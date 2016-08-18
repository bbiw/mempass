
from os.path import commonprefix as _cp
import random
import yaml
import traceback


class PassDB:
    def __init__(self,dbpath):
        self.dbpath = dbpath
        self.data = None
        self.readDB()

    def readDB(self):
        try:
            with open(self.dbpath,"rt") as fi:
                d = yaml.load(fi.read())
            self.data = d
        except:
            traceback.print_exc()

    def writeDB():
        pass

    def getChecker(self,key="master"):
        pc = self.data.get(key)
        return PassCheck(pc)


class PassCheck:
    PROMPT_TEMPLATE = "<b style='background-color:green;'>{0}</b><b style='color:red;'>{1}</b>{2}"

    def __init__(self,ds,dot="·"):
        password = ds["password"]
        lp = len(password)
        self.__pw = password

        hidecount = ds["history"][-1]["hidden"]
        self.__hc = min(max(0,hidecount),lp)
        self.__hi = max(1,(lp-self.__hc)//8)

        self.realm = ds.get("realm","unspecified")
        self.user = ds.get("user","unspecified")
        
        self.__dot = dot
        ho = list(range(lp))
        random.shuffle(ho)
        self.__horder = ho
        self.__prompt = self._obscure()

    def _obscure(self):
        """replace some characters in the prompt with a dot"""
        t = list(self.__pw)
        for i in self.__horder[:self.__hc]:
            t[i] = self.__dot
        return "".join(t)

    def _prefix(self,a,b,c):
        p = _cp((a,b))
        l = len(p)
        aa = "·"*l # a[:l]
        bb = a[l:]
        cc = c[len(a):]
        return self.PROMPT_TEMPLATE.format(aa,bb,cc)

    def check(self,text):
        """return True if proposed matches the actual password

        on success, increase the number of hidden characters in the prompt
        on failure, decrease the number of hidden characters in the prompt
        """
        ok = self.__pw == text
        if ok:
            self.__hc = min(len(self.__pw),self.__hc + self.__hi)
        else:
            self.__hc  = max(0,self.__hc - self.__hi)
        self.__prompt = self._obscure()
        return ok

    def prompt(self,proposed):
        """return a prompt based on how well proposed matches password
        """
        return self._prefix(proposed,self.__pw,self.__prompt)
