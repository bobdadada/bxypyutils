from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import shutil

__all__ = ['install_all', 'install']

def install_all(srcdir, objdir, quiet=False, exception_ok=False):
    """
    Update or install all softwares in a source directory to a specific
    directory by comparing timestamps.

    :param srcdir: source directory where all the softwares are located.
    :param objdir: the directory where the software is installed.
    :param quiet: flag whether to print the installation info quietly. default: False.
    :param exception_ok: flag whether to ignore the raised exception. default: False.

    >>>install('dist/', 'bin/')
    """
    except_filenames = []
    for filename in os.listdir(srcdir):
        try:
            install(os.path.join(srcdir, filename), objdir, quiet, exception_ok)
        except:
            except_filenames.append(filename)
    if except_filenames:
        raise Exception("[!]Failed to update software %s"%(','.join(except_filenames)))


def install(src, objdir, quiet=False, exception_ok=False):
    """
    Update or install software to a specific directory by comparing timestamps.

    :param src: the path of the software.
    :param objdir: the directory where the software is installed.
    :param quiet: flag whether to print the installation info quietly. default: False.
    :param exception_ok: flag whether to ignore the raised exception. default: False.
    
    >>>install('test.exe', 'bin/')
    """
    src = os.path.abspath(src)
    _, filename = os.path.split(src)

    update_flag = False

    if filename in os.listdir(objdir):
        # 时间戳比较
        pst = os.stat(os.path.join(objdir, filename))
        cst = os.stat(src)
        if pst.st_mtime < cst.st_mtime:
            update_flag = True
    else:
        update_flag = True

    if update_flag:
        if not quiet:
            print("[+]Updating software %s"%filename)

        try:
            shutil.copy(src, objdir)
        except:
            if not quiet:
                print("[!]Failed to update software %s"%filename)
            if not exception_ok:
                raise

        if not quiet:
            print("[-]Successfully updated software %s"%filename)
    else:
        print("[*]Software %s does not need to be updated"%filename)
