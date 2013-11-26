"""
transaction datamanager
"""
import json
import os
import transaction


class DictSavepoint(object):

    def __init__(self, dm):
        self.dm = dm
        self.saved_committed = self.dm.uncommitted.copy()

    def rollback(self):
        self.dm.uncommitted = self.saved_committed.copy()


class JSONDataManager(dict):

    transaction_manager = transaction.manager
    savepoint_factory = DictSavepoint

    def __init__(self, sender, send_on_vote=False):
        # self == uncommitted
        self.send_on_vote = send_on_vote
        self.send = sender
        self.committed = self.copy()

    def abort(self, transaction):
        self.clear()
        self.update(self.committed.copy())

    def tpc_begin(self, transaction):
        pass

    def commit(self, transaction):
        pass

    def tpc_vote(self, transaction):
        devnull = open(os.devnull, 'wb')
        try:
            json.dump(self, devnull)
        except TypeError as e:
            raise ValueError("Unserializable value cannot be saved: %s" %e.message)
        self.state = 'voted'
        if self.send_on_vote is True:
            self._send()

    def _send(self):
        self.send(self)
        self.committed = self.copy()

    def tpc_finish(self, transaction):
        if self.send_on_vote is False:
            self._send()

    def tpc_abort(self, transaction):
        self.abort(transaction)

    def sortKey(self):
        return 'json_dm' + str(id(self))

    def savepoint(self):
        return self.savepoint_factory(self)
