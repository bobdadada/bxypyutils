# -*- coding: utf-8 -*-

import os
import zipfile

def compress(src, dst, compression=0, allowZip64=True, compresslevel=None):
    """
    Compress files or folders

    :param src: source file or folder
    :param dst: destination, path of the compressed file
    :param compression: see zipfile.ZipFile
    :param allowZip64: see zipfile.ZipFile
    :param compresslevel: see zipfile.ZipFile
    """
    
    # path
    src = os.path.abspath(src)
    arcname = os.path.basename(src)
    dst = os.path.abspath(dst)

    if src in dst:
        raise ValueError('The path of the compressed file cannot be in the source folder.')

    dst_dir = os.path.dirname(dst)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # Remove ZIP file
    if os.path.basename(dst) in os.listdir(os.path.dirname(dst)):
        os.remove(dst)

    if os.path.isdir(src):
        with zipfile.ZipFile(dst, 'w', compression=compression, allowZip64=allowZip64, \
                                compresslevel=compresslevel) as fd:
            for dirpath, _, filenames in os.walk(src):
                for filename in filenames:
                    fd.write(os.path.join(dirpath, filename),
                                os.path.join(dirpath.replace(src, arcname), filename))
    elif os.path.isfile(src):
        with zipfile.ZipFile(dst, 'w', compression=compression, allowZip64=allowZip64, \
                                compresslevel=compresslevel) as fd:
            fd.write(src, arcname=arcname)
    else:
        raise FileNotFoundError('Source file %s not exists'%src)
