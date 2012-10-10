
try:
    import cPickle as pickle
except ImportError:
    import pickle

from functools import wraps
from datetime import timedelta

from django.core.cache import cache
from django.utils import timezone

from .exceptions import ServeStaleContentException


class cached(object):
    def __init__(self, expire=5 * 60, hard_expire=24 * 60 * 60, default=None):
        self.expire = expire
        self.hard_expire = hard_expire
        self.default = default

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            """wrapper function"""

            key_prefix = 'cacheutils:'
            hash_ = hash(pickle.dumps([args, kwargs]))

            #TODO: is hash(fn) the same across threads, processes and servers?
            key = '{0}:{1}:{2}'.format(key_prefix, hash(fn), hash_)

            data = cache.get(key)

            if data:
                data = pickle.loads(data)
                if data[0] > timezone.now():
                    return data[1]

            try:
                out = fn(*args, **kwargs)
            except ServeStaleContentException:
                # serve stale content, if any
                if data:
                    return data[1]

                return self.default

            cache.set(
                key,
                pickle.dumps(
                    (timezone.now() + timedelta(seconds=self.expire), out)
                ),
                self.hard_expire
            )

            return out

        return wrapper
