from  PyQt5.QtWidgets import QTreeWidgetItem as QTWI
class QTreeWidgetItem(QTWI):
    def __init__(self,parent):
        QTWI.__init__(self)
        self.parent=parent


