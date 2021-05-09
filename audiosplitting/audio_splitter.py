import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import math
import soundfile as sf


if __name__ == '__main__':
    #TODO
    # input_directory =
    # output_directory =


    # get all the folders and files using os.walk
    #https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python

    # make all the output directories

    # then the code below get's called for each file - might want to put the code below as a separate function in the program


    directory = 'train_short_audio/bkcchi/'
    filename = 'XC199366.ogg'
    output_dir = directory + 'output/'
    y, sample_rate = librosa.load(directory + filename, sr=None)
    # Trim the silent edges from the file
    sound_array, _ = librosa.effects.trim(y)
    sound_array_median = np.median(sound_array)
    print('loaded file')

    # sample rate is samples per second so the length of the array divided by the sample rate tells us the seconds in the total track
    track_length = math.floor(librosa.get_duration(sound_array, sr=sample_rate))
    chunk_length_sec = 5
    # samples_per_chunk = sample_rate * chunk_length_sec

    # determine how many chunks can fit into track and then make an array incrementing from 0 by 5 up to the total number of chunks
    time_steps = np.arange(0, track_length +1, chunk_length_sec).tolist()
    # if time_steps[-1] < track_length:
        #time_steps.append(track_length)
        #TODO we need to add 0 padding to the array to make the array divisiable by 5 seconds and add the new last 5 segment
        #time to the time steps array

    # make two lists out of all the time steps we care about
    # time steps = [0,5,7]
    # starts = [0,5]
    # stops = [5,7]
    start_times = time_steps[:-1]
    stop_times = time_steps[1:]

    start_samples = list(map(lambda x: x * sample_rate, start_times))
    stop_samples = list(map(lambda x: x * sample_rate, stop_times))

    n_fft = 2048
    n_mels = 256
    hop_length = 256  # This is basically the size of the window for averaging samples together

    plt.figure(figsize=(60.48,15.60), edgecolor='black', facecolor='black')


    for i, (start, stop) in enumerate(zip(start_times, stop_times)):
        out_filename = ''
        #slice the original signal list
        audio = sound_array[start_samples[i]:stop_samples[i]]

        #chop ogg off the file name
        out_filename = filename[:-4] + '_' + str(start) + '_' + str(stop) + '.png'

        #write out the sliced array at the original sample rate

        final_out_filename = output_dir + out_filename
        print('About to make: ' + final_out_filename)

        S = librosa.feature.melspectrogram(audio, sr=sample_rate, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels, fmin=1600.0, fmax=11000)

        # amin represents the amplitude mininimum (related to DB) that is considered more than 0. The higher you make the number the more noise you remove
        # but you may actually start to remove the information you want.


        # ref represents the value of which you are standardzing all the values against. Possible choices are mean, median, max
        # We actually ended up using the median of the entire audio clip to rescale the audio values in each individual clip
        S_DB = librosa.power_to_db(S, ref=sound_array_median, amin=0.0015)
        librosa.display.specshow(S_DB, sr=sample_rate, hop_length=hop_length)

        # Remove the black color using the method here in the article and save to disk
        # https://www.delftstack.com/howto/matplotlib/hide-axis-borders-and-white-spaces-in-matplotlib/
        plt.savefig(final_out_filename, bbox_inches='tight', pad_inches=0)
