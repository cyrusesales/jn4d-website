# JN4D Interior Design Services

### Django E-Commerce Web Application

An e-commerce web application for **JN4D Interior Design Services**, a home decor business specializing in blinds, curtains, sail shades, and related interior design products.

The application is being developed using Django and Python for the backend, PostgreSQL for data storage, and HTML, CSS, and JavaScript for the frontend.

The goal is to provide customers with an online platform to explore home decor products while allowing administrators to manage product catalogs, inventory, and customer orders.

> 🚧 This project is currently under development.

---

## 📌 Project Overview

JN4D Interior Design Services is a web-based e-commerce project focused on home decor products.

The application aims to provide a convenient shopping experience for customers and an organized management system for administrators.

This project also serves as a practical portfolio demonstrating my experience with Django backend development, database relationships, CRUD operations, authentication, and e-commerce business logic.

## ✨ Features

### Customer Features

- User registration and authentication
- Customer profile management
- Product catalog
- Product details and product images
- Product variations such as sizes and colors
- Shopping cart management
- Add and update cart items
- Wishlist functionality
- Product search
- Order management
- Responsive user interface

### Admin Features

- Product management
- Category management
- Inventory management
- Product size and color management
- Multiple product image uploads
- Customer profile management
- Order management
- Search and pagination
- Order status management

*Features are being implemented and refined as development progresses.*

## 🛠️ Tech Stack

| Technology | Description |
|---|---|
| Python | Backend programming language |
| Django | Backend web framework |
| PostgreSQL | Relational database |
| HTML5 | Web page structure |
| CSS3 | Styling and responsive design |
| JavaScript | Frontend interactivity |
| Bootstrap | Responsive UI components |
| Django ORM | Database queries and relationships |
| Git | Version control |
| GitHub | Source code repository |

## 🗄️ Database and Backend

The application uses Django models and PostgreSQL to manage its data.

The database includes entities for managing:

- Users and user profiles
- Products and categories
- Product sizes and variations
- Product inventory
- Shopping cart items
- Customer orders
- Wishlist items

The backend uses Django's Model-View-Template (MVT) architecture to handle application logic, database operations, and rendering of dynamic web pages.

## 📂 Project Structure

```text
jn4d-website/
│
├── jn4dwebsite/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
├── README.md
└── requirements.txt
```

*The structure above is a simplified overview. Additional application folders, templates, static files, and media directories may be present in the repository.*

## 🚀 Installation and Setup

### Prerequisites

- Python 3.x
- PostgreSQL
- pip
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/cyrusesales/jn4d-website.git
```

Navigate to the project directory:

```bash
cd jn4d-website
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment.

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Configure your PostgreSQL database in Django's `settings.py`.

Example:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Replace the example values with your local database credentials.

### 5. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser

```bash
python manage.py createsuperuser
```

### 7. Start the Development Server

```bash
python manage.py runserver
```

Open the application:

http://127.0.0.1:8000/

## 📸 Screenshots

Screenshots of the application will be added here as development progresses.

### Homepage

<img width="1887" height="857" alt="image" src="https://github.com/user-attachments/assets/e760298e-39dd-4a01-8203-f3bd71f321d3" />


### Product Catalog

<img width="1882" height="857" alt="image" src="https://github.com/user-attachments/assets/d6347617-b305-49b9-a744-72dcbb89b1be" />


### Shopping Cart

<img width="1886" height="857" alt="image" src="https://github.com/user-attachments/assets/0fe0c4fa-49d1-47aa-b45c-1a3e31675d50" />


### Admin Inventory Management

<!-- Add your inventory management screenshot here -->

## 🎯 Development Goals

This project demonstrates my practical experience with:

- Developing web applications using Django
- Designing relational database models
- Implementing CRUD operations
- Working with Django ORM and querysets
- Implementing authentication and authorization
- Handling image uploads
- Implementing search and pagination
- Managing shopping cart and order workflows
- Building responsive web interfaces
- Debugging and improving backend functionality

## 🔮 Future Improvements

Planned improvements include:

- Payment gateway integration
- Product reviews and ratings
- Email notifications
- Advanced product filtering and sorting
- REST API development using Django REST Framework
- Automated testing
- Application deployment
- Improved security and performance

## 👨‍💻 Developer

Developed by **Cyrus Sales**

GitHub: [@cyrusesales](https://github.com/cyrusesales)

This project is part of my ongoing journey in Python and Django backend development.

## 📄 License

This project is currently intended for portfolio and learning purposes.


