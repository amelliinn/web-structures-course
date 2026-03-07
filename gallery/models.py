# Импортируем базовый класс для создания моделей
from django.db import models
import os

# Создаем класс Asset, который наследуется от models.Model
# Каждый такой класс - это будущая таблица в базе данных
class Asset(models.Model):
    # Поле "Название" - строка до 200 символов
    # CharField - тип данных для короткого текста
    # verbose_name - отображаемое имя в админке
    title = models.CharField(max_length=200, verbose_name="Название модели")
    
    # Поле для файла 3D-модели
    # FileField НЕ хранит файл в БД, только путь к нему
    # upload_to - подпапка в media/ куда будут сохраняться файлы
    # '3d_assets/' - создаст папку media/3d_assets/
    file = models.FileField(upload_to='3d_assets/', verbose_name="3D файл")
    
    # --- НОВОЕ ПОЛЕ ДЛЯ ПРЕВЬЮ ---
    # ImageField для хранения скриншота
    # blank=True, null=True - разрешаем пустые значения (на случай, если скриншот не удался)
    image = models.ImageField(
        upload_to='thumbnails/', 
        blank=True, 
        null=True,
        verbose_name="Превью"
    )
    
    # Поле "Дата создания"
    # DateTimeField - тип для даты и времени
    # auto_now_add=True - автоматически ставит текущее время при создании записи
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    
    # Магический метод для строкового представления объекта
    # Без него в админке будет "Asset object (1)", с ним - название модели
    def __str__(self):
        return self.title
    
    # Класс Meta для дополнительных настроек модели
    class Meta:
        # Как будет называться одна запись в админке
        verbose_name = "3D Модель"
        # Как будет называться раздел с записями
        verbose_name_plural = "3D Модели"
    
    # Дополнительный метод для безопасного получения размера файла
    @property
    def file_size_safe(self):
        """Безопасно возвращает размер файла или None если файла нет"""
        try:
            if self.file and os.path.exists(self.file.path):
                return self.file.size
        except (FileNotFoundError, ValueError, OSError):
            return None
        return None