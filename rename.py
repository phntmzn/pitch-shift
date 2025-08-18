import random
from pathlib import Path

# --- Name generation config ---
BASE_NAMES = [
    "2u", "midnight drive", "echoes", "neon skies", "slow burn",
    "haze", "fading lights", "static rain", "noir", "pulse",
]

ADJECTIVES = list(dict.fromkeys([
    "midnight", "neon", "hollow", "velvet", "crystal", "silver", "shadow",
    "golden", "deep", "phantom", "cold", "empty", "silent", "electric", "storm"
]))

NOUNS = list(dict.fromkeys([
    "drive", "echoes", "skies", "burn", "waves", "dreams", "hearts", "city",
    "rain", "horizons", "tides", "shadowplay", "dusk", "bloom", "loop"
]))


def dedup_preserve(seq):
    """Remove duplicates while preserving order."""
    return list(dict.fromkeys(seq))


def generate_combos(adjs, ns, needed, existing_set):
    """Generate up to 'needed' unique 'adj noun' combos not in existing_set."""
    out = []
    attempts = 0
    max_attempts = needed * 20  # safety cap
    while len(out) < needed and attempts < max_attempts:
        attempts += 1
        name = f"{random.choice(adjs)} {random.choice(ns)}"
        if name not in existing_set:
            existing_set.add(name)
            out.append(name)
    return out


def build_song_names(target_count):
    # Start with curated seeds
    names = dedup_preserve([s.strip().lower() for s in BASE_NAMES if s.strip()])
    existing = set(names)

    # Top up with generated combinations
    if len(names) < target_count:
        to_add = target_count - len(names)
        names.extend(generate_combos(ADJECTIVES, NOUNS, to_add, existing))

    return names


def rename_files(folder: Path, names, dry_run: bool = False, preview_count: int = 20):
    # Preview
    for name in names[:preview_count]:
        print(name)
    print(f"Generated {len(names)} unique names.")

    files = sorted([f for f in folder.iterdir() if f.is_file() and f.suffix.lower() == ".wav"])
    for file_path, songname in zip(files, names):
        ext = file_path.suffix
        new_name = f"zonedout - {songname} (prod. phntmzn bR){ext}"
        new_path = file_path.with_name(new_name)
        if dry_run:
            print(f"[dry-run] {file_path.name} → {new_name}")
        else:
            file_path.rename(new_path)
            print(f"{file_path.name} → {new_name}")
    print("Done" + (" (dry-run)." if dry_run else "."))


if __name__ == "__main__":
    folder = Path("/Users/macbookair/Desktop/output_wavs_new")

    if not folder.exists():
        raise SystemExit(f"Folder does not exist: {folder}")

    names = build_song_names(len([f for f in folder.iterdir() if f.is_file() and f.suffix.lower() == ".wav"]))
    rename_files(folder, names, dry_run=False, preview_count=20)
