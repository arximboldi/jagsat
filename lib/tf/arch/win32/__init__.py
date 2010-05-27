#
#  Copyright (C) 2009 TribleFlame Oy
#  
#  This file is part of TF.
#  
#  TF is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  
#  TF is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

def create_debug_port():
    """
    N/A This functionality does not exist on Windows.
    """
    pass

_win32_cpu_usage = None


def get_cpu_usage():
    """
    N/A. Unfortunately, this implementation is way too slow
    Probably should run it in a thread or something.
    """
    return 0

    global _win32_cpu_usage
    if _win32_cpu_usage is None:
        from tf.arch.win32 import win32_cpu_usage
        _win32_cpu_usage = win32_cpu_usage.QueryCPUUsage()
    return _win32_cpu_usage.getCPUUsage()
