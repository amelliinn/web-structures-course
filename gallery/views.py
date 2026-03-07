from django.shortcuts import render, redirect
import base64
from django.core.files.base import ContentFile
from .models import Asset
from .forms import AssetForm
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator 
from django.contrib import messages


def home(request):
    # 1. Получаем параметры из URL (GET-запроса)
    search_query = request.GET.get('q', '')
    ordering = request.GET.get('ordering', 'new')  # По умолчанию 'new'
    days = request.GET.get('days') 

    # 2. Базовый запрос: Берем ВСЕ
    assets = Asset.objects.all()

    # 3. Применяем поиск (если пользователь что-то ввел)
    if search_query:
        assets = assets.filter(title__icontains=search_query)

    # 4. Фильтр по дням (если указан)
    if days:
        assets = assets.filter(created_at__gte=timezone.now() - timedelta(days=int(days)))

    # 5. Применяем сортировку
    if ordering == 'old':
        assets = assets.order_by('created_at')  # От старых к новым
    elif ordering == 'name':
        assets = assets.order_by('title')  # По алфавиту
    else:
        # По умолчанию (new) - свежие сверху
        assets = assets.order_by('-created_at')

    # 6. ПАГИНАЦИЯ
    paginator = Paginator(assets, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 7. Отдаем результат
    context_data = {
        'page_title': 'Главная Галерея',
        'page_obj': page_obj,
        'search_query': search_query,
        'ordering': ordering,
        'days': days,
    }
    
    return render(request, 'gallery/index.html', context_data)

def about(request):
    """Страница 'О нас'"""
    context = {
        'page_title': 'О нас',
    }
    return render(request, 'gallery/about.html', context)

def upload(request):
    if request.method == 'POST':
        form = AssetForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. Создаем объект, но пока НЕ сохраняем в базу (commit=False)
            new_asset = form.save(commit=False)
            
            # 2. Обрабатываем картинку из скрытого поля
            image_data = request.POST.get('image_data')
            if image_data:
                # Формат строки: "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]  # получаем "jpeg"
                
                # Декодируем текст в байты
                data = base64.b64decode(imgstr)
                
                # Создаем безопасное имя файла (очищаем от спецсимволов)
                safe_title = "".join(x for x in new_asset.title if x.isalnum() or x in [' ', '-', '_'])[:50]
                file_name = f"{safe_title}_thumb.{ext}"
                
                # Сохраняем байты в поле image
                new_asset.image.save(file_name, ContentFile(data), save=False)
            
            # 3. Финальное сохранение в БД
            new_asset.save()
            
            # ✅ ДОБАВЛЯЕМ СООБЩЕНИЕ ОБ УСПЕХЕ
            messages.success(request, f'Модель "{new_asset.title}" успешно загружена!')
            
            return redirect('home')
    else:
        form = AssetForm()
    
    return render(request, 'gallery/upload.html', {'form': form})