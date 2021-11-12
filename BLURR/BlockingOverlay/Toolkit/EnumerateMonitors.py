import typing as T

import enum
import typing as T
from dataclasses import dataclass


@dataclass
class Monitor:
    """Stores the resolution and position of a monitor."""

    x: int
    y: int
    width: int
    height: int
    scaling: int
    width_mm: T.Optional[int] = None
    height_mm: T.Optional[int] = None
    name: T.Optional[str] = None

    def __repr__(self) -> str:
        return (
            f"Monitor("
            f"x={self.x}, y={self.y}, "
            f"width={self.width}, height={self.height}, "
            f"width_mm={self.width_mm}, height_mm={self.height_mm}, "
            f"name={self.name!r}, "
            f"scaling={self.scaling}"
            f")"
        )


def enumerate_monitors() -> T.Iterable[Monitor]:
    import ctypes
    import ctypes.wintypes

    CCHDEVICENAME = 32
    # gdi32.GetDeviceCaps keys for monitor size in mm
    HORZSIZE = 4
    VERTSIZE = 6
    HORZRES = 8
    DESKTOPHORZRES = 118

    MonitorEnumProc = ctypes.WINFUNCTYPE(
        ctypes.c_int,
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.POINTER(ctypes.wintypes.RECT),
        ctypes.c_double,
    )

    class MONITORINFOEXW(ctypes.Structure):
        _fields_ = [
            ("cbSize", ctypes.wintypes.DWORD),
            ("rcMonitor", ctypes.wintypes.RECT),
            ("rcWork", ctypes.wintypes.RECT),
            ("dwFlags", ctypes.wintypes.DWORD),
            ("szDevice", ctypes.wintypes.WCHAR * CCHDEVICENAME),
        ]

    monitors = []

    def callback(monitor: T.Any, dc: T.Any, rect: T.Any, data: T.Any) -> int:
        info = MONITORINFOEXW()
        info.cbSize = ctypes.sizeof(MONITORINFOEXW)
        if ctypes.windll.user32.GetMonitorInfoW(monitor, ctypes.byref(info)):
            name = info.szDevice
        else:
            name = None

        h_size = ctypes.windll.gdi32.GetDeviceCaps(dc, HORZSIZE)
        v_size = ctypes.windll.gdi32.GetDeviceCaps(dc, VERTSIZE)
        virtual = ctypes.windll.gdi32.GetDeviceCaps(dc, HORZRES)
        physical = ctypes.windll.gdi32.GetDeviceCaps(dc, DESKTOPHORZRES)
        if(physical == 0): \
            return 1
        scaling = 100 * virtual/physical
        rct = rect.contents
        monitors.append(
            Monitor(
                x=rct.left,
                y=rct.top,
                width=rct.right - rct.left,
                height=rct.bottom - rct.top,
                scaling=scaling,
                width_mm=h_size,
                height_mm=v_size,
                name=name,
            )
        )
        return 1


    # On Python 3.8.X GetDC randomly fails returning an invalid DC.
    # To workaround this request a number of DCs until a valid DC is returned.
    for retry in range(100):
        # Create a Device Context for the full virtual desktop.
        dc_full = ctypes.windll.user32.GetDC(None)
        if dc_full > 0:
            # Got a valid DC, break.
            break
        ctypes.windll.user32.ReleaseDC(dc_full)
    else:
        # Fallback to device context 0 that is the whole
        # desktop. This allows fetching resolutions
        # but monitor specific device contexts are not
        # passed to the callback which means that physical
        # sizes can't be read.
        dc_full = 0
    # Call EnumDisplayMonitors with the non-NULL DC
    # so that non-NULL DCs are passed onto the callback.
    # We want monitor specific DCs in the callback.
    ctypes.windll.user32.EnumDisplayMonitors(
        dc_full, None, MonitorEnumProc(callback), 0
    )
    ctypes.windll.user32.ReleaseDC(dc_full)

    yield from monitors