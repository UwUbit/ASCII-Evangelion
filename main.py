import time
import os
import fpstimer
from playsound import playsound
from pynput.keyboard import Key, Controller
from ImageConverting import get_list
from CreateDirectoryWithFrames import get_frames_from_video


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

    # Getting the list of frames
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frames")
    list_with_frame_names = sorted(
        [(filename, int(filename[:-4])) for filename in os.listdir(directory) if filename.endswith(".jpg")],
        key=lambda x: x[1]
    )

    # Getting terminal size and calculating output frames
    columns, rows = os.get_terminal_size()
    print("Calculating output...")
    out_list = [get_list(os.path.join(directory, f[0]), columns, rows) for f in list_with_frame_names]
    print("Done!")
    time.sleep(1)

    if confirm_sound == 'Y':
        audio_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lost_soul_audio.mp3")
        playsound(audio_file, False)

    # Displaying frames with FPS control
    fps = 90
    timer = fpstimer.FPSTimer(fps)

    # Initializing an empty previous frame for comparison
    previous_frame = [''] * rows

    # Loop through each frame
    for current_frame in out_list:
        # Split current frame into lines
        current_frame_lines = current_frame.splitlines()

        # Compare and print only the lines that have changed
        for i, (old_line, new_line) in enumerate(zip(previous_frame, current_frame_lines)):
            if old_line != new_line:
                # Move cursor to the correct line and print the new line
                print(f"\033[{i+1}0H{new_line}")

        # Update the previous frame with the current frame's data
        previous_frame = current_frame_lines.copy()

        # Control FPS
        timer.sleep()


if __name__ == "__main__":
    main()
