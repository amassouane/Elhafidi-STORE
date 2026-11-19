# ELHAFIDI STORE — Streetwear E-Commerce Platform

ELHAFIDI STORE is a full-stack e-commerce web application for a streetwear brand, built with **Flask**, **SQLAlchemy** and **SQLite**. It provides a complete customer storefront (catalog, filters, product pages, cart and Cash-on-Delivery checkout) together with a protected **admin panel** to manage products, stock and orders.

The user interface is in French and prices are in **MAD (Moroccan Dirham)**.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Data Model](#data-model)
- [Routes](#routes)
- [Business Rules](#business-rules)
- [Installation](#installation)
- [Configuration](#configuration)
- [Admin Access](#admin-access)
- [Security Notes](#security-notes)
- [Author](#author)

---

## Features

### Customer storefront
- **Home page**: hero banner, *Nouveautés* (4 latest products), *Shop by category* section, and featured products ("Collection Hiver").
- **Shop / catalog** (`/shop`):
  - Filter by **category**: Jackets, T-Shirts, Hoodies, Espadrilles, Pantalons, Parfums, Casquettes.
  - Filter by **size** (S, M, L, XL, XXL, shoe sizes, etc.).
  - Sort by **newest**, **price ascending** or **price descending**.
  - **Pagination** (12 products per page).
- **Product detail page**: images, description, price, stock, size and color selection, quantity, and a "Vous aimerez aussi" section with similar products from the same category.
- **Shopping cart**, stored in the session (no customer account needed):
  - Add products with a specific size and color. Each size/color combination is its own cart line.
  - Update quantities or remove items.
  - Live cart counter in the navbar.
  - Order summary with subtotal, shipping and grand total.
- **Checkout**: billing form (name, email, phone, address, city) and **Cash on Delivery** payment.
- **Light / dark theme** toggle, saved in `localStorage`.
- **Responsive design** with a mobile slide-in menu.
- Flash messages that close on click or disappear after 5 seconds.

### Admin panel (`/admin`)
- **Login** with Flask-Login (passwords hashed with Werkzeug).
- **Dashboard** showing:
  - Revenue (sum of orders with status *Livrée*)
  - Total orders
  - Number of products
  - The 5 most recent orders
- **Product management**:
  - List all products.
  - Add products: name, description, price, category, stock, sizes, colors, image upload, and a "featured" flag.
  - Update stock inline.
  - Delete products.
- **Order management**:
  - List all orders with customer details.
  - Change order status: `En attente` → `Confirmée` → `Livrée` / `Annulée`.

---

## Tech Stack

| Layer      | Technology |
|------------|------------|
| Backend    | Python 3, Flask 3.0 (Blueprints, application factory) |
| ORM / DB   | Flask-SQLAlchemy 3.1, SQLite |
| Auth       | Flask-Login 0.6, Werkzeug password hashing |
| Config     | python-dotenv (`.env` file) |
| Mail (configured) | Flask-Mail |
| Images     | Pillow, uploads to `static/images` (16 MB maximum) |
| Frontend   | Jinja2 templates, Vanilla CSS (CSS variables for theming), Vanilla JavaScript |
| UI assets  | Google Fonts (Bebas Neue, Poppins), Font Awesome 6 |

---

## Project Structure

```
elhafidi_store/
├── app.py                  # Application factory, Flask-Login setup, blueprint registration
├── config.py               # Configuration (secret key, database URI, mail, uploads)
├── models.py               # SQLAlchemy models: Admin, Product, Order, OrderItem
├── seed.py                 # Resets the database and loads the admin account and demo products
├── requirements.txt        # Python dependencies
├── .env.example            # Template for environment variables
├── routes/
│   ├── main.py             # Home page
│   ├── shop.py             # Catalog (filters, sorting, pagination) and product detail
│   ├── cart.py             # Session cart and checkout / order creation
│   ├── auth.py             # Admin login / logout
│   └── admin.py            # Dashboard, product CRUD, stock and order status
├── templates/
│   ├── base.html           # Layout: navbar, mobile menu, flash messages, footer
│   ├── index.html          # Home page
│   ├── shop.html           # Catalog with filters
│   ├── product_detail.html # Product page
│   ├── cart.html           # Cart
│   ├── checkout.html       # Checkout form
│   ├── auth/login.html     # Admin login
│   └── admin/
│       ├── dashboard.html
│       ├── manage_products.html
│       ├── add_product.html
│       └── manage_orders.html
└── static/
    ├── css/style.css       # Full theme (dark by default, light mode, responsive)
    ├── js/main.js          # Mobile menu, flash messages, theme toggle
    └── images/             # Uploaded product images (created automatically)
```

---

## Data Model

| Model       | Main fields |
|-------------|-------------|
| `Admin`     | `id`, `username` (unique), `password_hash` |
| `Product`   | `id`, `name`, `description`, `price`, `category`, `sizes` (JSON list), `colors` (JSON list), `stock`, `image_url`, `is_featured`, `created_at` |
| `Order`     | `id`, `customer_name`, `customer_email`, `customer_phone`, `customer_address`, `customer_city`, `total_price`, `payment_method` (default *Cash on Delivery*), `status` (default *En attente*), `created_at` |
| `OrderItem` | `id`, `order_id` → `Order`, `product_id` → `Product`, `quantity`, `size`, `color`, `unit_price` |

`Order` 1 ── * `OrderItem` * ── 1 `Product`

---

## Routes

### Public
| Method   | URL | Description |
|----------|-----|-------------|
| GET      | `/` | Home page |
| GET      | `/shop?category=&size=&sort=&page=` | Catalog with filters (`sort` = `newest`, `price_asc` or `price_desc`) |
| GET      | `/product/<id>` | Product detail |
| GET      | `/cart` | View cart |
| POST     | `/cart/add/<product_id>` | Add to cart (`quantity`, `size`, `color`) |
| POST     | `/cart/update/<cart_key>` | Update quantity (0 removes the line) |
| POST     | `/cart/remove/<cart_key>` | Remove a line |
| GET/POST | `/checkout` | Checkout form / place the order |

### Authentication
| Method   | URL | Description |
|----------|-----|-------------|
| GET/POST | `/auth/login` | Admin login |
| GET      | `/auth/logout` | Logout |

### Admin (login required)
| Method   | URL | Description |
|----------|-----|-------------|
| GET      | `/admin/` | Dashboard |
| GET      | `/admin/products` | Product list |
| GET/POST | `/admin/product/add` | Add a product |
| POST     | `/admin/product/update_stock/<id>` | Update stock |
| POST     | `/admin/product/delete/<id>` | Delete a product |
| GET      | `/admin/orders` | Order list |
| POST     | `/admin/order/update_status/<id>` | Change order status |

---

## Business Rules

- **Shipping**: 50 MAD for orders under 500 MAD. Shipping is free from 500 MAD.
- **Payment**: Cash on Delivery only.
- **Order statuses**: `En attente` (default), `Confirmée`, `Livrée`, `Annulée`.
- **Revenue** on the dashboard counts only orders with status `Livrée`.
- After checkout, the cart is cleared and the customer is sent back to the home page with a confirmation message.

---

## Installation

**Requirements:** Python 3.10 or newer, and pip.

1. **Clone the repository**
   ```bash
   git clone https://github.com/amassouane/Elhafidi-STORE.git
   cd Elhafidi-STORE
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install the dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create your `.env` file**
   ```bash
   cp .env.example .env      # Windows: copy .env.example .env
   ```
   Then edit `.env` and set your own `SECRET_KEY` (see [Configuration](#configuration)).

5. **Initialize the database with demo data**
   ```bash
   python seed.py
   ```
   This **drops and recreates** all tables. It then creates an admin account and 12 demo products across all categories.

6. **Start the development server**
   ```bash
   python app.py
   ```
   Open <http://127.0.0.1:5000> in your browser.

---

## Configuration

Settings are read from `.env` by `config.py`:

| Variable        | Description | Default |
|-----------------|-------------|---------|
| `SECRET_KEY`    | Flask secret key (signs sessions and the cart) | `default-secret-key-123` (**change it**) |
| `DATABASE_URI`  | SQLAlchemy database URI | `sqlite:///elhafidi_store.db` |
| `MAIL_SERVER`   | SMTP server | — |
| `MAIL_PORT`     | SMTP port | `587` |
| `MAIL_USE_TLS`  | Enable TLS when set | — |
| `MAIL_USERNAME` | SMTP username | — |
| `MAIL_PASSWORD` | SMTP password | — |

---

## Admin Access

- URL: <http://127.0.0.1:5000/admin>
- Demo credentials (created by `seed.py`): **`admin` / `admin123`**

> Change these credentials before deploying the application anywhere public.

---

## Security Notes

- Never commit your `.env` file. It is excluded by `.gitignore`.
- Use a long, random `SECRET_KEY` in production.
- `app.py` runs with `debug=True`, which is for development only. Use a WSGI server (such as Gunicorn or Waitress) in production.
- Replace the demo admin password after seeding.

---

## Author

**amassouane** — [GitHub](https://github.com/amassouane)
