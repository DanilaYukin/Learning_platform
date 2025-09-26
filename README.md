# Learning Platform Backend

Бэкенд для платформы самообучения, позволяющий управлять разделами, уроками, материалами и тестами, а также пользователями.

---

## 🚀 Основные возможности

- Модуль **users**: регистрация, аутентификация, управление профилем пользователей.  
- Модуль **education**:  
  - разделы (Sections)  
  - уроки (Lessons)   
  - тесты по урокам (Tests)  
- Модуль **config**: настройки приложения (настройка окружения, константы и конфигурации).  

---

## 🛠 Технологии

- Python  
- Django 
- База данных PostgreSQL  
- Виртуальное окружение .venv  
- Менеджер зависимостей: `requirements.txt`  

---

## ⚙ Быстрый запуск

Ниже шаги, чтобы запустить проект локально.

1. Склонируй репозиторий  
   ```bash
   git clone https://github.com/DanilaYukin/Learning_platform.git
   cd Learning_platform
   ```
2. Создай и активируй виртуальное окружение
   ```bash
   python -m venv venv
   source venv/bin/activate       # на Unix / MacOS
   venv\Scripts\activate.bat      # на Windows
   ```
3. Установи зависимости
   ```bash
   pip install -r requirements.txt
   ```
4. Сделай миграции и примените их
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ``` 
5. Запусти сервер разработки
   ```bash
   python manage.py runserver
   ```
   
## Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE)