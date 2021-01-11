import subprocess


class Stream:

    def __init__(self, url, width, height):
        self.url = url
        self.stream_cmd = ['ffmpeg',
                           '-f', 'lavfi',
                           '-i',
                           'anullsrc=channel_layout=stereo:sample_rate=44100',
                           '-f', 'rawvideo',
                           '-pix_fmt', 'gray',
                           '-s', '{}x{}'.format(width, height),
                           '-use_wallclock_as_timestamps', '1',
                           '-i', '-',
                           '-b:v', '2600k',
                           '-preset', 'ultrafast',
                           '-f', 'flv',
                           '-s', 'hd1080',
                           url]
        self.p = subprocess.Popen(self.stream_cmd, stdin=subprocess.PIPE)
        self.stream_pipe = self.p.stdin
        if __debug__:
            print("Stream PID = " + str(self.p.pid))

    def finish(self):
        if __debug__:
            print("Closing stream")
        self.stream_pipe.close()
        self.p.wait()
        if self.p.returncode != 0:
            raise subprocess.CalledProcessError(self.p.returncode,
                                                self.stream_cmd)
