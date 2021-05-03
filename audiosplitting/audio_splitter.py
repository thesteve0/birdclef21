import librosa
import numpy as np
import soundfile as sf


if __name__ == '__main__':
    directory = 'train_short_audio/bkcchi/'
    filename = 'XC121068.ogg'
    output_dir = directory + 'output/'

    
    sound_array, sample_rate = librosa.load(directory + filename, sr=None)
    print('loaded file')
    o_env = librosa.onset.onset_strength(sound_array, sr=sample_rate)
    #o_env = librosa.onset.onset_strength(sound_array, sr=sample_rate, feature=librosa.feature.chroma_cqt)
    onset_times = librosa.onset.onset_detect(onset_envelope=o_env, sr=sample_rate, backtrack=True, units='time')

    onset_samples = list(librosa.time_to_samples(onset_times, sr=sample_rate))
    onset_samples = np.concatenate(onset_samples, len(sound_array))
    starts = onset_samples[0:-1]
    stops = onset_samples[1:]
    for i, (start, stop) in enumerate(zip(starts, stops)):
        out_filename = ''
        audio = sound_array[start:stop]
        out_filename = filename[:-4] + '_' + str(start) + '_' + str(stop) + '.ogg'
        sf.write(output_dir + out_filename, audio, sample_rate)
