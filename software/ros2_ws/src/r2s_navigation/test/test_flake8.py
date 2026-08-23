# Copyright (c) 2026 R2-Sentinel — Apache-2.0
from ament_flake8.main import main_with_errors
import pytest


@pytest.mark.flake8
@pytest.mark.linter
def test_flake8():
    rc, errors = main_with_errors(argv=[])
    assert rc == 0, "Trovati %d errori flake8:\n%s" % (
        len(errors), "\n".join(errors))
