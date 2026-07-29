# -*- coding: utf-8 -*-

from os import environ as env
from unittest.mock import patch

from varstore import expand as expandvars


@patch.dict(env, {"EXPANDVARS_RECOVER_NULL": "foo", "BAR": "bar"}, clear=True)
def test_strict_parsing_recover_null():

    assert expandvars.expandvars("${FOO:?}:${BAR?}") == "foo:bar"
    assert expandvars.expandvars("${FOO:?custom err}:${BAR?custom err}") == "foo:bar"

    assert expandvars.expandvars("$FOO$BAR", nounset=True) == "foobar"
    assert expandvars.expandvars("${FOO}:${BAR}", nounset=True) == "foo:bar"
