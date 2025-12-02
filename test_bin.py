with open("output.bin", "rb") as file_obj:
    #Chunk size should be 1, to read 1 byte at a time
    chunk_size = 1

    #Do you want 8bit or 16 bit?  16 is default
    bytes_per_line = 16

    #Variable Initializaition
    hex_line = ""
    ascii_line = ""
    line_number = 1
    
    while True:
        #Use a for loop to iterate through the file in either 8 or 16
        # bit mode.
        for i in range(0,bytes_per_line):

            #Read out the next byte
            #Then build the variable for the hex line to be printed
            chunk = file_obj.read(chunk_size)
            hex_byte = chunk.hex()
            hex_line = hex_line + hex_byte + " "
            
            #Decode the byte for the ascii line to be printed
            decoded_byte = chunk.decode('latin-1')
            ascii_line = ascii_line + decoded_byte

        # Break out of the while loop if we read null data
        if not chunk:
            break

        #Print the hex and ascii
        #Example:
        #
        # 8-Bit Mode
        #41 41 41 41 41 41 41 41    AAAAAAAA
        #
        # 16-Bit Mode
        #41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41   AAAAAAAAAAAAAAAA

        print(f"{line_number}:\t {hex_line}\t{ascii_line}")
        line_number = line_number + 1
        hex_line = ""
        ascii_line = ""

