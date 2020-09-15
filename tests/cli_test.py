from library.cli import main


def test_with_no_args():
    assert main() == 0
