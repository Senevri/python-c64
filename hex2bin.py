#!/bin/python3
import sys

# import and set up logging
import logging


logger = None
def setup_logging():
    # Create a logger
    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)

    # Add the stream handler to the logger
    logger.addHandler(stream_handler)

def hex_to_binary(hex_string):
    # Remove spaces and convert to bytes
    hex_bytes = bytes.fromhex(hex_string.replace(" ", "").lower())
    return hex_bytes

def calculate_length_and_pointer(line, current_pointer=0x0800):
    # Calculate the length of the BASIC code and the pointer to the next BASIC line
    total_length = len(hex_to_binary(line))
    pointer = current_pointer + total_length + 2 # Add 2 bytes for the length and pointer
    return total_length, pointer

def main(input_file, output_file, include_length_and_pointer=False):
    try:
        # Read hex data from the input file
        with open(input_file, 'r') as f:
            lines = [line.split('#')[0].strip() for line in f.readlines()]
            hex_data = ''.join(lines)

        logger.info("Hex data: %s", hex_data)
        # Convert hex to binary
        binary_data = hex_to_binary(hex_data)

        # Calculate total length and pointer to the next line
        total_length, pointer = calculate_length_and_pointer(lines[0])


        # If requested, prepend the length and pointer to the next BASIC line
        if include_length_and_pointer:
            header = total_length.to_bytes(2, 'little') + pointer.to_bytes(2, 'little')
            binary_data = header + binary_data

        # Write binary data to the output file
        with open(output_file, 'wb') as f:
            f.write(binary_data)

        print(f"Conversion successful. Binary data saved to {output_file}")

    except FileNotFoundError:
        print("Error: Input file not found.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Check if both input and output file paths are provided
    if len(sys.argv) < 3:
        print("Usage: python script_name.py input_file output_file")
    else:
        # Get input and output file paths from command-line arguments
        input_file_path = sys.argv[1]
        output_file_path = sys.argv[2]
        setup_logging()

        # Check if the optional length flag is provided
        include_length_and_pointer = len(sys.argv) == 4 and sys.argv[3] in ['-l', '--length']

        main(input_file_path, output_file_path, include_length_and_pointer)
