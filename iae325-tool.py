import typing
import argparse

def sanatize(text: str) -> str:
    text = text.lower()
    return text

def caesar_encrypt(plaintext: str, key: int) -> str:
    plaintext = sanatize(plaintext)
    ciphertext: str = ""

    ASCII_RANGE = {"max": 122, "min": 97}

    # Iterate through plaintext
    for c in plaintext:
        # Check for spaces
        if c == ' ':
            # Skip
            ciphertext += c
            continue

        # Transform to ASCII decimal code
        ascii_char_value: int = ord(c)

        # Iterate through each character shift
        for shift in range(key):
            # Shift forwards by 1
            ascii_char_value += 1

            # Check for valis ASCII code
            if ascii_char_value > ASCII_RANGE["max"]:
                ascii_char_value = ASCII_RANGE["min"]
        
        # Transform to ASCII character
        ciphertext += chr(ascii_char_value)
    
    return ciphertext

def caesar_decrypt(ciphertext: str, key: int) -> str:
    ciphertext = sanatize(ciphertext)
    plaintext: str = ""

    ASCII_RANGE = {"max": 122, "min": 97}

    # Iterate through ciphertext
    for c in ciphertext:
        # Check for spaces
        if c == ' ':
            # Skip
            plaintext += c
            continue

        # Transform to ASCII decimal code
        ascii_char_value: int = ord(c)

        # Iterate through each character shift
        for shift in range(key):
            # Shift backwards by 1
            ascii_char_value -= 1

            # Check for valid ASCII range
            if ascii_char_value < ASCII_RANGE["min"]:
                ascii_char_value = ASCII_RANGE["max"]
        
        # Transform to ASCII character
        plaintext += chr(ascii_char_value)
    
    return plaintext

def railfence_fill(text: str, key: int) -> typing.List[typing.List]:
    grid: typing.List[typing.List] = [[None for _ in range(len(text))] for _ in range(key)]
    row: int = 0
    col: int = 0
    dir: int = 2 #(Even = Down, Odd = Up)

    # Iterate text
    for c in text:
        # Check if direction need changed
        if row+1 == key or (row == 0 and col != 0):
            dir += 1

        # Fill grid position
        grid[row][col] = c

        # Iterate row and col
        if dir % 2 == 0 and len(grid) > 1:
            row += 1
        elif dir % 2 != 0 and len(grid) > 1:
            row -= 1
        
        col += 1

    return grid

def railfence_replace(ciphertext: str, grid: typing.List[typing.List]) -> typing.List[typing.List]:
    # Iterate through ciphertext
    for char in ciphertext:
        is_found = False
        # Iterate through each row
        for row in range(len(grid)):
            # Check if char location already found
            if is_found:
                break
            # Iterate through each column 
            for col in range(len(grid[row])):
                # Check if char location already found
                if is_found:
                    break
                # Check if grid cordinate needs replaced
                if grid[row][col] == '.':
                    # Replace with character from ciphertext
                    grid[row][col] = char
                    is_found = True
    
    return grid

def railfence_collapse(grid: typing.List[typing.List]) -> str:
    plaintext: str = ""

    # Iterate through columns 
    for col in range(len(grid[0])):
        # Iterate through rows
        for row in range(len(grid)):
            # Check if grid space if filled
            if grid[row][col] is not None:
                # Append to plaintext
                plaintext += grid[row][col]
                # Check next column
                break
    
    return plaintext

def railfence_stack(grid: typing.List[typing.List]) -> str:
    ciphertext = ""

    # Iterate through rows
    for row in range(len(grid)):
        # Iterate through columns
        for col in range(len(grid[0])):
            # Check if grid space is set
            if grid[row][col] is not None:
                # Append to ciphertext
                ciphertext += grid[row][col]

    return ciphertext

def railfence_encrypt(plaintext: str, key: int) -> str:
    plaintext = sanatize(plaintext)

    grid = railfence_fill(text=plaintext, key=key)

    ciphertext = railfence_stack(grid=grid)

    return ciphertext

def railfence_decrypt(ciphertext: str, key: int) -> str:
    ciphertext = sanatize(ciphertext)

    grid = railfence_fill(text=('.' * len(ciphertext)), key=key)
    grid = railfence_replace(ciphertext=ciphertext, grid=grid)

    plaintext = railfence_collapse(grid=grid)

    return plaintext

def caesar_railfence_decrypt(ciphertext: str, key: int):
    # Decrypt railfence
    no_railfence = railfence_decrypt(ciphertext=ciphertext, key=key)

    # Decrypt caesar cipher
    plaintext = caesar_decrypt(ciphertext=no_railfence, key=key)

    return plaintext

def caesar_railfence_encrypt(plaintext: str, key: int):
    # Encrypt railfence
    ciphertext = railfence_encrypt(plaintext=plaintext, key=key)

    # Encrypt caesar cipher
    ciphertext = caesar_encrypt(plaintext=ciphertext, key=key)

    return ciphertext

def main():
    # Parse commandlin arguments
    parser = argparse.ArgumentParser(prog='IAE325Tool',
                                     description='Tool used to help with learning concepts in ISE325.')
    parser.add_argument('text', type=str, help='The text that will be processed by the program.')
    parser.add_argument('-t', '--type', type=str, required=True, help='Used to define the algorithm.', choices=['caesar', 'railfence', 'caesar/railfence'])
    parser.add_argument('-a', '--action', type=str, required=True, help='Tells the program what action to take with the algorithm and text.', choices=['decrypt', 'encrypt'])
    parser.add_argument('-k', '--key', type=int, help='Define the key to be used with the algorithm, defaults to 1.')
    parser.add_argument('-b', '--brute-force', action='store_true', help='Enabled brute force mode')
    parser.add_argument('-m', '--brute-force-max-key', type=int, help="Max key to try when brute forcing, defaults to 26.")
    args = parser.parse_args()

    # Check if key is passed
    if not args.key:
        args.key = 1
    else:
        # Ensure positive key
        args.key = abs(args.key)

    # Check if brute_force passed
    if args.brute_force:
        # Check for brute force max key
        if not args.brute_force_max_key:
            args.brute_force_max_key = 26
        else:
            args.brute_force_max_key = abs(args.brute_force_max_key)

    # Evaluate Type
    if args.type == 'caesar':
        # Evaluate Action
        if args.action == 'encrypt':
            print(f"{args.action} \"{args.text}\" with {args.type} when key is {args.key}:")
            print(caesar_encrypt(plaintext=args.text, key=args.key))

        elif args.action == 'decrypt':
            # Check for brute force
            if args.brute_force:
                print(f"brute force {args.action} \"{args.text}\" with {args.type}:")
                for key in range(args.brute_force_max_key):
                    print(f"when key is {key+1}")
                    print(f"\t{caesar_decrypt(ciphertext=args.text, key=key+1)}")
            else:
                print(f"{args.action} \"{args.text}\" with {args.type} when key is {args.key}:")
                print(caesar_decrypt(ciphertext=args.text, key=args.key))

    elif args.type == 'railfence':
        # Evaluate Action
        if args.action == 'encrypt':
            print(f"{args.action} \"{args.text}\" with {args.type} when key is {args.key}:")
            print(railfence_encrypt(plaintext=args.text, key=args.key))

        elif args.action == 'decrypt':
            # Check for brute force
            if args.brute_force:
                print(f"brute force {args.action} \"{args.text}\" with {args.type}:")
                for key in range(args.brute_force_max_key):
                    print(f"when key is {key+1}")
                    print(f"\t{railfence_decrypt(ciphertext=args.text, key=key+1)}")
            else:
                print(f"{args.action} \"{args.text}\" with {args.type} when key is {args.key}:")
                print(railfence_decrypt(ciphertext=args.text, key=args.key))

    elif args.type == 'caesar/railfence':
        # Evaluate Action
        if args.action == 'encrypt':
            print(f"{args.action} \"{args.text}\" with {args.type} when key is {args.key}:")
            print(caesar_railfence_encrypt(plaintext=args.text, key=args.key))

        elif args.action == 'decrypt':
            # Check for brute force
            if args.brute_force:
                print(f"brute force {args.action} \"{args.text}\" with {args.type}:")
                for key in range(args.brute_force_max_key):
                    print(f"when key is {key+1}")
                    print(f"\t{caesar_railfence_decrypt(ciphertext=args.text, key=key+1)}")
            else:
                print(f"{args.action} \"{args.text}\" with {args.type} when key is {args.key}:")
                print(caesar_railfence_decrypt(ciphertext=args.text, key=args.key))

if __name__ == "__main__":
    main()