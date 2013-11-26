from functools import wraps
import contextlib
import json
import pytest
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


@pytest.fixture
def sink():
    outlist = []
    sink = appender(outlist)
    return sink, outlist


def makeone(sender):
    from zmqtxn.datamanager import JSONDataManager
    dm = JSONDataManager(sender)
    return dm


@contextlib.contextmanager
def joined_txn(*dms):
    with transaction.manager as txn:
        [txn.join(dm) for dm in dms]
        yield txn


def test_jsondm(sink):
    appender, out = sink
    dm = makeone(appender.send)

    with joined_txn(dm):
        dm['entry_one'] = 1
        dm['entry_two'] = dict(hello='world')

    assert len(out) == 1
    results = json.loads(out[0])
    assert 'entry_one' in results


def test_failed_txn(sink):
    appender, out = sink
    dm = makeone(appender.send)

    with joined_txn(dm) as txn:
        dm['entry_one'] = 1
        dm['entry_two'] = dict(hello='world')
        txn.abort()

    assert out == []


def test_broken_sender_2_dm(sink):
    appender, out = sink


    def broken(data):
        import pdb;pdb.set_trace()
        raise Exception('Kaboom')

    dm2 = makeone(broken)
    dm = makeone(appender.send)
    
    try:
        with joined_txn(dm, dm2) as txn:
            dm['entry_one'] = 1
            dm['entry_two'] = dict(hello='world')
    except Exception as e:
        assert out == []
