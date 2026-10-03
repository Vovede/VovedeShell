# UNIX-like shell emulator

Эмулятор языка оболочки ОС для практической работы №1.

## Текущий этап

Подготовлена базовая структура Python-проекта и Git-репозитория.
Реализация команд будет добавляться на следующих шагах.

## Структура проекта

```text
shell-emulator/
├── README.md
├── .gitignore
├── Makefile
├── run.sh
├── src/
│   └── shell/
│       └── main.py
├── tests/
│   └── test_project.py
├── data/
└── scripts/
```

## Требования

- Python 3.11 или новее.
- Внешние зависимости не используются.

## Запуск

```bash
./run.sh
```

или:

```bash
make run
```

## Тесты

```bash
./run.sh --test
```

или:

```bash
make test
```
