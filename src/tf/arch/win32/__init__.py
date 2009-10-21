#
# This file is copyright Tribeflame Oy, 2009.
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
