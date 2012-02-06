class DictSavepoint(object):

    def __init__(self, dm):
        self.dm = dm 
        self.saved_committed = self.dm.uncommitted.copy()

    def rollback(self):
        self.dm.uncommitted = self.saved_committed.copy()
