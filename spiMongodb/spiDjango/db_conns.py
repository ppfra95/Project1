import redis
from mongoengine import connect, get_connection
from pymongo import MongoClient

try:
    from django.conf import settings
except ImportError:
    settings = None


class MongoEngineConn(object):
    aux = {
        'host': getattr(settings, 'MONGO_HOST', ''),
        'port': getattr(settings, 'MONGO_PORT', ''),
        'username': getattr(settings, 'MONGO_USER', ''),
        'password': getattr(settings, 'MONGO_SECRET', ''),
        'replicaset': getattr(settings, 'MONGO_REPLICA_SET', ''),
        'authentication_source': 'admin'
    }

    def __new__(cls, *args, **kwargs):
        try:
            return get_connection('default')
        except Exception:
            return connect(db=getattr(settings, 'MONGO_DB', ''), alias='default', **cls.aux)


class MongoConn(object):
    _conn = None

    def __new__(cls, *args, **kwargs):
        new_conn = kwargs.pop('new', False)
        readPreference = kwargs.pop('readPreference', 'secondaryPreferred')
        w = kwargs.pop('w', 3)
        if not cls._conn or new_conn:
            conn = MongoClient(
                username=getattr(settings, 'MONGO_USER', ''),
                password=getattr(settings, 'MONGO_SECRET', ''),
                host=getattr(settings, 'MONGO_HOST', ''),
                replicaset=getattr(settings, 'MONGO_REPLICA_SET', ''),
                readPreference=readPreference, w=w,
            )
            MONGO_DB = getattr(settings, 'MONGO_DB', '')
            _conn = getattr(conn, MONGO_DB)
            if new_conn:
                return _conn
            cls._conn = _conn
        return cls._conn


class MongoAvlConn(object):
    _conn = None

    def __new__(cls, *args, **kwargs):
        new_conn = kwargs.pop('new', False)
        readPreference = kwargs.pop('readPreference', 'secondaryPreferred')
        w = kwargs.pop('w', 3)
        if not cls._conn or new_conn:
            conn = MongoClient(
                username=getattr(settings, 'MONGO_WS_USER', ''),
                password=getattr(settings, 'MONGO_WS_SECRET', ''),
                host=getattr(settings, 'MONGO_HOST', ''),
                replicaset=getattr(settings, 'MONGO_REPLICA_SET', ''),
                readPreference=readPreference, w=w,
            )
            MONGO_DB = getattr(settings, 'MONGO_WS_DB', 'encontrack')
            _conn = getattr(conn, MONGO_DB)
            if new_conn:
                return _conn
            cls._conn = _conn
        return cls._conn


class MongoLogConn(object):
    _conn = None

    def __new__(cls, *args, **kwargs):
        new_conn = kwargs.pop('new', False)
        readPreference = kwargs.pop('readPreference', 'secondaryPreferred')
        w = kwargs.pop('w', 3)
        if not cls._conn or new_conn:
            conn = MongoClient(
                username=getattr(settings, 'MONGO_LOG_USER', ''),
                password=getattr(settings, 'MONGO_LOG_SECRET', ''),
                host=getattr(settings, 'MONGO_HOST', ''),
                replicaset=getattr(settings, 'MONGO_REPLICA_SET', ''),
                readPreference=readPreference, w=w,
            )
            MONGO_DB = getattr(settings, 'MONGO_LOG_DB', 'encontrack')
            _conn = getattr(conn, MONGO_DB)
            if new_conn:
                return _conn
            cls._conn = _conn
        return cls._conn


class RedisConn(object):
    _conn = None

    def __new__(cls, *args, **kwargs):
        if not cls._conn:
            cls._conn = redis.StrictRedis(
                host=getattr(settings, 'REDIS_HOST', 'localhost'),
                port=getattr(settings, 'REDIS_PORT', 6379),
                db=getattr(settings, 'REDIS_DATABASE', 0))
        return cls._conn
