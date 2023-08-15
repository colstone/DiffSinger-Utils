import os
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
from scipy import interpolate

def freq_to_midi(freq):
    # Convert frequency to MIDI pitch
    return 12 * np.log2(freq / 440) + 69

def plot_f0_curve(wav_path):
    # Load the audio file
    y, sr = librosa.load(wav_path)

    # Extract the fundamental frequency (f0) using librosa's pitch tracking
    f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))

    # Create a time array for plotting
    times = librosa.times_like(f0)

    # Perform one-dimensional linear interpolation to fill unvoiced regions
    f0_interp = np.interp(times, times[voiced_flag], f0[voiced_flag])

    # Convert frequencies to MIDI pitch
    midi_pitch = freq_to_midi(f0_interp)

    # Compute loudness curve using librosa's loudness function
    loudness = librosa.amplitude_to_db(librosa.feature.rms(y=y, frame_length=2048, hop_length=512), ref=np.max)

    # Plot the f0 curve and loudness curve
    plt.figure(figsize=(12, 6), dpi=300)  # Increase dpi for higher resolution

    # Plot voice part (blue color)
    plt.plot(times, midi_pitch, label='MIDI Pitch (Voiced)', color='b')

    # Add gray horizontal lines at each integer MIDI pitch value
    midi_integers = np.arange(np.ceil(midi_pitch.min()), np.floor(midi_pitch.max()) + 1)
    for midi_integer in midi_integers:
        plt.axhline(y=midi_integer, color='gray', linestyle='--', linewidth=0.5)

    plt.xlabel('Time (s)')
    plt.ylabel('MIDI Pitch')
    plt.title('MIDI Pitch and Loudness Curve')
    plt.legend(loc='best')

    # Create a twin y-axis for loudness
    ax2 = plt.twinx()
    ax2.plot(times, loudness[0], label='Loudness', color='magenta')
    ax2.set_ylabel('Loudness (dB)')
    ax2.legend(loc='upper right')

    plt.tight_layout()

    # Save the plot to the same directory as the input wav file
    output_filename = os.path.splitext(os.path.basename(wav_path))[0] + '_midi_pitch_loudness_curve.png'
    output_path = os.path.join(os.path.dirname(wav_path), output_filename)
    plt.savefig(output_path)
    plt.close()

    print(f"MIDI pitch and loudness curve plot saved at: {output_path}")

if __name__ == "__main__":
    wav_path = input("Please enter the path of the WAV file: ")
    plot_f0_curve(wav_path)
