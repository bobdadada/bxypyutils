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
    failed_softwares = []
    for name in os.listdir(srcdir):
        try:
            install(os.path.join(srcdir, name),
                    objdir, quiet, exception_ok=False)
        except Exception as e:
            if not quiet:
                print(e)
            failed_softwares.append(name)
    if failed_softwares:
        if not quiet:
            print("[!]Failed to update software %s" %
                  (','.join(failed_softwares)))
        if not exception_ok:
            raise Exception("[!]Failed to update software %s" %
                            (','.join(failed_softwares)))


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


def install_dir(srcdir, objdir, quiet=False, exception_ok=False):
    """
    Update or install a directory to a specific directory by comparing timestamps.

    :param srcdir: the path of the directory.
    :param objdir: the directory where the directory is installed.
    :param quiet: flag whether to print the installation info quietly. default: False.
    :param exception_ok: flag whether to ignore the raised exception. default: False.

    >>>install('test/', 'bin/')
    """
    srcdir = os.path.abspath(srcdir)
    objdir = os.path.abspath(objdir)

    if not os.path.isdir(srcdir):
        if not exception_ok:
            raise Exception('[!]%s is not a directory' % srcdir)
        return

    if srcdir == objdir:
        if not exception_ok:
            raise Exception(
                '[!]The source path %s conflicts with the destination path' % srcdir)
        return

    topath = os.path.join(objdir, os.path.split(srcdir)[1])
    os.makedirs(topath, exist_ok=True)

    if not quiet:
        print("[+]Updating %s" % srcdir)

    failed_filenames = []

    for dirpath, dirnames, filenames in os.walk(srcdir):

        for filename in filenames:
            path = os.path.join(dirpath, filename)
            try:
                install_file(path, dirpath.replace(srcdir, topath),
                             quiet=True, exception_ok=False)
            except:
                failed_filenames.append(path)

        # ingore the destination diretory to prevent endless recursion
        remove_dirname = None
        for dirname in dirnames:
            path = os.path.join(dirpath, dirname)
            if path == objdir:
                remove_dirname = dirname
                break
        if remove_dirname:
            dirnames.remove(remove_dirname)

    if failed_filenames:
        if not quiet:
            print("[!]For %s, fail to update files %s" %
                  (srcdir, ',\n\t'.join(failed_filenames)))

        if not exception_ok:
            raise Exception("[!]For %s, failed to update files %s" %
                            (srcdir, ',\n\t'.join(failed_filenames)))
    else:
        if not quiet:
            print("[-]Successfully update %s" % srcdir)


def install_file(srcfile, objdir, quiet=False, exception_ok=False):
    """
    Update or install a file to a specific directory by comparing timestamps.

    :param srcfile: the path of the file.
    :param objdir: the directory where the file is installed.
    :param quiet: flag whether to print the installation info quietly. default: False.
    :param exception_ok: flag whether to ignore the raised exception. default: False.

    >>>install('test.exe', 'test.txt')
    """
    srcfile = os.path.abspath(srcfile)
    objdir = os.path.abspath(objdir)

    if not os.path.isfile(srcfile):
        if not exception_ok:
            raise Exception('[!]%s is not a file' % srcfile)
        return

    os.makedirs(objdir, exist_ok=True)

    _, filename = os.path.split(srcfile)

    update_flag = False

    if filename in os.listdir(objdir):
        # 时间戳比较
        pst = os.stat(os.path.join(objdir, filename))
        cst = os.stat(srcfile)
        if pst.st_mtime < cst.st_mtime:
            update_flag = True
    else:
        update_flag = True

    if update_flag:
        if not quiet:
            print("[+]Updating %s" % srcfile)

        try:
            shutil.copy(srcfile, objdir)
        except:
            if not quiet:
                print("[!]Fail to update %s" % srcfile)
            if not exception_ok:
                raise

        if not quiet:
            print("[-]Successfully update %s" % srcfile)
    else:
        if not quiet:
            print("[*]Software %s does not need to be updated" % srcfile)
