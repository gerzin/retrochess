from pygame.color import Color
from pathlib import Path

class Config:
    class Color:
        LIGHT = Color(168, 133, 50)
        DARK = Color(183, 87, 13)
        HIGHLIGHT = Color(179, 154, 75)
        SELECTION = Color(255, 51, 0)
        LAST_MOVE = Color(255, 51, 100)
        TEXT_COLOR = Color(0,0,0)
    class Assets:
        ASSETS = Path(__file__).parent / "assets"
        PIECES = Path(__file__).parent / "assets" / "piecesets"
        FONTS  = Path(__file__).parent / "assets" / "fonts"

    assets = Assets()
    color = Color()
    SPACING = 10