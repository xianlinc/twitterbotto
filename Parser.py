import argparse

from Storage import *

def parse_operation(operation):
    if (operation == 'check-new'):
        new_following = check_for_new_following(args.handle)
        return new_following
    elif (operation == 'get-following'):
        following = get_following_from_db(args.handle)
        print(f"Here are the people @{args.handle} is following:\n{following}")
        return following
    elif (operation == 'get-accounts'):
        account_list = get_account_list()
        return account_list

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', help='operation')
    parser.add_argument('--handle', help='users twitter handle')

    args = parser.parse_args()
    parse_operation(args.operation)

    
            