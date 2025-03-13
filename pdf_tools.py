import os
import argparse
import logging
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import fitz  # PyMuPDF
from PIL import Image
import io

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def merge_pdfs(input_files, output_file):
    """Объединяет несколько PDF файлов в один"""
    try:
        merger = PdfMerger()
        
        for pdf_file in input_files:
            if not os.path.exists(pdf_file):
                logging.error(f"Файл не найден: {pdf_file}")
                continue
            merger.append(pdf_file)
        
        merger.write(output_file)
        merger.close()
        logging.info(f"PDF файлы успешно объединены в: {output_file}")
        return True
    except Exception as e:
        logging.error(f"Ошибка при объединении PDF: {str(e)}")
        return False

def split_pdf(input_file, output_dir):
    """Разделяет PDF файл на отдельные страницы"""
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        reader = PdfReader(input_file)
        total_pages = len(reader.pages)
        
        for page_num in range(total_pages):
            writer = PdfWriter()
            writer.add_page(reader.pages[page_num])
            
            output_file = os.path.join(output_dir, f"page_{page_num + 1}.pdf")
            with open(output_file, "wb") as out:
                writer.write(out)
            
            logging.info(f"Создана страница {page_num + 1} из {total_pages}: {output_file}")
        
        return True
    except Exception as e:
        logging.error(f"Ошибка при разделении PDF: {str(e)}")
        return False

def extract_text(input_file, output_file=None):
    """Извлекает текст из PDF файла"""
    try:
        text = []
        doc = fitz.open(input_file)
        
        for page_num in range(len(doc)):
            text.append(doc[page_num].get_text())
        
        full_text = "\n\n".join(text)
        
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(full_text)
            logging.info(f"Текст сохранен в файл: {output_file}")
        else:
            print("\nИзвлеченный текст:")
            print("-" * 40)
            print(full_text)
        
        return True
    except Exception as e:
        logging.error(f"Ошибка при извлечении текста: {str(e)}")
        return False

def extract_images(input_file, output_dir):
    """Извлекает изображения из PDF файла"""
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        doc = fitz.open(input_file)
        image_count = 0
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            images = page.get_images()
            
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                
                # Определяем формат изображения
                image_ext = base_image["ext"]
                image_path = os.path.join(
                    output_dir,
                    f"image_p{page_num + 1}_{img_index + 1}.{image_ext}"
                )
                
                # Сохраняем изображение
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)
                image_count += 1
                
                logging.info(f"Сохранено изображение: {image_path}")
        
        logging.info(f"Всего извлечено изображений: {image_count}")
        return True
    except Exception as e:
        logging.error(f"Ошибка при извлечении изображений: {str(e)}")
        return False

def compress_pdf(input_file, output_file, quality="medium"):
    """Сжимает PDF файл"""
    try:
        # Определяем параметры сжатия
        quality_settings = {
            "low": 30,      # Сильное сжатие
            "medium": 50,   # Среднее сжатие
            "high": 70      # Легкое сжатие
        }
        
        if quality not in quality_settings:
            quality = "medium"
        
        doc = fitz.open(input_file)
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Сжимаем изображения на странице
            for img in page.get_images():
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                
                # Открываем изображение с помощью PIL
                image = Image.open(io.BytesIO(image_bytes))
                
                # Сжимаем изображение
                output_buffer = io.BytesIO()
                image.save(output_buffer, 
                         format=base_image["ext"],
                         quality=quality_settings[quality],
                         optimize=True)
                
                # Заменяем изображение в PDF
                page.delete_image(xref)
                page.insert_image(
                    img[1],  # Прямоугольник изображения
                    stream=output_buffer.getvalue()
                )
        
        # Сохраняем сжатый PDF
        doc.save(output_file, 
                garbage=4,  # Максимальная очистка мусора
                deflate=True,  # Сжатие потоков
                clean=True)  # Очистка и оптимизация
        
        # Выводим информацию о размерах
        original_size = os.path.getsize(input_file)
        compressed_size = os.path.getsize(output_file)
        saved = original_size - compressed_size
        saved_percent = (saved / original_size) * 100
        
        logging.info(f"PDF успешно сжат: {output_file}")
        logging.info(f"Исходный размер: {original_size / 1024:.2f} KB")
        logging.info(f"Размер после сжатия: {compressed_size / 1024:.2f} KB")
        logging.info(f"Сэкономлено: {saved / 1024:.2f} KB ({saved_percent:.1f}%)")
        
        return True
    except Exception as e:
        logging.error(f"Ошибка при сжатии PDF: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Инструменты для работы с PDF файлами')
    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')
    
    # Объединение PDF
    merge_parser = subparsers.add_parser('merge', help='Объединить PDF файлы')
    merge_parser.add_argument('input_files', nargs='+', help='Входные PDF файлы')
    merge_parser.add_argument('output_file', help='Выходной PDF файл')
    
    # Разделение PDF
    split_parser = subparsers.add_parser('split', help='Разделить PDF на страницы')
    split_parser.add_argument('input_file', help='Входной PDF файл')
    split_parser.add_argument('output_dir', help='Директория для выходных файлов')
    
    # Извлечение текста
    text_parser = subparsers.add_parser('text', help='Извлечь текст из PDF')
    text_parser.add_argument('input_file', help='Входной PDF файл')
    text_parser.add_argument('--output', help='Выходной текстовый файл')
    
    # Извлечение изображений
    images_parser = subparsers.add_parser('images', help='Извлечь изображения из PDF')
    images_parser.add_argument('input_file', help='Входной PDF файл')
    images_parser.add_argument('output_dir', help='Директория для сохранения изображений')
    
    # Сжатие PDF
    compress_parser = subparsers.add_parser('compress', help='Сжать PDF файл')
    compress_parser.add_argument('input_file', help='Входной PDF файл')
    compress_parser.add_argument('output_file', help='Выходной PDF файл')
    compress_parser.add_argument('--quality', 
                               choices=['low', 'medium', 'high'],
                               default='medium',
                               help='Качество сжатия')
    
    args = parser.parse_args()
    
    if args.command == 'merge':
        merge_pdfs(args.input_files, args.output_file)
    elif args.command == 'split':
        split_pdf(args.input_file, args.output_dir)
    elif args.command == 'text':
        extract_text(args.input_file, args.output)
    elif args.command == 'images':
        extract_images(args.input_file, args.output_dir)
    elif args.command == 'compress':
        compress_pdf(args.input_file, args.output_file, args.quality)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()