from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import shutil

__all__ = ['install_all', 'install', 'install_dir', 'install_file']


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
            install(os.path.join(srcdir, filename),
                    objdir, quiet, exception_ok)
        except:
            except_filenames.append(filename)
    if except_filenames:
        if not quiet:
            print("[!]Failed to update software %s" %
                  (','.join(except_filenames)))
        if not exception_ok:
            raise Exception("[!]Failed to update software %s" %
                            (','.join(except_filenames)))


def install(src, objdir, quiet=False, exception_ok=False):
    """
    Update or install software to a specific directory by comparing timestamps.

    :param src: the path of the software.
    :param objdir: the directory where the software is installed.
    :param quiet: flag whether to print the installation info quietly. default: False.
    :param exception_ok: flag whether to ignore the raised exception. default: False.

    >>>install('test.exe', 'bin/')
    """
    if os.path.isfile(src):
        install_file(src, objdir, quiet=quiet, exception_ok=exception_ok)
    elif os.path.isdir(src):
        install_dir(src, objdir, quiet=quiet, exception_ok=exception_ok)
    else:
        if not exception_ok:
            raise Exception("[!]%s doesn't exist" % src)


def install_dir(src, objdir, quiet=False, exception_ok=False):
    """
    Update or install a directory to a specific directory by comparing timestamps.

    :param src: the path of the directory.
    :param objdir: the directory where the directory is installed.
    :param quiet: flag whether to print the installation info quietly. default: False.
    :param exception_ok: flag whether to ignore the raised exception. default: False.

    >>>install('test/', 'bin/')
    """
    src = os.path.abspath(src)
    if not os.path.isdir(src):
        if not exception_ok:
            raise Exception('[!]%s is not a directory' % src)
        return

    _, dirname = os.path.split(src)

    objdir = os.path.join(objdir, dirname)
    os.makedirs(objdir, exist_ok=True)

    for name in os.listdir(src):
        path = os.path.join(src, name)
        if os.path.isfile(path):
            install_file(path, objdir, quiet=quiet, exception_ok=exception_ok)
        else:
            install_dir(path, objdir, quiet=quiet, exception_ok=exception_ok)


def install_file(src, objdir, quiet=False, exception_ok=False):
    """
    Update or install a file to a specific directory by comparing timestamps.

    :param src: the path of the file.
    :param objdir: the directory where the file is installed.
    :param quiet: flag whether to print the installation info quietly. default: False.
    :param exception_ok: flag whether to ignore the raised exception. default: False.

    >>>install('test.exe', 'test.txt')
    """
    src = os.path.abspath(src)
    if not os.path.isfile(src):
        if not exception_ok:
            raise Exception('[!]%s is not a file' % src)
        return

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
            print("[+]Updating %s" % src)

        try:
            shutil.copy(src, objdir)
        except:
            if not quiet:
                print("[!]Failed to update %s" % src)
            if not exception_ok:
                raise

        if not quiet:
            print("[-]Successfully update %s" % src)
    else:
        print("[*]Software %s does not need to be updated" % src)
