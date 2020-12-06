import fileinput
import re

if __name__ == '__main__':
    # replace useless characters
    expr = re.compile(r'\(cid:\w*\)', re.IGNORECASE)
    expr2 = re.compile(r'This content downloaded .*?/terms.', re.IGNORECASE)
    with fileinput.FileInput('./jstortext/b.txt', inplace=True) as f:
        for line in f:
            print(expr2.sub('', expr.sub('', line)), end='')