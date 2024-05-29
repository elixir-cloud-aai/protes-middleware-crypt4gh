import sys


def get_uppercase_contents(file_name):
    with open(file_name, encoding='utf-8') as f:
        content = f.readline()
        return content.upper()


if __name__ == '__main__':
    file = sys.argv[1]
    print(get_uppercase_contents(file), end='')