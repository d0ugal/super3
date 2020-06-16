import os

from super3 import __version__
from super3 import main

DIR = os.path.dirname(__file__)
INPUT = os.path.join(DIR, "input.py")
OUTPUT = os.path.join(DIR, "output.py")


def test_upgrade():

    source_file = main.load_file(INPUT)
    lines = source_file.source.splitlines()
    for violation in main.list_violations(source_file):
        main.upgrade_string(lines, violation)

    with open(OUTPUT) as f:
        expected = f.read()

    # TODO: This newline handling needs fixed
    result = "\n".join(lines) + "\n"

    assert expected == result


def test_upgrade_no_change():

    source_file = main.load_file(OUTPUT)
    lines = source_file.source.splitlines()
    for violation in main.list_violations(source_file):
        main.upgrade_string(lines, violation)

    with open(OUTPUT) as f:
        expected = f.read()

    # TODO: This newline handling needs fixed
    result = "\n".join(lines) + "\n"

    assert expected == result


def test_has_violations_positive():
    assert main.has_violation(main.load_file(INPUT))


def test_has_violations_negative():
    assert not main.has_violation(main.load_file(OUTPUT))


def test_list_violations():

    input_code = main.load_file(INPUT)

    assert [
        main.Violation(col_offset=8, end_col_offset=22, lineno=12, end_lineno=12,),
        main.Violation(col_offset=8, end_col_offset=22, lineno=17, end_lineno=17,),
    ] == list(main.list_violations(input_code))
