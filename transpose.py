import os
from pathlib import Path
import mido

# 🔧 Change this to your MIDI folder path
MIDI_FOLDER = Path("/Users/macbookair/massive/midis")

def transpose_midi(input_path: Path, semitone_shift: int, output_path: Path):
    mid = mido.MidiFile(input_path)
    out = mido.MidiFile()

    for track in mid.tracks:
        new_track = mido.MidiTrack()
        for msg in track:
            if msg.type in ("note_on", "note_off"):
                new_note = msg.note + semitone_shift
                new_note = max(0, min(127, new_note))  # clamp valid range
                new_track.append(msg.copy(note=new_note))
            else:
                new_track.append(msg)
        out.tracks.append(new_track)

    out.save(output_path)


def main():
    if not MIDI_FOLDER.is_dir():
        print(f"❌ {MIDI_FOLDER} is not a valid folder")
        return

    for midi_file in MIDI_FOLDER.glob("*.mid"):
        up_path = midi_file.with_name(midi_file.stem + "_up.mid")
        down_path = midi_file.with_name(midi_file.stem + "_down.mid")
        transpose_midi(midi_file, 1, up_path)
        transpose_midi(midi_file, -1, down_path)
        print(f"✅ {midi_file.name} → {up_path.name}, {down_path.name}")


if __name__ == "__main__":
    main()
