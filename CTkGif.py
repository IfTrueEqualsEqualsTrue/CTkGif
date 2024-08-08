from PIL import Image
import customtkinter as ctk


class CTkGif(ctk.CTkLabel):

    def __init__(self, master: any, file_path: str, loop: bool = True, acceleration: float = 1, repeat: int = 1,
                 size: tuple = None, stop_command: callable = None, **kwargs) -> None:
        """ CustomTkinter widget to display and manage a GIF file (as a succession of frames)
        :param master: the parent widget
        :param file_path: the path to the .gif file
        :param loop: if the gif should start again when its end is reached
        :param acceleration: factor of speed to play the gif animation
        :param repeat: the number of times the gif should be played if not looped
        :param size: the size in px of the frames in the gif
        :param stop_command: to call at the end of the gif
        :param kwargs: params for the parent CTkLabel if needed """
        super().__init__(master, **kwargs)

        if acceleration <= 0:
            raise ValueError('Acceleration must be strictly positive')

        self.repeat = repeat
        self.loop = loop
        self.stop_command = stop_command
        self.gif = Image.open(file_path)
        self.n_frame = self.gif.n_frames
        self.frame_duration = self.gif.info['duration'] * 1 / acceleration
        if size is not None:
            self.size = size
        else:
            self.size = self.gif.size
        self.configure(text='', image=ctk.CTkImage(self.gif, size=self.size))

        self.repeat_count = 0
        self.frame_index = 0
        self.is_playing = False
        self.force_stop = False

    def update(self):
        """ Manage the next gif frame to display"""
        if self.frame_index < self.n_frame:  # Before the last gif frame

            if not self.force_stop:

                self.gif.seek(self.frame_index)  # next frame
                self.configure(image=ctk.CTkImage(self.gif, size=self.size))  # update displayed image
                self.frame_index += 1  # Indexation
                self.after(int(self.frame_duration), self.update)  # Programmation prochaine frame

            else:
                self.force_stop = False
                self.call_stop_command()

        else:  # Last gif frame reached

            self.frame_index = 0  # Next frame to be displayed is the first one
            self.repeat_count += 1
            if self.is_playing and (self.repeat_count < self.repeat or self.loop):
                self.after(self.frame_duration, self.update)
            else:
                self.is_playing = False
                self.call_stop_command()

    def start(self):
        """ Launch the frame cycle"""
        if not self.is_playing:
            self.repeat_count = 0
            self.is_playing = True
            self.after(int(self.frame_duration), self.update)

    def stop(self, forced=False):
        """ Stops instantaneously the frame cycle if forced, else ends the current cycle"""
        if self.is_playing:
            self.is_playing = False
            self.force_stop = forced

    def toggle(self, forced=False):
        """ toggle the cycle state, aka stops it if cycling, or starts it if stopped."""
        if self.is_playing:
            self.stop(forced=forced)
        else:
            self.start()

    def call_stop_command(self):
        if self.stop_command is not None:
            self.stop_command()
