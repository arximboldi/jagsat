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

# Code from StackOverflow
# http://stackoverflow.com/users/9493/brian
import code
import traceback
import signal


def __debug(sig, frame):
    """
    Interrupt running process, and provide a python prompt for
    interactive debugging.
    """
    d={'_frame': frame}         # Allow access to frame object.
    d.update(frame.f_globals)  # Unless shadowed by global
    d.update(frame.f_locals)

    i = code.InteractiveConsole(d)
    message = "tf: Signal recieved: entering python shell.\nTraceback:\n"
    message += ''.join(traceback.format_stack(frame))
    i.interact(message)


def create_debug_port():
    signal.signal(signal.SIGUSR1, __debug)  # Register handler

######################################################################


def _get_values():
    line = open("/proc/stat").readline()
    s = line.split(" ")
    user = float(int(s[2]))
    nice = float(int(s[3]))
    sys = float(int(s[4]))
    idle = float(int(s[5]))
    iowait = float(int(s[6]))
    irq = float(int(s[7]))
    softirq = float(int(s[8]))

    u = user + nice + sys # + iowait + irq + softirq
    return u, idle

previous_values = list(_get_values())


def get_cpu_usage():
    global previous_values
    used, idle = _get_values()
    u = used - previous_values[0]
    i = idle - previous_values[1]
    previous_values[0] = used
    previous_values[1] = idle

    i = max(i, 1)
    usage = u / (u + i) * 100.0
    return usage
