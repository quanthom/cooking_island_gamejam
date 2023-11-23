#
# Play some music in the game
#
import pygame
import os
from time import sleep

try:
    from pydub import AudioSegment
    from pydub.effects import speedup
except ModuleNotFoundError:
    print ("Error try \npip install pydub")

class Music():
    def __init__(self, mp3_file=None):
        if mp3_file is None:
            self._music_file = os.path.join("assets", "music", "Island_Cooking_Songs_LOOP2.mp3")
        else:
            self._music_file = mp3_file
        
        print("mp3:{}".format(self._music_file))        
        self.mixer = pygame.mixer.init()
        pygame.mixer.music.load(self._music_file)

    def load(self, mp3_file=None):
        pygame.mixer.music.load(self._music_file)
        if mp3_file is None:
            pygame.mixer.music.load(self._music_file)
        else:
            pygame.mixer.music.load(mp3_file)
            self._music_file = mp3_file

    def play(self,loop=False):
        pygame.mixer.music.play(-1 if loop else 0)

    def pause(self):
        pygame.mixer.music.play()

    def unpause(self):
        pygame.mixer.pause()
    
    def faster(self):
        # Add some clever bit here but not quite working yet @todo
        try:
            audio = AudioSegment.from_mp3(self._music_file)
            new_file = speedup(audio,1.5,150)
            new_file.export("file_150.mp3", format="mp3")
            self.pause()
            self.load()
            self.play()
        except FileNotFoundError:
            print ("Fix me please")
            pass

    def slower(self):
        pass
