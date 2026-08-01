from pathlib import Path

from digdep.analyzer import DepAnalyzer


def test_stats():
    project = Path(__file__).parent / "testpkg"

    analyzer = DepAnalyzer()
    analyzer.analyze(project)

    stats = analyzer.stats

    assert stats.files == 13
    assert stats.imports == 26
    assert stats.used_imports == 16
    assert stats.unused_imports == 9

    assert stats.stdlib == 12
    assert stats.third_party == 3
    assert stats.local == 6
