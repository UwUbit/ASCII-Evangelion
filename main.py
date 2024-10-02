import time
import os
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

    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frames")
    list_with_frame_names = sorted(
        [(filename, int(filename[:-4])) for filename in os.listdir(directory) if filename.endswith(".jpg")],
        key=lambda x: x[1]
    )

    columns, rows = os.get_terminal_size()
    print("Calculating output...")
    out_list = [get_list(os.path.join(directory, f[0]), columns, rows) for f in list_with_frame_names]
    print("Done!")
    time.sleep(1)

    if confirm_sound == 'Y':
        audio_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nge_op.mp3")
        playsound(audio_file, False)

    start_time = time.time()

    previous_frame = [''] * rows

    for frame_index, current_frame in enumerate(out_list):
        frame_start_time = time.time()

        current_frame_lines = current_frame.splitlines()

        for i, (old_line, new_line) in enumerate(zip(previous_frame, current_frame_lines)):
            if old_line != new_line:
                print(f"\033[{i+1}0H{new_line}")

        previous_frame = current_frame_lines.copy()

        expected_frame_duration = (frame_index + 1) / 30.0
        elapsed_time = time.time() - start_time

        if elapsed_time < expected_frame_duration:
            time.sleep(expected_frame_duration - elapsed_time)


if __name__ == "__main__":
    main()