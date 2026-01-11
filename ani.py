#!/usr/bin/env python3
import subprocess
import sys
import os

def load_episode(anime):
    """Load last watched episode from cache"""
    file_path = os.path.expanduser(f"~/.cache/ani-progress_{anime.replace(' ', '_')}.txt")
    if not os.path.exists(file_path):
        return 1
    try:
        with open(file_path, "r") as f:
            ep = int(f.read().strip())
            return max(ep, 1)
    except Exception:
        return 1

def save_episode(anime, episode):
    """Save next episode to cache"""
    file_path = os.path.expanduser(f"~/.cache/ani-progress_{anime.replace(' ', '_')}.txt")
    try:
        with open(file_path, "w") as f:
            f.write(str(episode + 1))
    except Exception:
        pass

def main():
    if len(sys.argv) < 2:
        print('Usage: python ani.py "Anime Name" [start_episode]')
        return

    anime = sys.argv[1]
    episode = int(sys.argv[2]) if len(sys.argv) >= 3 else load_episode(anime)
    if episode < 1:
        episode = 1

    print(f"▶ Auto-playing {anime} from episode {episode}")

    while True:
        # Command for ani-cli with non-interactive options
        cmd = [
            "ani-cli",
            anime,
            "-e", str(episode),
            "-q", "720p",             # preferred quality (change if needed)
            "--exit-after-play"       # prevents interactive menu
        ]
        try:
            # Run ani-cli and inherit stdout/stderr
            result = subprocess.run(cmd)

            if result.returncode != 0:
                print(f"❌ ani-cli failed for episode {episode}. Stopping autoplay.")
                break

            save_episode(anime, episode)
            episode += 1

        except KeyboardInterrupt:
            print("\n⏹ Autoplay interrupted by user.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            break

    print(f"🎬 Finished auto-play for {anime}")

if __name__ == "__main__":
    main()
