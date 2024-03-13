
def main():
    def eculidian(num1: int, num2: int):
        number_set = {num1, num2}

        left_side = max(number_set)
        right_side = min(number_set)

        while True:
            quotient = left_side // right_side
            remainder = left_side % right_side

            print(f"{left_side} = {right_side} * {quotient} + {remainder}")

            if remainder == 0:
                print(f"GCD of {num1} and {num2} is {right_side}")
                break
                
            left_side = right_side
            right_side = remainder
    
    while True:
        first_num = input("Enter the first number: ")
        second_num = input("Enter the second number: ")
        eculidian(int(first_num), int(second_num))

if __name__ == '__main__':
    main()