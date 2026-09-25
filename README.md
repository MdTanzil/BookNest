# 📚 BookNest

BookNest is a robust, full-featured E-commerce platform built with Python and Django designed for selling books online. It includes features for book classification, user account profiles, order lifecycle fulfillment, customer reviews, a shopping cart workflow, and a user wishlist system.

## 🗂️ Project Architecture

The application is modularized into several dedicated Django apps to ensure strict separation of concerns:

- **`config`**: Project configurations and routing engine settings.
- **`accounts`**: User authorization, customer registration, and secure profile systems.
- **`books`**: Core catalog tracking categories, authors, books, and image galleries.
- **`cart`**: Shopping session engine handling product counts and checkout staging.
- **`orders`**: Transaction management and shipment pipeline tracking.
- **`reviews`**: Community interaction framework powering book ratings and feedback.
- **`wishlist`**: Saved items layer enabling personal book collections for future purchases.
- **`core`**: Base templates, context processors, and shared structural layouts.

---

## 🚀 Getting Started

Follow these instructions to set up the development environment locally on your machine.

### Prerequisites
- Python 3.11+
- Git

### Installation & Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd BookNest
   ```

2. **Initialize the Virtual Environment:**
   Create an isolated environment using `virtualenv`:
   ```bash
   python -m virtualenv .env
   ```

3. **Activate the Environment:**
   - **Windows (PowerShell):**
     ```powershell
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
     .\.env\Scripts\activate.ps1
     ```
   - **Mac / Linux (Bash/Zsh):**
     ```bash
     source .env/bin/activate
     ```

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run Database Migrations:**
   Generate tables and sync configurations across all apps:
   ```bash
   python manage.py makemigrations accounts books cart core orders reviews wishlist
   python manage.py migrate
   ```

6. **Create a Superuser Account:**
   Set up your administrator dashboard access credentials:
   ```bash
   python manage.py createsuperuser
   ```

7. **Launch the Server:**
   ```bash
   python manage.py runserver
   ```
   Open your browser and navigate to `http://127.0.0.1:8000/` to explore the store.

---

## 🛠️ Built With

- **Backend Framework**: [Django](https://djangoproject.com) (Python)
- **Database Engine**: SQLite (Default development database)
- **Styling Architecture**: HTML5 / CSS3 / JavaScript

---

## 📄 License

This project is open-source software licensed under the [MIT License](LICENSE).
