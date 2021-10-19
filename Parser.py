import argparse

from Storage import check_for_new_following
from Storage import get_following_from_db
from Storage import get_account_list
from Storage import add_account


def parse_operation(operation):
    if (operation == 'check'):
        check_for_new_following(args.handle)
    elif (operation == 'following'):
        following = get_following_from_db(args.handle)
        print(f"Here are the people @{args.handle} is following:\n{following}")
    elif (operation == 'list'):
        get_account_list()
    elif (operation == 'stalk'):
        add_account(args.handle)
    else:
        print("I do not understand your command!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', help='operation')
    parser.add_argument('--handle', help='users twitter handle')

    args = parser.parse_args()
    parse_operation(args.operation)
