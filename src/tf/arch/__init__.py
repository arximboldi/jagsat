#
# This file is copyright Tribeflame Oy, 2009.
#
"""
You can ignore this package.
"""
import sys
if sys.platform.startswith("linux"):
    from tf.arch.linux import *
elif sys.platform.startswith("win"):
    from tf.arch.win32 import *
