import tkinter as tk


class MainUI:

    def __init__(self, root, title):
        self.root = root
        self.frame = tk.Frame(self.root)
        self.root.title(title)
        self.sli_exposure = tk.Scale(self.frame, from_=100, to=20000,
                                     orient=tk.HORIZONTAL,
                                     command=self.update_exposure,
                                     length=400)
        self.sli_exposure.set(5000)
        self.sli_exposure.pack()

        self.sli_gain = tk.Scale(self.frame, from_=0, to=600,
                                 orient=tk.HORIZONTAL,
                                 command=self.update_gain,
                                 length=400)
        self.sli_gain.set(150)
        self.sli_gain.pack()

    def update_exposure(val):
        print('Updating exposure to %s' % val)
        camera.set_control_value(asi.ASI_EXPOSURE, int(val))


    def update_gain(val):
        print('Updating gain to %s' % val)
        camera.set_control_value(asi.ASI_GAIN, int(val))
