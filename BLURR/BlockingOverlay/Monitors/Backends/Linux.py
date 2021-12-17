from BlockingOverlay.Monitors.Monitor import Monitor
import ctypes.util
import typing as T
import ctypes


def load_library(name: str) -> T.Any:
    path = ctypes.util.find_library(name)
    if not path:
        raise RuntimeError("Could not load " + name)
    return ctypes.cdll.LoadLibrary(path)


def enumerate_monitors() -> T.Iterable[Monitor]:

    class XineramaScreenInfo(ctypes.Structure):
        _fields_ = [
            ("screen_number", ctypes.c_int),
            ("x", ctypes.c_short),
            ("y", ctypes.c_short),
            ("width", ctypes.c_short),
            ("height", ctypes.c_short),
        ]

    xlib = load_library("X11")
    xlib.XOpenDisplay.argtypes = [ctypes.c_char_p]
    xlib.XOpenDisplay.restype = ctypes.POINTER(ctypes.c_void_p)
    xlib.XFree.argtypes = [ctypes.c_void_p]
    xlib.XFree.restype = None

    xinerama = load_library("Xinerama")

    display = xlib.XOpenDisplay(b"")
    if not display:
        raise RuntimeError("Could not open display")

    try:
        if not xinerama.XineramaIsActive(display):
            raise RuntimeError("Xinerama is not active")

        number = ctypes.c_int()
        xinerama.XineramaQueryScreens.restype = ctypes.POINTER(
            XineramaScreenInfo
        )
        infos = xinerama.XineramaQueryScreens(display, ctypes.byref(number))
        infos = ctypes.cast(
            infos, ctypes.POINTER(XineramaScreenInfo * number.value)
        ).contents

        for info in infos:
            yield Monitor(
                x=info.x, y=info.y, width=info.width, height=info.height, scaling=1
            )

        xlib.XFree(infos)

    finally:
        xlib.XCloseDisplay.restype = ctypes.POINTER(ctypes.c_void_p)
        xlib.XCloseDisplay(display)
