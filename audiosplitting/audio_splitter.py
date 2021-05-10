import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import math
import os


def audioToSlicedSpecto(input_file, output_stub):

    # Set some of the values we use for the Spectrogram
    n_fft = 2048
    n_mels = 256
    hop_length = 256  # This is basically the size of the window for averaging samples together
    
    y, sample_rate = librosa.load(input_file, sr=None)
    # Trim the silent edges from the file
    sound_array, _ = librosa.effects.trim(y)
    sound_array_median = np.median(sound_array)
    print('loaded file: ' + input_file)

    # sample rate is samples per second so the length of the array divided by the sample rate tells us the seconds in the total track
    track_length = math.floor(librosa.get_duration(sound_array, sr=sample_rate))
    chunk_length_sec = 5

    # determine how many chunks can fit into track and then make an array incrementing from 0 by 5 up to the total number of chunks
    time_steps = np.arange(0, track_length + 1, chunk_length_sec).tolist()

    # TODO we need to add 0 padding to the array to make the array divisiable by 5 seconds and add the new last 5 segment
    # if time_steps[-1] < track_length:
    #   time_steps.append(track_length)

    # time to the time steps array
    # make two lists out of all the time steps we care about
    # time steps = [0,5,7]
    # starts = [0,5]
    # stops = [5,7]
    start_times = time_steps[:-1]
    stop_times = time_steps[1:]
    start_samples = list(map(lambda x: x * sample_rate, start_times))
    stop_samples = list(map(lambda x: x * sample_rate, stop_times))

    plt.figure(figsize=(60.48, 15.60), edgecolor='black', facecolor='black')
    for i, (start, stop) in enumerate(zip(start_times, stop_times)):
        out_filename = ''
        # slice the original signal list
        audio = sound_array[start_samples[i]:stop_samples[i]]

        # chop ogg off the file name
        out_filename = ''.join((out_file_prepped, '_', str(start), '_', str(stop), '.png'))
        mel = librosa.feature.melspectrogram
        S = mel(audio, sr=sample_rate, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels,
                                           fmin=1600.0, fmax=11000)

        # amin represents the amplitude mininimum (related to DB) that is considered more than 0. The higher you make the number the more noise you remove
        # but you may actually start to remove the information you want.

        # ref represents the value of which you are standardzing all the values against. Possible choices are mean, median, max
        # We actually ended up using the median of the entire audio clip to rescale the audio values in each individual clip
        p_to_d = librosa.power_to_db
        S_DB = p_to_d(S, ref=sound_array_median, amin=0.0015)

        spshow = librosa.display.specshow
        spshow(S_DB, sr=sample_rate, hop_length=hop_length)

        # Remove the black color using the method here in the article and save to disk
        # https://www.delftstack.com/howto/matplotlib/hide-axis-borders-and-white-spaces-in-matplotlib/
        plt.savefig(out_filename, bbox_inches='tight', pad_inches=0)
        plt.close()


if __name__ == '__main__':
    # Input directory should be a single directory with every species in its own sub-directory and no directories below that
    input_directory = r'C:\Users\steve\data\six_species'

    # This script will make this directory
    output_directory = r'C:\Users\steve\data\six_species\_output'


    # get all the folders and files using os.walk
    # https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
    for root, dirs, files in os.walk(input_directory):
        # make all the output directories
        for name in dirs:
            output_path = os.path.join(output_directory, name)
            if not os.path.exists(output_path):
                os.makedirs(output_path)
        for name in files:
            out_file_prepped = os.path.join(output_directory, os.path.basename(root), os.path.splitext(name)[0])
            print()
            audioToSlicedSpecto(input_file=os.path.join(root, name), output_stub = out_file_prepped)

    print("Done")
