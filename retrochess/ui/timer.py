from pygame.surface import Surface

from ui.config import Config

class TimerViewer():
    def __init__(self, surface:Surface) -> None:
        self.__surface = surface
    
    @property
    def surface(self):
        return self.__surface
    
    def update(self):
        self.surface.fill(Config.color.LIGHT)