
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

    def call(self, fn, args, kwargs, force=False):
        key_prefix = 'cacheutils:'
        args_hash = hash(pickle.dumps([args, kwargs]))
        #TODO: use a better hash for fn
        function_hash = hash(fn.__module__ + fn.__name__)

        key = '{0}:{1}:{2}'.format(key_prefix, function_hash, args_hash)

        if not force:
            data = cache.get(key)
        else:
            data = None

        if data:
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
            (timezone.now() + timedelta(seconds=self.expire), out),
            self.hard_expire
        )

        return out

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            """wrapper function"""

            return self.call(fn, args, kwargs)

        def force(*args, **kwargs):
            return self.call(fn, args, kwargs, force=True)

        wrapper.force = force
#        wrapper.fn = fn

        return wrapper
