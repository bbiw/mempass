
from PyQt5 import QtGui,QtCore,QtWidgets

class CheckPassDlg(QtWidgets.QDialog):

    def __init__(self,title,target,remaining):
        super(CheckPassDlg, self).__init__()
        self.target = target
        self.remaining = remaining

        # init UI
        vbox = QtWidgets.QVBoxLayout(self)

        hbox = QtWidgets.QHBoxLayout()
        lbl = QtWidgets.QLabel(self)
        lbl.setText("Realm:")
        hbox.addWidget(lbl)
        lbl = QtWidgets.QLabel(self)
        lbl.setText(target.realm)
        hbox.addWidget(lbl,1)
        lbl = QtWidgets.QLabel(self)
        lbl.setText("User:")
        hbox.addWidget(lbl)
        lbl = QtWidgets.QLabel(self)
        lbl.setText(target.user)
        hbox.addWidget(lbl,1)
        vbox.addLayout(hbox)

        lrem = self.lrem = QtWidgets.QLabel(self)
        lrem.setText("remaining: {} times".format(self.remaining))
        vbox.addWidget(lrem,1)

        lbl = self.lbl = QtWidgets.QLabel(self)
        mf = QtGui.QFont('Monospace', 18)
        lbl.setFont(mf)
        lbl.setText(self.target.prompt(""))
        vbox.addWidget(lbl,1)

        qle = self.qle = QtWidgets.QLineEdit(self)
        qle.setFont(mf)
        qle.setEchoMode(qle.Password)
        vbox.addWidget(qle,1)

        qdb = QtWidgets.QDialogButtonBox
        bb = qdb(qdb.Ok|qdb.Cancel,1,self)
        vbox.addWidget(bb,1)

        self.setLayout(vbox)
        self.setWindowTitle(title)

        qle.textChanged[str].connect(self.onChanged)
        qle.returnPressed.connect(self.finish)

    def finish(self,*args):
        text = self.qle.text()
        if self.target.check(text):
            self.remaining-=1
        else:
            self.remaining+=1
        self.lrem.setText("remaining: {} times".format(self.remaining))
        if self.remaining <= 0:
            self.hide()
        self.qle.setText("") # this will trigger onChanged to adjust the prompt

    def onChanged(self, text):
        tt = self.target.prompt(text)
        self.lbl.setText(tt)
        self.lbl.adjustSize()

    @classmethod
    def doModal(cls,title,passcheck,times):
        d = cls(title,passcheck,times)
        result = d.exec_()
        return result

def mainloop(db):
    from model import PassCheck,PassDB
    pdb = PassDB(db)
    app = QtWidgets.QApplication([])
    ex = CheckPassDlg.doModal("test",pdb.getChecker(),10)
