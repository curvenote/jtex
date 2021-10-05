import os
import subprocess
import tempfile


def test_cli_build():
    dir, _ = os.path.split(os.path.realpath(__file__))

    with tempfile.TemporaryDirectory() as tmp_dir:
        CLI_CMD = (
            f"curvenote_template build {tmp_dir} "
            f"{os.path.join(dir, 'data', 'cn')} "
            f"{os.path.join(dir, 'data', 'cn', 'template')}"
        )
        ret_val = subprocess.run(CLI_CMD, shell=True)
        assert ret_val.returncode == 0
        assert os.path.exists(os.path.join(tmp_dir, "main.tex"))

        with open(os.path.join(tmp_dir, "main.tex"), "r") as outfile:
            actual = outfile.read()

        actual_lines = actual.split("\n")

        expected = (
            "\\title{Test Document}\n"
            "\\author{Curve Note \\and An Other}\n"
            "\\begin{document}\n"
            "\\maketitle\n"
            "\\begin{abstract}\n"
            "Lorem Abstractium\n"
            "\\end{abstract}\n"
            "Option text: Some String\n"
            "Option flag - this content was added because the flag was True\n"
            "Option keywords:\n"
            "a,b,c,\n"
            "Choose:\n"
            "A\n"
            "Corresponding:\n"
            "Joe Blogs, joe@bloggs.com\n"
            "Lorem ipsum\n"
            "\\end{document}\n"
        )

        expected_lines = expected.split("\n")

        for n in range(0, len(expected_lines)):
            assert len(actual_lines) > n
            assert actual_lines[n] == expected_lines[n]

        assert expected == actual
