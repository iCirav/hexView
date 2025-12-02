with open("output.bin", "wb") as file_obj:
    output_string = "The quick brown fox jumped over the dog."
    encoded_bytes = output_string.encode('utf-8')

    # Pad with 0xFF until the total length is 1024 bytes
    padded_bytes = encoded_bytes.ljust(1024, bytes([255]))

    #print(padded_bytes)
    file_obj.write(padded_bytes)

    
