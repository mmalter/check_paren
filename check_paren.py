"""check_paren

Usage:
  check_paren.py [--spec=<brackets_pairs>] [--pretty] <string>...
  check_paren.py (-h | --help)
  check_paren.py --version

Options:
  --spec=str    Pair of brackets [default: ()[]{}]
  --pretty      Pretty printing
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt
import functools
import operator

foldl = lambda func, acc, xs: functools.reduce(func, xs, acc)

def paren_counter(bracket_spec):
    def fun(acc, character):
        if acc == "order_inconsistency":
            return "order_inconsistency"
        if acc < 0:
            return "order_inconsistency"
        if character == bracket_spec[0]:
            return acc + 1
        if character == bracket_spec[1]:
            return acc - 1
        return acc
    return fun

def count_paren(bracket_specs, to_check):
    for bracket_spec in bracket_specs:
        fun = paren_counter(bracket_spec)
        yield bracket_spec, foldl(fun, 0, to_check)

def format_result(duple, pretty):
    spec, result = duple
    if pretty == False:
        print(duple)
    else:
        if result == "order_inconsistency":
            print("Bad parenthesis order for spec {}".format(spec))
        elif result == 0:
            print("Consistent delimiters for spec {}".format(spec))
        elif result > 0:
            print("Too many {}".format(spec[0]))
        elif result < 0:
            print("Too many {}".format(spec[1]))


def main(arguments):
    bracket_specs = [arguments['--spec'][i:i+2] for i in
                     range(0, len(arguments['--spec']), 2)]
    to_check = " ".join(arguments['<string>'])
    return count_paren(bracket_specs, to_check)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Milner')
    fun = functools.partial(format_result, pretty=arguments['--pretty'])
    list(map(fun, list(main(arguments))))
