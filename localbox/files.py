"""
Encoding functions specific to localbox
"""
from datetime import datetime
from os.path import join
from os.path import split
from os.path import abspath
from os.path import relpath
from os.path import isdir
from os.path import islink
from os import chdir
from os import getcwd
from os import stat
from os import walk
from os import readlink
from os import sep

from .config import ConfigSingleton


def get_filesystem_path(localbox_path, user):
    """
    Given a LocalBox path (e.g. '/file_name'), return the corresponding
    filesystem path (e.g. '/var/localbox/data/user/file_name')
    """
    bindpoint = ConfigSingleton().get('filesystem', 'bindpoint')
    filepath = join(bindpoint, user, localbox_path)
    return filepath


def stat_reader(filesystem_path, user):
    """
    Return metadata for the given (filesystem) path based on information
    provided by the stat system call.
    """
    bindpoint = ConfigSingleton().get('filesystem', 'bindpoint')
    bindpath = abspath(join(bindpoint, user))
    if bindpath == abspath(filesystem_path):
        title = 'Home'
    else:
        title = [item for item in split(filesystem_path) if item != ''][-1]
    localboxpath = '/' + join(relpath(filesystem_path,
                                      bindpath)).replace(sep, '/')
    if localboxpath == '/.':
        localboxpath = '/'
    statstruct = stat(filesystem_path)
    statdict = {
        'title': title,
        'is_dir': isdir(filesystem_path),
        'modified_at': datetime.fromtimestamp(statstruct.st_mtime).isoformat(),
        'is_share': SymlinkCache().exists(abspath(filesystem_path)),
        'is_shared': islink(abspath(filesystem_path)),
        'has_keys': True,
        'path': localboxpath,
    }
    if statdict['is_dir']:
        statdict['icon'] = 'Folder'
    else:
        statdict['icon'] = 'File'
    if isdir(filesystem_path):
        statdict['hash'] = 'TODO'
    return statdict


class SymlinkCache(object):
    """
    Singleton keeping track of all symlinks (shares)
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SymlinkCache, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def remove(self, absolute_filename):
        """
        removes links to and from filename
        """
        if absolute_filename in self.cache.keys():
            self.cache.pop(absolute_filename)
        for key, value in self.cache.iteritems():
            if absolute_filename in value:
                newvalue = value.remove(absolute_filename)
                self.cache[key] = newvalue

    def exists(self, absolute_file_name):
        """
        Check whether absolute_file_name is in the cache, and thus a
        destination of a symlink and thus a 'share' folder
        """
        return absolute_file_name in self.cache

    def get(self, path):
        return self.cache[path]

    def __init__(self):
        if not hasattr(self, 'cache'):
            print("initialising SymlinkCache")
            self.cache = {}
            self.build_cache()
            print("initialised SymlinkCache")

    def build_cache(self):
        """
        Build the reverse symlink cache by walking through the filesystem and
        finding all symlinks.
        """
        working_directory = getcwd()
        bindpoint = ConfigSingleton().get('filesystem', 'bindpoint')
        for dirname, directories, files in walk(bindpoint):
            for entry in directories + files:
                linkpath = abspath(join(dirname, entry))
                if islink(linkpath):
                    chdir(dirname)
                    destpath = abspath(readlink(linkpath))
                    if destpath in self.cache:
                        self.cache[destpath].append(linkpath)
                    else:
                        self.cache[destpath] = [linkpath]
        chdir(working_directory)