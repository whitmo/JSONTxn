from functools import wraps
import json
import transaction

def coro(func):
    @wraps(func)
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        cr.next()
        return cr
    return start

@coro
def appender(outlist):
    while True:
        payload = (yield)
        outlist.append(json.dumps(payload))
    


def makeone(sender):
    from zmqtxn.datamanager import JSONDataManager
    t = transaction.get()
    dm = JSONDataManager(sender)
    t.join(dm)
    return t, dm

def test_jsondm():
    outlist = []
    sender = appender(outlist).send
    txn, dm = makeone(sender)
    dm['entry_one'] = 1
    dm['entry_two'] = dict(hello='world')
    txn.commit()
    assert len(outlist) == 1
    results = json.loads(outlist[0])
    assert 'entry_one' in results





