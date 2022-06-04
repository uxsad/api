from typing import Optional, Tuple

from pydantic import BaseModel
import data
import math


class Vector(BaseModel):
    total: float
    x: float
    y: float


class MouseData(data.MouseData):
    speed: Vector
    acceleration: Vector


class ComputedData(data.CollectedData):
    mouse: MouseData
    slope: float

    def to_dict(self):
        return {
            # "id": self.id,
            "user_id": self.user_id,
            "timestamp": self.timestamp,
            "url": self.url,
            "url.category": None,
            # Mouse
            "mouse.position.x": self.mouse.position.x,
            "mouse.position.y": self.mouse.position.y,
            "mouse.clicks": self.mouse.buttons.any(),
            "mouse.clicks.left": self.mouse.buttons.left,
            "mouse.clicks.right": self.mouse.buttons.right,
            "mouse.clicks.middle": self.mouse.buttons.middle,
            "mouse.clicks.others": self.mouse.buttons.others,
            "mouse.speed": self.mouse.speed.total,
            "mouse.speed.x": self.mouse.speed.x,
            "mouse.speed.y": self.mouse.speed.y,
            "mouse.acceleration": self.mouse.acceleration.total,
            "mouse.acceleration.x": self.mouse.acceleration.x,
            "mouse.acceleration.y": self.mouse.acceleration.y,
            "trajectory.slope": self.slope,
            # Scroll
            "scroll.absolute.x": self.scroll.absolute.x,
            "scroll.absolute.y": self.scroll.absolute.y,
            "scroll.relative.x": self.scroll.relative.x,
            "scroll.relative.y": self.scroll.relative.y,
            # Keyboard
            "keyboard": self.keyboard.any,
            "keyboard.alpha": self.keyboard.alpha,
            "keyboard.numeric": self.keyboard.numeric,
            "keyboard.function": self.keyboard.function,
            "keyboard.symbol": self.keyboard.symbol,
        }


def pythagorean(x: float, y: float) -> float:
    return math.sqrt((x ** 2 + y ** 2))


def compute_speed(first: data.CollectedData, second: data.CollectedData) -> \
        Tuple[Optional[ComputedData], Optional[ComputedData]]:
    def convert(obj: data.CollectedData) -> ComputedData:
        zero_vec = Vector(total=0, x=0, y=0)
        d: dict = obj.dict()
        d['mouse'].update({'speed': zero_vec, 'acceleration': zero_vec})
        return ComputedData(**d, slope=0)

    if first is None:
        return None, convert(second)
    if second is None:
        return convert(first), None

    f, s = convert(first), convert(second)

    deltaT = s.timestamp - f.timestamp
    speedx = (s.mouse.position.x - f.mouse.position.x) / deltaT
    speedy = (s.mouse.position.y - f.mouse.position.y) / deltaT
    speed = Vector(x=speedx, y=speedy, total=pythagorean(speedx, speedy))
    s.mouse.speed = speed
    s.slope = speedy / speedx if speedx != 0 else math.inf if speedy != 0 else None
    return f, s


def compute_acceleration(first: ComputedData, second: ComputedData) -> \
        Tuple[Optional[ComputedData], Optional[ComputedData]]:
    if first is None:
        return None, second
    if second is None:
        return first, None

    deltaT = second.timestamp - first.timestamp
    accx = (second.mouse.speed.x - first.mouse.speed.x) / deltaT
    accy = (second.mouse.speed.y - first.mouse.speed.y) / deltaT
    acc = Vector(x=accx, y=accy, total=pythagorean(accx, accy))
    second.mouse.acceleration = acc
    return first, second


def compute_features(first: data.CollectedData, second: data.CollectedData) -> \
        Tuple[Optional[ComputedData], Optional[ComputedData]]:
    return compute_acceleration(*compute_speed(first, second))
