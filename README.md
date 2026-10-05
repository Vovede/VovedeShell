# VovedeShell

Эмулятор командной оболочки UNIX-подобной операционной системы,
реализованный на Python.

Проект выполняется в рамках учебного задания по дисциплине
«Конфигурационное управление».

## Требования

* Python 3.12+
* pytest

## Запуск

Все команды выполняются из корневой папки проекта.

### Запуск в интерактивном режиме

```text
.\run.bat
```

Запускает shell в интерактивном режиме.

### Запуск с VFS

```text
.\run.bat --vfs data\vfs.json
```

Запускает shell и загружает виртуальную файловую систему
из указанного JSON-файла.

### Запуск стартового скрипта

```text
.\run.bat --script scripts\start.txt
```

Запускает shell и последовательно выполняет команды
из указанного стартового скрипта.

### Запуск с VFS и стартовым скриптом

```text
.\run.bat --vfs data\vfs.json --script scripts\start.txt
```

Сначала загружает VFS из JSON-файла, затем выполняет команды
из стартового скрипта.

### Просмотр справки

```text
.\run.bat --help
```

Показывает доступные параметры командной строки.

## Тестирование

### Запуск всех тестов

```text
python -m pytest
```

Запускает все тесты проекта.

### Запуск тестов с подробным выводом

```text
python -m pytest -v
```

### Запуск тестов отдельного модуля

```text
python -m pytest tests\test_parser.py
python -m pytest tests\test_shell.py
python -m pytest tests\test_script.py
python -m pytest tests\test_vfs.py
python -m pytest tests\test_project.py
```
