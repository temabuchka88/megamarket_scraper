# Megamarket parser

Этот проект представляет собой парсер магазина Megamarket, написанного на Python с использованием библиотеки `Selenium`.

## Установка через git

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/temabuchka88/megamarket_scraper.git
   cd megamarket_scraper

2. **Запустите программу с помощью Docker Compose:**

    docker compose up --build -d

3. **Ожидайте выполнение программы**

4. **Результаты выполнения будут находиться в файле goods.xlsx **

## Установка через DockerHub

1. **Установите Docker**

2. **Получите Docker-образ**
    Выполните следующую команду в терминале, чтобы загрузить образ с DockerHub:

    docker pull temabuchka88/megamarket_scraperr:latest

3. **Запустите контейнер:**
    Выполните следующую команду в терминале:

    docker run -d --name megamarket_scraper -v $(pwd)/output:/app/output temabuchka88/megamarket_scraper:latest

4. **Ожидайте выполнение программы**

5. **Результаты выполнения будут находиться в файле goods.xlsx **