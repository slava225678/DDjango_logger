from main import analyze_logs


def test_analyze_logs_counts_requests(sample_log_file):
    result = analyze_logs([sample_log_file])
    assert result["/api/test/"]["INFO"] == 1
    assert result["/api/test/"]["ERROR"] == 1
    assert result["/api/another/"]["INFO"] == 1


def test_analyze_logs_counts_totals(sample_log_file):
    result = analyze_logs([sample_log_file])
    assert result["RESULT"]["INFO"] == 2
    assert result["RESULT"]["ERROR"] == 1


def test_analyze_logs_empty_file(tmp_path):
    empty_file = tmp_path / "empty.log"
    empty_file.write_text("")
    result = analyze_logs([empty_file])
    assert len(result) == 0
