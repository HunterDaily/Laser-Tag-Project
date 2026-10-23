import random
from pathlib import Path # Path is used to navigate our confusing file system.
import pygame # We'll use pygame's built in music functions.

# Music folder:
music_folder = Path(__file__).parent / "photon-main" / "photon_tracks"

def start_track(): # Randomly picks a track to play from the music folder.
    tracks = [
        path for path in music_folder.iterdir() if path.suffix == ".mp3" # All music files should be mp3s!
    ]

    track = random.choice(tracks) # Picking our randomly selected track.
    pygame.mixer.music.load(str(track))
    pygame.mixer.music.play() # Load then play the track file.

    # print(f"Now playing: {track.name}") # Print the name of the track to the console.
    return track

def wait_for_track_finished(): # Checks for track completion.
    clock = pygame.time.Clock()
    while pygame.mixer.music.get_busy():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit # Double checking to make sure we properly exit the program.
        clock.tick(30) # Wait for 30 ticks before checking again!