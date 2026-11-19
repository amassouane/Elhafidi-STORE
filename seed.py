import os
from flask import Flask
from werkzeug.security import generate_password_hash
from app import create_app
from models import db, Admin, Product

app = create_app()

def seed_database():
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()

        print("Creating admin user...")
        admin = Admin(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)

        print("Creating dummy products...")
        
        products = [
            # Jackets
            Product(
                name="Veste Aviator Classic", description="Veste streetwear coupe aviateur premium.", price=850.0, category="Jackets", stock=15, is_featured=True,
                sizes='["S","M","L","XL"]', colors='["Noir","Kaki"]', image_url="https://images.unsplash.com/photo-1551028719-00167b16eac5?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80"
            ),
            Product(
                name="Polaire Oversize", description="Veste polaire ultra chaude.", price=450.0, category="Jackets", stock=10,
                sizes='["S","M","L","XL"]', colors='["Beige","Noir"]', image_url="https://images.unsplash.com/photo-1559551409-d2222d32ce78?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80"
            ),
            
            # T-Shirts
            Product(
                name="T-Shirt Boxy Fit Logo", description="T-shirt coupe boxy avec logo discret.", price=200.0, category="T-Shirts", stock=50, is_featured=True,
                sizes='["S","M","L","XL","XXL"]', colors='["Blanc","Noir"]', image_url="https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80"
            ),
            Product(
                name="T-Shirt Graphique Tokyo", description="T-shirt imprimé style japonais.", price=250.0, category="T-Shirts", stock=30,
                sizes='["M","L","XL"]', colors='["Noir"]', image_url="https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80"
            ),
            
            # Hoodies
            Product(
                name="Hoodie Essential Heavyweight", description="Hoodie épais 400gsm.", price=550.0, category="Hoodies", stock=25, is_featured=True,
                sizes='["S","M","L","XL"]', colors='["Gris chiné","Noir"]', image_url="https://images.unsplash.com/photo-1556821840-3a63f95609a7?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80"
            ),
            Product(
                name="Hoodie Zip Y2K", description="Hoodie zippé coupe courte.", price=480.0, category="Hoodies", stock=15,
                sizes='["S","M"]', colors='["Noir","Rouge"]', image_url="https://images.unsplash.com/photo-1509942774463-acf339cf87d5?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80"
            ),

            # Espadrilles
            Product(
                name="Sneakers Chunky Cloud", description="Baskets semelle épaisse.", price=890.0, category="Espadrilles", stock=40,
                sizes='["40","41","42","43","44"]', colors='["Blanc"]', image_url="https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80"
            ),
            Product(
                name="Retro Runner 90s", description="Espadrilles style vintage.", price=750.0, category="Espadrilles", stock=20,
                sizes='["41","42","43"]', colors='["Noir","Gris"]', image_url="https://images.unsplash.com/photo-1608231387042-66d1773070a5?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80"
            ),
            
            # Pantalons
            Product(
                name="Cargo Pants Utility", description="Pantalon cargo multi-poches.", price=450.0, category="Pantalons", stock=30, is_featured=True,
                sizes='["S","M","L"]', colors='["Kaki","Noir"]', image_url="https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80"
            ),
            Product(
                name="Baggy Jeans", description="Jeans coupe ultra large.", price=500.0, category="Pantalons", stock=25,
                sizes='["M","L","XL"]', colors='["Bleu clair","Gris"]', image_url="https://images.unsplash.com/photo-1542272201-b1ca555f8505?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80"
            ),

            # Parfums
            Product(
                name="Oud Mystik", description="Parfum oriental intense 50ml.", price=600.0, category="Parfums", stock=50,
                sizes='["50ml"]', colors='[]', image_url="https://images.unsplash.com/photo-1585386959984-a4155224a1ad?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80"
            ),
            
            # Casquettes
            Product(
                name="Casquette Trucker Logo", description="Casquette ajustable.", price=150.0, category="Casquettes", stock=60,
                sizes='["Unique"]', colors='["Noir","Rouge"]', image_url="https://images.unsplash.com/photo-1588850561407-ed78c282e89b?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80"
            )
        ]

        db.session.add_all(products)
        db.session.commit()
        print("Database seeded successfully with admin account and products!")
        print("Admin credentials -> Username: admin | Password: admin123")

if __name__ == '__main__':
    seed_database()
