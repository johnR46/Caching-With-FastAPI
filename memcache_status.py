import re
import telnetlib
from typing import Optional


class MemcachedStats:
    _client = None
    _key_regex = re.compile(r'ITEM (.*) \[(.*); (.*)\]')
    _slab_regex = re.compile(r'STAT items:(.*):number')
    _stat_regex = re.compile(r"STAT (.*) (.*)\r")

    def __init__(self, host: Optional[str] = 'localhost', port: Optional[int] = 11211, timeout=None):
        self._host = host
        self._port = port
        self._timeout = timeout

    @property
    def client(self):
        if self._client is None:
            self._client = telnetlib.Telnet(self._host, self._port, self._timeout)
        return self._client

    def command(self, cmd):
        """ Write a command to telnet and return the response """
        self.client.write(("%s\n" % cmd).encode('ascii'))
        return self.client.read_until(b'END').decode('ascii')

    def key_details(self, sort=True, limit=100):
        """ Return a list of tuples containing keys and details """
        cmd = 'stats cachedump %s %s'
        keys = [key for idx in self.slab_ids()
                for key in self._key_regex.findall(self.command(cmd % (idx, limit)))]
        if sort:
            return sorted(keys)
        else:
            return keys

    def keys(self, sort=True, limit=100):
        """ Return a list of keys in use """
        return [key[0] for key in self.key_details(sort=sort, limit=limit)]

    def slab_ids(self):
        """ Return a list of slab ids in use """
        return self._slab_regex.findall(self.command('stats items'))

    def stats(self):
        """ Return a dict containing memcached stats """
        return dict(self._stat_regex.findall(self.command('stats')))
