import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf


if __name__ == '__main__':
    directory = 'train_short_audio/bkcchi/'
    filename = 'XC121068.ogg'
    output_dir = directory + 'output/'
    y, sample_rate = librosa.load(directory + filename, sr=None)
    #Trim the silent edges from the file
    sound_array, _ = librosa.effects.trim(y)
    print('loaded file')

    # TODO for now put this here while exploring but them move into the loop
    n_fft = 2048
    n_mels = 256
    hop_length = 512

    plt.figure(figsize=(40.48,15.60), edgecolor='black', facecolor='black')
    plt.set_cmap('gray')
    
    S = librosa.feature.melspectrogram(sound_array, sr=sample_rate, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels, fmin=1600.0, fmax=11000)
    S_DB = librosa.power_to_db(S, ref=np.max)                                                               
    librosa.display.specshow(S_DB, sr=sample_rate, hop_length=hop_length)
    #plt.colorbar(format='%+2.0f dB')
    plt.show()



    #sample rate is samples per second so the length of the array divided by the sample rate tells us the seconds in the total track
    
    track_length = round(len(sound_array)/sample_rate)
    chunk_length_sec = 5
    samples_per_chunk = sample_rate *chunk_length_sec

    #generate two arrays of start and stop points in sound_array indices
    time_steps = np.arange(0, track_length +1, chunk_length_sec).tolist()
    if time_steps[-1] < track_length:
        time_steps.append(track_length)

    # make two lists out of all the time steps we care about
    # time steps = [0,5,7]
    # starts = [0,5]
    # stops = [5,7]
    start_times = time_steps[:-1]
    stop_times = time_steps[1:]

    start_samples = list(map(lambda x: x * samples_per_chunk, start_times))
    stop_samples = list(map(lambda x: x * samples_per_chunk, stop_times))


    for i, (start, stop) in enumerate(zip(start_times, stop_times)):
        out_filename = ''
        #slice the original signal list
        audio = sound_array[start_samples[i]:stop_samples[i]]

        #chop ogg off the file name
        out_filename = filename[:-4] + '_' + str(start) + '_' + str(stop) + '.png'

        #write out the sliced array at the original sample rate

        final_out_filename = output_dir + out_filename

        # todo image writing goes here
        # Remove the black color using the method here
        # https://www.delftstack.com/howto/matplotlib/hide-axis-borders-and-white-spaces-in-matplotlib/

        #try:
       #    sf.write(final_out_filename, audio, samplerate=sample_rate)
        #finally:
        #    print(final_out_filename)

        #with sf.SoundFile(final_out_filename, mode='x', samplerate=sample_rate, channels=1) as chunk_sound_file:
        #     chunk_sound_file.write( data=audio)
