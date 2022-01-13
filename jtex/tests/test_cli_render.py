import os
import subprocess
import tempfile


def test_cli_render():
    dir, _ = os.path.split(os.path.realpath(__file__))

    with tempfile.TemporaryDirectory() as tmp_dir:
        CLI_CMD = (
            f"jtex render "
            f"{os.path.join(dir, 'data', 'cn', 'main.tex')} "
            f"--output-path {tmp_dir} "
            f"--template-path {os.path.join(dir, 'data', 'cn', 'template')}"
        )
        ret_val = subprocess.run(CLI_CMD, shell=True)
        assert ret_val.returncode == 0
        assert os.path.exists(os.path.join(tmp_dir, "ms.tex"))

        with open(os.path.join(tmp_dir, "ms.tex"), "r") as outfile:
            actual = outfile.read()

        actual_lines = actual.split("\n")

        expected = (
            "% ---\n"
            "% authors:\n"
            "% - name: Curve Note\n"
            "% - name: An Other\n"
            "% date:\n"
            "%   day: 14\n"
            "%   month: 1\n"
            "%   year: 2022\n"
            "% jtex:\n"
            "%   input:\n"
            "%     tagged:\n"
            "%       abstract: abstract.tex\n"
            "%   options:\n"
            "%     choose: A\n"
            "%     corresponding_author:\n"
            "%     - email: joe@bloggs.com\n"
            "%       name: Joe Blogs\n"
            "%     flag: true\n"
            "%     keywords:\n"
            "%     - a\n"
            "%     - b\n"
            "%     - c\n"
            "%     text: Some String\n"
            "%   output:\n"
            "%     copy_images: true\n"
            "%     filename: ms.tex\n"
            "%     path: _build\n"
            "%     single_file: false\n"
            "%   strict: false\n"
            "%   template: default\n"
            "%   version: 1\n"
            "% title: Test Document\n"
            "% ---\n"
            "\\title{Test Document}\n"
            "\\author{Curve Note \\and An Other}\n"
            "\\newdate{articleDate}{14}{1}{2022}\n"
            "\date{\displaydate{articleDate}}\n"
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


def test_cli_render_from_api():
    dir, _ = os.path.split(os.path.realpath(__file__))

    with tempfile.TemporaryDirectory() as tmp_dir:
        CLI_CMD = (
            f"jtex render "
            f"{os.path.join(dir, 'data', 'cn', 'main.tex')} "
            f"--output-path {tmp_dir} "
        )
        ret_val = subprocess.run(CLI_CMD, shell=True)
        assert ret_val.returncode == 0
        assert os.path.exists(os.path.join(tmp_dir, "ms.tex"))

        with open(os.path.join(tmp_dir, "ms.tex"), "r") as outfile:
            actual = outfile.read()

        assert "% ---" in actual
        assert "% title: Test Document" in actual
        assert "\\title{Test Document}" in actual
        assert "curvenote_default" in actual
        assert "Lorem Abstractium" in actual
        assert "Lorem ipsum" in actual
