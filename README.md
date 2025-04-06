``Заупск тестов``
```python
pytest tests/ -v
```

``Вариант с использованием регулярного выражения``
```python
import re
from collections import defaultdict
from pathlib import Path
from constants import LEVELS, NULL, HANDLER


def print_report(data):
    '''Форматирует и выводит отчет в виде таблицы.
    
    Args:
        data (defaultdict): Собранная статистика по логам
    '''
    formatted_levels = [f'{level:^10}' for level in LEVELS]
    joined_levels = ' '.join(formatted_levels)
    final_output_lvl = '{:^25} {}'.format(
        HANDLER,
        joined_levels
    )
    print(final_output_lvl)
    
    for handler in sorted(data.keys()):
        if not data:
            continue
        counts = [data[handler].get(level, NULL) for level in LEVELS]
        formatted_handler = [f'{count:^10}' for count in counts]
        joined_handlers = ' '.join(formatted_handler)
        final_output_hand = '{:<25} {}'.format(
            handler,
            joined_handlers
        )
        print(final_output_hand)


def analyze_logs(log_files):
    '''Анализирует логи Django с использованием регулярных выражений.
    
    Args:
        log_files (list): Список путей к файлам логов
        
    Returns:
        defaultdict: Собранная статистика
    '''
    log_dict = defaultdict(lambda: defaultdict(int))
    log_pattern = re.compile(
        r'^(?P<timestamp>.+?)\s+'
        r'(?P<level>\w+)\s+'
        r'django\.request:\s+'
        r'.*?(?P<handler>/[^\s\]]+)'
    )

    for file_path in log_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = log_pattern.match(line)
                if match:
                    level = match.group('level')
                    handler = match.group('handler')
                    log_dict[handler][level] += ONE
                    log_dict[RESULT][level] += ONE

    return log_dict


def parse_args():
    '''Парсит аргументы командной строки.
    
    Returns:
        Namespace: Объект с распарсенными аргументами
    '''
    parser = argparse.ArgumentParser(description='Анализатор логов Django')
    parser.add_argument(
        'log_files',
        nargs='+',
        type=Path,
        help='Пути к файлам логов (можно указать несколько)'
    )
    return parser.parse_args()


def main():
    '''Главная функция, объединяющая все компоненты.'''
    args = parse_args()
    
    for log_file in args.log_files:
        if not log_file.exists():
            print(
                f'Ошибка: файл {log_file} не найден. '
                'Проверьте существование файла в нужной директории logs/'
            )
            return

    data = analyze_logs(args.log_files)
    print_report(data)


if __name__ == '__main__':
    import argparse
    main()
```
![image](https://github.com/user-attachments/assets/4b1f2051-58a6-4e17-b714-f5fbf5618a3b)

![image](https://github.com/user-attachments/assets/c2b7beaa-7bd4-4c54-be2b-926e054a6e39)

