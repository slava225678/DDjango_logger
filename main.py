import argparse
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, List
from constants import FIVE, LEVELS, NULL, ONE, RESULT, TOTAL_REQ, TWO


def print_report(
        data: DefaultDict[str, DefaultDict[str, int]],
        report_type: str = 'handlers'
) -> None:
    '''Форматирует и выводит отчёт в виде таблицы.

    Args:
        data (defaultdict): Собранная статистика по логам
        report_type (str): Тип отчёта ('handlers' или 'summary')
    '''
    if report_type == 'handlers':
        print('\nОтчёт по обработчикам (handlers):')
        formatted_levels = [f'{level:^10}' for level in LEVELS]
        joined_levels = ' '.join(formatted_levels)
        final_output_lvl = '{:^25} {}'.format('HANDLER', joined_levels)
        print(final_output_lvl)

        for handler in sorted(data.keys()):
            if handler == RESULT:
                continue
            counts = [data[handler].get(level, NULL) for level in LEVELS]
            formatted_handler = [f'{count:^10}' for count in counts]
            joined_handlers = ' '.join(formatted_handler)
            final_output_hand = '{:<25} {}'.format(handler, joined_handlers)
            print(final_output_hand)

        if RESULT in data:
            counts = [data[RESULT].get(level, NULL) for level in LEVELS]
            formatted_counts = ' '.join(f'{count:^10}' for count in counts)
            print('\n{:<25} {}'.format(TOTAL_REQ, formatted_counts))

    elif report_type == 'summary':
        print('\nСводный отчёт (summary):')
        total = sum(
            sum(level_counts.values()) for level_counts in data.values()
        )
        print(f'Всего запросов: {total}')

        for level in LEVELS:
            level_total = sum(data[handler].get(level, 0) for handler in data)
            print(f'{level}: {level_total}')


def analyze_logs(
        log_files: List[Path]
) -> DefaultDict[str, DefaultDict[str, int]]:
    '''Анализирует логи Django и собирает статистику.'''
    final_stats = defaultdict(lambda: defaultdict(int))

    for file in log_files:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                if 'django.request:' not in line:
                    continue

                parts = line.split()
                if len(parts) < FIVE:
                    continue

                handler = parts[7] if parts[FIVE] == 'Server' else parts[FIVE]
                level = parts[TWO]

                final_stats[handler][level] += ONE
                final_stats[RESULT][level] += ONE

    return final_stats


def parse_args() -> argparse.Namespace:
    '''Парсит аргументы командной строки.'''
    parser = argparse.ArgumentParser(description='Анализатор логов Django')
    parser.add_argument(
        'log_files',
        nargs='+',
        type=Path,
        help='Пути к файлам логов (можно указать несколько)'
    )
    parser.add_argument(
        '--report',
        choices=['handlers', 'summary'],
        default='handlers',
        help='Тип отчёта (handlers - по обработчикам, summary - сводный)'
    )
    return parser.parse_args()


def main() -> None:
    '''Главная функция, объединяющая все компоненты.'''
    args = parse_args()

    # Проверка существования файлов
    valid_files = []
    for log_file in args.log_files:
        if not log_file.exists():
            print(f'Предупреждение: файл {log_file} не найден, пропускаем')
        else:
            valid_files.append(log_file)
    if not valid_files:
        print('Ошибка: не указано ни одного существующего файла логов')
        return
    stats = analyze_logs(valid_files)
    if stats:
        print_report(stats, args.report)


if __name__ == '__main__':
    main()
