# Инструменты для работы с PDF

Набор полезных инструментов для работы с PDF файлами на Python. Программа позволяет выполнять различные операции с PDF документами: объединение, разделение, извлечение текста и изображений, сжатие.

## Возможности

- Объединение нескольких PDF файлов в один
- Разделение PDF файла на отдельные страницы
- Извлечение текста из PDF
- Извлечение изображений из PDF
- Сжатие PDF файлов с настраиваемым качеством

## Установка

```bash
git clone https://github.com/looapz/py-pdf-tools.git
cd py-pdf-tools
pip install -r requirements.txt
```

## Использование

### Объединение PDF файлов

```bash
python pdf_tools.py merge input1.pdf input2.pdf input3.pdf output.pdf
```

### Разделение PDF на страницы

```bash
python pdf_tools.py split input.pdf output_directory
```

### Извлечение текста

Вывод в консоль:
```bash
python pdf_tools.py text input.pdf
```

Сохранение в файл:
```bash
python pdf_tools.py text input.pdf --output text.txt
```

### Извлечение изображений

```bash
python pdf_tools.py images input.pdf images_directory
```

### Сжатие PDF

```bash
python pdf_tools.py compress input.pdf output.pdf --quality medium
```

Доступные уровни качества:
- low: сильное сжатие
- medium: среднее сжатие (по умолчанию)
- high: легкое сжатие

## Особенности

- Поддержка всех основных операций с PDF
- Удобный интерфейс командной строки
- Подробное логирование операций
- Настраиваемые параметры сжатия
- Сохранение метаданных при обработке
- Обработка ошибок и информативные сообщения

## Зависимости

- PyPDF2: для базовых операций с PDF
- PyMuPDF: для извлечения текста и изображений
- Pillow: для обработки изображений

## Требования к системе

- Python 3.6 или выше
- Установленные зависимости из requirements.txt

## Лицензия

MIT