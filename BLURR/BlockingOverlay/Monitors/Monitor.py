from dataclasses import dataclass
import typing as T


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
