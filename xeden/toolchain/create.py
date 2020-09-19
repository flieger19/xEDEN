"""
Documentation
"""

import sys
import os
import shutil

DEFAULT_TOOL = "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/"
XEDEN_TOOL = os.path.expanduser('~') + "/Library/Developer/Toolchains/X-EDEN.xctoolchain/"
CURRENT_DIR = os.path.abspath(os.getcwd())


def directory_maker(path):
    """
    Makes specified directory
    :param path: directory to make
    """
    try:
        os.makedirs(path)
    except OSError:
        print("Creation of the directory %s failed" % path)


def directory_iterator(source, target):
    """
    Iterates through a directory and symlinks all containing files in a target director with the same structure
    :param source: Directory to iterate through
    :param target: Directory to symlink files to
    """
    for file in os.listdir(source):
        filename = os.fsdecode(file)
        path_source = source + bytes("/", 'utf-8') + file
        path_target = target + bytes("/", 'utf-8') + file
        if os.path.isdir(path_source):
            directory_maker(os.fsdecode(path_target))
            directory_iterator(os.fsencode(path_source), os.fsencode(path_target))
        elif os.path.isfile(path_source):
            try:
                os.symlink(path_source, path_target)
            except:
                print("Symlink Error")
        elif os.access(path_source, os.X_OK):
            try:
                os.symlink(path_source, path_target)
            except:
                print("Symlink Error")
        elif os.path.islink(path_source):
            continue
        else:
            print("Special file ", path_source)


def create():
    """
    Creates X-EDEN Xcode toolchain
    """
    # gen tool chain
    usr_directory = "usr/"
    directory_maker(XEDEN_TOOL + usr_directory)

    # copy plist file
    info_file = "/Info.plist"
    source = CURRENT_DIR + info_file
    target = XEDEN_TOOL + info_file
    try:
        shutil.copyfile(source, target)
    except IOError as error:
        print("Unable to copy file. %s" % error)
    except:
        print("Unexpected error:", sys.exc_info())

    # symlink
    directory_iterator(os.fsencode(DEFAULT_TOOL + usr_directory), os.fsencode(XEDEN_TOOL + usr_directory))

    # symlink lld
    source_lld = "/usr/local/opt/arm-none-eabi-llvm/bin/lld"
    target_lld = "usr/bin/ld.lld"
    try:
        os.symlink(source_lld, XEDEN_TOOL + target_lld)
    except:
        print("Symlink Error")
