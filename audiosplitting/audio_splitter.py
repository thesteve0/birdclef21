import librosa


if __name__ == '__main__':
    filename = 'train_short_audio/bkcchi/XC199366.ogg'
    sound_array, sample_rate = librosa.load(filename, sr=None)
    print('Done')
