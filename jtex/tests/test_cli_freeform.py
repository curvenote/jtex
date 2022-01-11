import os
import subprocess
import tempfile


def test_cli_freeform():

    dir, _ = os.path.split(os.path.realpath(__file__))

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file = os.path.join(tmp_dir, next(tempfile._get_candidate_names()))
        tmp_file = "test_tmp_ff/main.tex"
        CLI_CMD = (
            f"jtex freeform "
            f"{os.path.join(dir, 'data', 'lite', 'template.tex')} "
            f"{os.path.join(dir, 'data', 'lite', 'main.tex')} "
            f"--output-tex {tmp_file} "
        )
        ret_val = subprocess.run(CLI_CMD, shell=True)
        assert ret_val.returncode == 0

        with open(tmp_file, "r") as outfile:
            actual = outfile.read()

        actual_lines = actual.split("\n")

        expected = (
            "% ---\n"
            "% authors:\n"
            "% - name: Curve Note\n"
            "% - name: An Other\n"
            "% tagged:\n"
            "%   abstract: Lorem Abstractium\n"
            "% title: Freeform Rendering\n"
            "% ---\n"
            "\\author{Curve Note}\n"
            "\\author{An Other}\n"
            "\\begin{abstract}\n"
            "Lorem Abstractium\n"
            "\\end{abstract}\n"
            "Lorem ipsum"
        )

        expected_lines = expected.split("\n")

        for n in range(0, len(expected_lines)):
            assert len(actual_lines) > n
            assert actual_lines[n] == expected_lines[n]

        assert expected == actual
