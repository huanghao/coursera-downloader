import os

from cdl.parser import parse


with open(os.path.join(
        os.path.dirname(__file__), 'pkuco-001_lecture.html')) as file:
    PKUCO_HTML = file.read()


def test_pkuco():
    res = parse(PKUCO_HTML)

    assert len(res) == 5     # 5 chapters
    assert len(res[0][1]) == 7  # 7 lecuters in chapter1

    from cdl.parser import generate_download_script
    print '\n'.join(generate_download_script(res))


test_pkuco()
