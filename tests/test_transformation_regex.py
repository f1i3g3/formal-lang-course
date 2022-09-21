from project.transformation_lib import *
from pyformlang.regular_expression import MisformedRegexError

import pytest


def test_wrong():
    with pytest.raises(MisformedRegexError):
        regex_to_nfa("[*|.]")


def test_power_two():
    dfa = regex_to_nfa("1 (0)*")
    assert dfa.is_deterministic
    for i in range(1, 5):
        assert dfa.accepts("{0:b}".format(2**i))
    assert not dfa.accepts("0")
    assert not dfa.accepts("1001")


def test_binary_ended_by_zero():
    dfa = regex_to_nfa("(0|1)* 0")
    assert dfa.is_deterministic
    for i in range(0, 42, 2):
        assert dfa.accepts("{0:b}".format(i))
        assert not dfa.accepts("{0:b}".format(i + 1))
