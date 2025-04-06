import pytest
from collections import defaultdict


@pytest.fixture
def sample_log_file(tmp_path):
    log_data = """2023-01-01 12:00:00 INFO django.request: GET /api/test/ 200
2023-01-01 12:01:00 ERROR django.request: POST /api/test/ 500
2023-01-01 12:02:00 INFO django.request: GET /api/another/ 200"""
    file_path = tmp_path / "test.log"
    file_path.write_text(log_data)
    return file_path


@pytest.fixture
def sample_stats():
    stats = defaultdict(lambda: defaultdict(int))
    stats["/api/test/"]["INFO"] = 2
    stats["/api/test/"]["ERROR"] = 1
    stats["/api/another/"]["INFO"] = 1
    stats["RESULT"]["INFO"] = 3
    stats["RESULT"]["ERROR"] = 1
    return stats
