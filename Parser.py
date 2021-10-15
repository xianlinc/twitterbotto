import argparse

from Storage import *

def parse_operation(operation):
    if (operation == 'check'):
        new_following = check_for_new_following(args.handle)
        return new_following
    elif (operation == 'following'):
        following = get_following_from_db(args.handle)
        print(f"Here are the people @{args.handle} is following:\n{following}")
        return following
    elif (operation == 'list'):
        account_list = get_account_list()
        return account_list
    else:
        print("I do not understand your command!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', help='operation')
    parser.add_argument('--handle', help='users twitter handle')

    args = parser.parse_args()
    parse_operation(args.operation)

    
            