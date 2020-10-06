"""
Steganography with wav file
"""

# Imports
import numpy as np
import os
import soundfile as sf  # Read/Write sound
import time  # write time

buffer_size = 1024  # buffer size
byte_max = 256  # max value of byte
message_ext = ".wav"  # encoding file type
noise_scale = 1  # amplitude of noise
progress_every = 10  # write progress every x %
sample_rate = 44100  # sampling rate


def compare():
    """
    Compare bytes of file
    :return: None
    """
    filename_1 = input("Enter the first filename: ")  # get filename
    filename_2 = input("Enter the second filename: ")  # get filename
    n_correct = 0  # number of correct
    file_1_size = os.path.getsize(filename_1)  # get file 1 size
    with open(filename_1, "rb") as file_1:  # open file 1
        with open(filename_2, "rb") as file_2:  # open file 2
            while True:  # till eof
                buffer_1 = file_1.read(buffer_size)  # read buffer
                buffer_2 = file_2.read(buffer_size)  # read buffer
                if buffer_1 and buffer_2:  # if read values
                    int_buff_1 = [b for b in buffer_1]  # get integer values
                    int_buff_2 = [b for b in buffer_2]  # get integer values
                    n_correct += np.sum(np.equal(int_buff_1, int_buff_2))  # increment number of identical values
                else:  # no buffer
                    break  # end comparison
    # Write results
    print("{0} is {1}% or {2} bytes different from {3}".format(filename_2,
                                                               100 - n_correct / file_1_size * 100,
                                                               file_1_size - n_correct,
                                                               filename_1))  # write results


def decode():
    """
    Decode message
    :return: None
    """
    filename = input("Enter the file to decode: ")  # get filename
    out_filename = os.path.splitext(filename)[0]  # get file without extension
    sound, sample = sf.read(filename)  # read sound file
    len_sound = len(sound)  # get length of sound file
    with open(out_filename, "wb") as f:  # open output file
        position = 0  # position in file
        prev_percent_progress = 0  # position of last writing progress
        prev_time = time.time()  # get time
        while position < len_sound:  # cycle through sound file
            sound_data = sound[position:position+buffer_size]  # read buffer
            scaled_data = np.floor(np.arccos(sound_data / noise_scale) * byte_max / np.pi).astype(np.uint8)  # scale
            buffer = bytearray(scaled_data)  # conversion to byte array
            if buffer:  # if read data
                f.write(buffer)  # write buffer

                # Update position
                percent_progress = position / len_sound * 100  # get progress as %
                if percent_progress - prev_percent_progress >= progress_every:  # if need to write progress
                    print("{0}% complete in {1} seconds.".format(percent_progress,
                                                                 time.time() - prev_time))  # write progress
                    prev_percent_progress = percent_progress  # update previous position
                position += len(sound_data)  # increment position
            else:  # if no data
                break  # end file
    print("Done decoding {0} to {1}".format(filename, out_filename))  # write done


def encode():
    """
    Encode message
    :return: None
    """
    filename = input("Enter the file to encode: ")  # get filename
    file_size = os.path.getsize(filename)  # get file size
    out_filename = filename + message_ext  # get output filename
    sound = []  # declare sound
    position = 0  # position in file
    prev_percent_progress = 0  # previous position for writing progress
    prev_time = time.time()  # get current time

    with open(filename, "rb") as f:  # open file
        n_correct = 0  # number of lossless conversions

        while True:  # till eof
            buffer = f.read(buffer_size)  # read buffer
            if buffer:  # if can read
                float_buffer = np.array([float(b) for b in buffer], dtype=np.float64)  # write buffer to floats
                sound_data = np.cos(float_buffer / byte_max * np.pi) * noise_scale  # scale and calculate sine

                # Validate
                valid_data = np.round(np.arccos(sound_data / noise_scale) * byte_max /
                                      np.pi).astype(np.uint8)  # validate
                n_correct += np.sum(np.equal(float_buffer, valid_data))  # validate data
                sound.extend(sound_data)  # extend sound file

                # update position
                percent_progress = position / file_size * 100  # convert progress to percent
                if percent_progress - prev_percent_progress >= progress_every:  # if need to write progress
                    print("{0}% done in {1} seconds.".format(percent_progress,
                                                             time.time() - prev_time))  # write progress
                    prev_percent_progress = percent_progress  # update previous position
                position += len(buffer)  # increment position
            else:  # if can't read
                break  # end encoding

    print("{0}% of {1} lossless conversion.".format(n_correct / file_size * 100, file_size))  # write results
    sf.write(out_filename, sound, sample_rate)  # write sound file


def main():
    """
    Main script program
    :return: None
    """
    is_exit = False  # should exit
    print_help()  # print help
    while not is_exit:  # while should not exit
        command = input("Enter a command: ").lower()  # get command
        if command == "exit":
            is_exit = True  # should exit
        elif command == "compare":  # if compare
            compare()  # call compare
        elif command == "decode":  # if decode
            decode()  # call decode
        elif command == "encode":  # if encode
            encode()  # call encode


def print_help():
    """
    Write help to console
    :return: None
    """
    print("Type 'Compare' to compare bytes.")  # write compare
    print("Type 'Decode' to decode a message.")  # write decode
    print("Type 'Encode' to write a message.")  # write encode
    print("Type 'Exit' to close.")  # write exit


if __name__ == "__main__":  # if running script
    main()  # call main
