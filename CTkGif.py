from PIL import Image
import customtkinter as ctk


class CTkGif(ctk.CTkLabel):
    """ Affichage d'un gif """

    def __init__(self, master: any, path, loop=True, acceleration=1, repeat=1, **kwargs):
        super().__init__(master, **kwargs)
        if acceleration <= 0:
            raise ValueError('Acceleration must be strictly positive')
        self.master = master  #  master
        self.repeat = repeat  # Nombre repeat max
        self.configure(text='')  # Retire texte base
        self.path = path  # Chemin gif
        self.count = 0  # Nombre d'animations réalisés
        self.loop = loop  # tourne on a l'infini ?
        self.acceleration = acceleration  # facteur de ralentissement
        self.index = 0  # Frame affichée
        self.is_playing = False  # état de l'affichage
        self.gif = Image.open(path)  # Image ouverte
        self.n_frame = self.gif.n_frames  # Nombres de frame de l'animation
        self.frame_duration = self.gif.info['duration'] * 1/self.acceleration  # temps d'une frame
        self.force_stop = False

    def update(self):  # Update l'affichage du gid
        if self.index < self.n_frame:  # Si on est pas au bout de l'animation
            if not self.force_stop:  # Si on est pas forcé de s'arrêter
                self.gif.seek(self.index)  # Frame suivante
                self.configure(image=ctk.CTkImage(self.gif, size=(300, 100)))  # Affichage
                self.index += 1  # Indexation
                self.after(int(self.frame_duration), self.update)  # Programmation prochaine frame
            else:
                self.force_stop = False  # On passe en off
        else:  # Si on est au bout
            self.index = 0  # On revient au début
            self.count += 1  # On incrémente le compteur
            if self.is_playing and (self.count < self.repeat or self.loop):  # pas d'arrêt et on recommence
                self.after(int(self.frame_duration), self.update)  # Programmation prochaine frame
            else:
                self.is_playing = False  # On passe en off

    def start(self):
        """ débute l'animation si arrêtée"""
        if not self.is_playing:
            self.count = 0
            self.is_playing = True
            self.after(int(self.frame_duration), self.update)

    def stop(self, forced=False):
        """arrête l'animation brusquement si forcé, à sa fin sinon"""
        if self.is_playing:
            self.is_playing = False
            self.force_stop = forced

    def toggle(self, forced=False):
        """ change le status de la lecture"""
        if self.is_playing:
            self.stop(forced=forced)
        else:
            self.start()


