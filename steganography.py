"""
Encode file as image
"""

import numpy as np  # import numpy
import os  # os path calculations
from scipy import misc  # read and write images
import struct  # binary conversion

buff_size = 1024  # buffer size
file_type = ".png"  # image type (need lossless compression)
int_size = 4  # size of integer in bytes


def decode():
    """
    Decode image
    :return: None
    """
    filename = input("Enter the image: ")  # get filename
    image = np.reshape(misc.imread(filename), [-1])  # get flattened image
    byte_file_size = bytearray([image[i] for i in range(int_size)])  # create byte array
    file_size = struct.unpack("i", byte_file_size)[0]  # get file size
    file_end_position = file_size + int_size  # get end of file in image.
    out_filename = os.path.splitext(filename)[0]  # trim extension
    with open(out_filename, "wb") as f:  # open result
        position = int_size  # position in file
        while position < file_end_position:  # loop till eof
            if position + buff_size < file_end_position:  # if can read full buffer
                buff = bytearray([image[i] for i in range(position, position + buff_size)])  # read buffer
                if buff:  # if read to buffer
                    f.write(buff)  # write buffer
                position += buff_size  # increment position
            else:  # read to max
                buff = bytearray([image[i] for i in range(position, file_end_position - position)])  # read buffer
                if buff:  # if read to buffer
                    f.write(buff)  # write buffer
                    position += len(buff)  # increment position
                else:  # if nothing read to final buffer
                    break  # end decoding


def encode():
    """
    Encode image
    :return: None
    """
    filename = input("Enter the filename: ")  # get filename
    file_size = os.path.getsize(filename)  # get byte size of file
    length = int(np.ceil((file_size + int_size)**0.5))  # get square root for length
    image = np.array([[0 for _ in range(length)] for _ in range(length)], np.uint8)  # create image

    # Write file size
    b_file_size = struct.pack("i", file_size)  # convert file size to bytes
    for i in range(int_size):
        image[0][i] = b_file_size[i]  # write file size

    # Write file
    with open(filename, "rb") as f:  # open file
        position = int_size  # position in image. Start after writing file size
        while True:  # till eof
            buff = f.read(buff_size)  # read buff
            if buff:  # if could read
                for b in buff:  # cycle through bytes
                    curr_length = int(position / length)  # get length
                    curr_width = position % length  # get width
                    image[curr_length][curr_width] = b  # write byte
                    position += 1  # increment position
            else:  # if can't read
                break  # done reading

    # Write image
    misc.imsave(filename + file_type, image)  # save image

    # Validate file
    while True:
        result = input("Validate (y/n)? ").lower()  # should validate
        if result == "y":  # should validate
            new_image = misc.imread(filename + file_type)  # get saved image
            size = len(new_image) * len(new_image[0])  # get size
            n_correct = 0  # number correct
            for i in range(len(new_image)):
                for j in range(len(new_image[0])):
                    if image[i][j] == new_image[i][j]:
                        n_correct += 1  # increment number correct
            print("{0}% correct of {1}".format(n_correct / size * 100, size))  # write validation
        elif result == "n":  # should not validate
            break  # stop looping


def main():
    """
    Main loop of program
    :return: None
    """
    is_exit = False  # should exit program
    print_help()  # write help

    # Enter main loop
    while not is_exit:  # while running
        command = input("Enter a command: ").lower()  # get command
        if command == "exit":
            is_exit = True  # exit program
        elif command == "encode":
            encode()  # run encode
        elif command == "decode":
            decode()  # run decode


def print_help():
    """
    Print help information
    :return: None
    """
    print("Type 'decode' to decode an image file.")  # write decode
    print("Type 'encode' to encode a file to image.")  # write encode
    print("Type 'exit' to exit the program.")  # write exit


if __name__ == "__main__":
    main()  # run main
