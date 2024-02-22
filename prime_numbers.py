
import argparse

def check_if_number_is_actually_prime(number_to_check: int) -> bool:
    if number_to_check <= 1:
        return False
    if number_to_check == 2:
        return True
    if number_to_check % 2 == 0:
        return False
    for i in range(3, int(number_to_check**0.5) + 1, 2):
        if number_to_check % i == 0:
            return False
    return True

def get_list_of_primes(lower_bound: int, upper_bound: int) -> list[int]:
    return list(filter(bool,[(current_integer if(check_if_number_is_actually_prime(current_integer)) else 0) for current_integer in range(lower_bound, upper_bound + 1)]))

def main(args)->None:

    print(get_list_of_primes(lower_limit, upper_limit))

    return


if("__main__" == __name__):

    parser = argparse.ArgumentParser(description="Calculate prime numbers within a range")
    parser.add_argument("lower", type=int, help="Lower limit of the range")
    parser.add_argument("upper", type=int, help="Upper limit of the range")
    args = parser.parse_args()


    lower_limit:int = args.lower
    upper_limit:int = args.upper

    if(upper_limit < lower_limit):
        print("Upper limit cannot be less than lower limit.")
        exit()

    main(args)
