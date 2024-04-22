
# Flower Manager

## Overview

**Flower Manager** streamlines inventory management for florists preparing for rapid Dutch flower auctions. This essential tool enables users to create detailed inventory reports on a tablet while in the warehouse, identifying flowers that are in low stock. These reports can then be conveniently accessed and searched on a PC, allowing users to efficiently plan which flowers to bid on at auctions. Simplify your inventory process and ensure you never miss an opportunity at the auctions with Flower Manager.
## Features

- **Inventory Tracking**: Use your tablet to walk through the warehouse, mark stock levels for low stock flowers, and finalize reports with custom notes.
- **Dynamic Search and Reports**: Access reports on your PC, input search queries to see which flowers are currently in demand at auctions, and adjust flower visibility in reports.
- **Visual Management**: Add colors using HEX codes or images for each flower type for better management and visual appeal. Each flower can be activated or deactivated, added, edited, or deleted.
- **Order Management**: Includes a basic order management system that allows for managing flower deliveries, complete with search functionality and separate color tagging for each order.
- **Customizable Report Ordering**: Control the display order of flowers in reports to match your workflow needs.



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