import time
import os
import fpstimer
from playsound import playsound
from pynput.keyboard import Key, Controller
from ImageConverting import get_list
from CreateDirectoryWithFrames import get_frames_from_video


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    keyboard = Controller()
    confirm_full_screen = input("Play in full screen? Y/n: ")
    if confirm_full_screen == 'Y':
        keyboard.press(Key.f11)
        keyboard.release(Key.f11)

    confirm_frames = input("Create frames? Y/n: ")
    if confirm_frames == 'Y':
        get_frames_from_video()

    confirm_sound = input("Play with sound? Y/n: ")

    # Get list of frames
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frames")
    list_with_frame_names = sorted(
        [(filename, int(filename[:-4])) for filename in os.listdir(directory) if filename.endswith(".jpg")],
        key=lambda x: x[1]
    )

    # Get terminal size and calculate output frames
    columns, rows = os.get_terminal_size()
    print("Calculating output...")
    out_list = [get_list(os.path.join(directory, f[0]), columns, rows) for f in list_with_frame_names]
    print("Done!")
    time.sleep(1)

    if confirm_sound == 'Y':
        audio_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lost_soul_audio.mp3")
        playsound(audio_file, False)

    # Display frames with FPS control
    fps = 30
    timer = fpstimer.FPSTimer(fps)
    for frame in out_list:
        clear_console()  # Clear screen before displaying new frame
        print(frame, end='')  # Display current frame
        timer.sleep()


if __name__ == "__main__":
    main()
