import numpy as np
from aubio import source, tempo

import sys
from pathlib import Path

import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('TkAgg')


def get_file_bpm(path):
    """
    Calculate the beats per minute (bpm) of a given file.
    Returns 0 whenever the tempo cannot be accurately measured.
    path: path to the file
    """

    samplerate, win_s, hop_s = 44100, 1024, 512
    s = source(str(path), samplerate, hop_s)
    samplerate = s.samplerate

    o = tempo("specdiff", win_s, hop_s, samplerate)

    # List of beats, in samples
    beats = []
    # Total number of frames read
    total_frames = 0

    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = o.get_last_s()
            beats.append(this_beat)
            # if o.get_confidence() > .2 and len(beats) > 2.:
            #    break
        total_frames += read
        if read < hop_s:
            break

    def beats_to_bpm(beats, name):
        # if enough beats are found, convert to periods then to bpm
        if len(beats) < 4:
            # Too few beats in order to provide a correct measurement
            return 0
        else:
            bpms = np.rint(60 / np.diff(beats))
            bpm_range = int(max(bpms) - min(bpms))

            if bpm_range == 0:
                # Clean sample file, every measured beat is correct, and thus
                # the algorithm gives a single bpm
                return bpms[0]
            else:
                # hist = np.histogram(bpms, bpm_range)

                # DEBUG: draws the histogram of all beats spacings
                plt.hist(bpms, bpm_range)
                plt.title(f"""\
                    {name}
                    Histogram of {len(bpms)} possible tempos\
                """)
                plt.show()

                # TODO: Make clever use of the histogram to determine
                # whether it can reveal the tempo of the sound file

                # The median is a placeholder for now
                return np.median(bpms)

    return beats_to_bpm(beats, path.name)


if __name__ == "__main__":

    files = []

    if len(sys.argv) > 1:
        # Use this to test a specific file
        file_name = Path(sys.argv[1])
        files = [file_name]
    else:
        # Without any arguments, it will test every
        # file in the subdirectory `tempo_tests`
        files = [
            file
            for file in Path('tempo_tests').iterdir()
            if file.is_file()
        ]

    for file_name in files:
        print(f"Testing {file_name}")
        tempo_found = get_file_bpm(file_name)
        print(f"tempo found = {tempo_found}\n")
