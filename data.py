from pydantic import BaseModel


class ScreenCoordinates(BaseModel):
    x: float
    y: float


class MouseButtons(BaseModel):
    left: bool
    middle: bool
    right: bool
    others: bool

    def any(self) -> bool:
        return self.left or self.right or self.middle or self.others


class MouseData(BaseModel):
    position: ScreenCoordinates
    buttons: MouseButtons


class ScrollData(BaseModel):
    absolute: ScreenCoordinates
    relative: ScreenCoordinates


class KeyboardData(BaseModel):
    alpha: bool
    numeric: bool
    symbol: bool
    function: bool

    def any(self):
        return self.alpha or self.symbol or self.numeric or self.function


class CollectedData(BaseModel):
    mouse: MouseData
    scroll: ScrollData
    keyboard: KeyboardData
