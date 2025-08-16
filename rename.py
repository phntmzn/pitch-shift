import librosa
import soundfile as sf
from pathlib import Path

# Folder containing WAV files
input_folder = Path("/Volumes/bR 870 QVO/WAVs")
output_folder = Path.home() / "Desktop" / "output_wavs_new"
output_folder.mkdir(exist_ok=True)

# Process each WAV file in folder
for wav_file in input_folder.glob("*.wav"):
    print(f"Processing: {wav_file.name}")
    
    # Load audio
    y, sr = librosa.load(wav_file, sr=None)
    
    # Pitch up/down 100 cents
    y_up = librosa.effects.pitch_shift(y, sr=sr, n_steps=1.0)
    y_down = librosa.effects.pitch_shift(y, sr=sr, n_steps=-1.0)
    
    # Save
    up_path = output_folder / f"{wav_file.stem}_up100cents.wav"
    down_path = output_folder / f"{wav_file.stem}_down100cents.wav"
    
    sf.write(up_path, y_up, sr)
    sf.write(down_path, y_down, sr)

print("Done — all files processed.")
