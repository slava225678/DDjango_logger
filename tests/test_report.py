from main import print_report


def test_print_report_handlers_format(capsys, sample_stats):
    print_report(sample_stats)
    captured = capsys.readouterr()
    assert "HANDLER" in captured.out
    assert "/api/test/" in captured.out
    assert "INFO" in captured.out
    assert "2" in captured.out


def test_print_report_summary_format(capsys, sample_stats):
    print_report(sample_stats, "summary")
    captured = capsys.readouterr()
    assert "Сводный отчёт" in captured.out
    assert "Всего запросов" in captured.out
    assert "INFO" in captured.out
