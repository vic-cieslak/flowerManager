
# Flower Manager

## Overview

**Flower Manager** streamlines inventory management for florists preparing for rapid Dutch flower auctions. This essential tool enables users to create detailed inventory reports on a tablet while in the warehouse, identifying flowers that are in low stock. These reports can then be conveniently accessed and searched on a PC, allowing users to efficiently plan which flowers to bid on at auctions. Simplify your inventory process and ensure you never miss an opportunity at the auctions, say goodbye to manual spreadsheets and handwritten notes.

Note:

Project is POC built with Django and Vuejs for dynamic bits. 

## Features

- **Inventory Tracking**: Use your tablet to walk through the warehouse, mark stock levels for low stock flowers and add notes.
- **Dynamic Search and Reports**: Access reports on your PC, input search queries to see which flowers are you interested in bidding on.
- **Visual Management**: Add colors using HEX codes or images for each flower type for better management and visual appeal. Each flower can be activated or deactivated, added, edited, or deleted.
- **Customizable Report Ordering**: Control the display order of flowers in reports to match your workflow needs.
- **Order Management**: Includes a basic order management system that allows for managing flower deliveries, complete with search functionality and separate color tagging for each order.

## Features Demo

- **Flower management (overview + search)**


https://github.com/vic-developer/flowerManager/assets/11517372/6f0e9739-3963-4929-b4d7-a9f8e8e3dc05



- **Add flowers, colors and variations**


https://github.com/vic-developer/flowerManager/assets/11517372/8827b372-a5fa-4e7c-b552-bfe313d8030e


- **Edit flowers**


https://github.com/vic-developer/flowerManager/assets/11517372/a354d668-6cba-4665-b236-dc01d511cf09


- **Start report (tablet view)**



[start-report.webm](https://github.com/vic-developer/flowerManager/assets/11517372/9dcde6f6-71a3-451a-b5c8-0cbd23ae6404)



- **Read report**


[read-report.webm](https://github.com/vic-developer/flowerManager/assets/11517372/fcd8800f-f036-47d1-8a23-62a8c35d3941)




- **Color management**


[Screencast from 2024-04-23 08-29-41.webm](https://github.com/vic-developer/flowerManager/assets/11517372/6acbc234-b569-41f6-8691-e2e8a2daf679)



- **Change order of flowers in report**


[Screencast from 2024-04-23 08-30-28.webm](https://github.com/vic-developer/flowerManager/assets/11517372/4427e75f-2378-4233-b93a-24fb0716871a)



- **Order manager list**

[Screencast from 2024-04-23 08-31-22.webm](https://github.com/vic-developer/flowerManager/assets/11517372/aa336e88-f095-48de-b185-3401a6aa2666)



- **Add new order**


[Screencast from 2024-04-23 08-31-47.webm](https://github.com/vic-developer/flowerManager/assets/11517372/8f68bddf-50bf-422b-9ec8-16e5ecb16204)



## Installation

### Prerequisites
Make sure Docker and Docker Compose are installed on your system.

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
   
2. Create a `.env` file and populate it with your environment variables:
   ```plaintext
   DEBUG=False
   POSTGRES_USER=test
   POSTGRES_PASSWORD=test
   POSTGRES_DB=hello
   ```

3. Launch the application using Docker Compose:
   ```bash
   docker-compose up --build -d
   ```

4. Import an example database:
   ```bash
   # List running containers to find the PostgreSQL container ID
   docker ps
   # Copy the SQL dump to the container
   docker cp dump_23-03-2024_18_04_55.sql CONTAINER_ID:/
   # Execute the SQL dump
   docker exec -it CONTAINER_ID /bin/bash
   psql -U test -d hello -f dump_23-03-2024_18_04_55.sql
   ```

5. Restart the Docker containers:
   ```bash
   docker-compose restart
   ```

6. Access the web container at 127.0.0.1:5085

---

## Manual Build / Development Setup

1. Download the Code

Clone the repository and navigate into the directory:
```bash
git clone <repository-url>
cd <repository-directory>
```

 2. Install Node Modules

Install the necessary Node.js modules:
```bash
npm install
npm run build
```

 3. Set Up Django Environment

Set up and activate a virtual environment, and install the required Python packages:
```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

 4. Configure Local Database

Modify the `settings.py` to set SQLite as the local database:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

 5. Install Tailwind CSS and Flowbite

In a separate terminal, install and run Tailwind CSS with Flowbite:
```bash
npm install
npm run dev        
```

 6. Database Migration

Migrate the database schema:
```bash
python manage.py makemigrations
python manage.py migrate
```

 7. Start the Application

Create an administrative user and start the Django server:
```bash
python manage.py createsuperuser # Follow the prompts to create the admin user
python manage.py runserver       # The server will start at http://127.0.0.1:5085/
```

## Localization

Currently available in Polish. We plan to support additional languages based on user demand. Contact us if you need assistance with translation or want to request additional languages.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request with your enhancements.

## Support

For support, please open an issue on the GitHub project page.


## Credit

Based on excelent:

https://rocket-django.onrender.com
https://github.com/app-generator/rocket-django
