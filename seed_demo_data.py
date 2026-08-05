import asyncio
from decimal import Decimal
from sqlalchemy import select
from app.database.session import AsyncSessionLocal
from app.models.category import Category
from app.models.product import Product
from app.utils.slug import slugify

DEMO_CATEGORIES = [
    {
        "name": "Electronics & Tech",
        "description": "Latest consumer electronics, smart home tech, and entertainment gear.",
    },
    {
        "name": "Smartphones & Mobile",
        "description": "Top-tier smartphones, fast chargers, and mobile accessories.",
    },
    {
        "name": "Laptops & Computers",
        "description": "High-performance laptops, desktop workstations, and computer peripherals.",
    },
    {
        "name": "Audio & Sound",
        "description": "Premium noise-canceling headphones, earbuds, and wireless speakers.",
    },
    {
        "name": "Wearable Tech",
        "description": "Smartwatches, fitness trackers, and outdoor GPS watches.",
    },
    {
        "name": "Gaming & Gear",
        "description": "Next-gen consoles, mechanical keyboards, and gaming accessories.",
    },
    {
        "name": "Home Appliances",
        "description": "Smart home cleaning, coffee makers, and modern lifestyle appliances.",
    },
    {
        "name": "Fashion & Accessories",
        "description": "Premium leather backpacks, eyewear, and everyday carry essentials.",
    },
]

DEMO_PRODUCTS = [
    # Electronics & Tech
    {
        "title": "Sony WH-1000XM5 Wireless Noise-Canceling Headphones",
        "category_name": "Electronics & Tech",
        "description": "Industry-leading noise cancellation with two processors and 8 microphones. Magnificent sound quality engineered with the new Integrated Processor V1. Up to 30-hour battery life.",
        "price": Decimal("399.99"),
        "discount_price": Decimal("349.99"),
        "stock": 35,
        "is_available": True,
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop",
    },
    {
        "title": "Samsung 55\" Neo QLED 4K Smart TV",
        "category_name": "Electronics & Tech",
        "description": "Quantum Matrix Technology with Mini LEDs, Neural Quantum Processor 4K, Dolby Atmos audio, and Motion Xcelerator Turbo+ for smooth 120Hz gaming.",
        "price": Decimal("1299.99"),
        "discount_price": Decimal("1099.99"),
        "stock": 12,
        "is_available": True,
        "image_url": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=600&auto=format&fit=crop",
    },

    # Smartphones & Mobile
    {
        "title": "iPhone 15 Pro Max - 256GB Natural Titanium",
        "category_name": "Smartphones & Mobile",
        "description": "Forged in titanium with aerospace-grade strength. A17 Pro chip with 6-core GPU, customizable Action button, and 48MP main camera with 5x optical zoom.",
        "price": Decimal("1199.00"),
        "discount_price": Decimal("1149.00"),
        "stock": 20,
        "is_available": True,
        "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600&auto=format&fit=crop",
    },
    {
        "title": "Google Pixel 8 Pro - 128GB Obsidian",
        "category_name": "Smartphones & Mobile",
        "description": "Super Actua display, Google Tensor G3 chip, fully upgraded cameras with Best Take, Magic Editor, and up to 24-hour battery life with fast wireless charging.",
        "price": Decimal("999.00"),
        "discount_price": Decimal("849.00"),
        "stock": 18,
        "is_available": True,
        "image_url": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=600&auto=format&fit=crop",
    },
    {
        "title": "Anker Magnetic Wireless Power Bank 10,000mAh",
        "category_name": "Smartphones & Mobile",
        "description": "Ultra-slim 10,000mAh portable charger with MagSafe compatible magnetic wireless charging, built-in kickstand, and USB-C Power Delivery.",
        "price": Decimal("59.99"),
        "discount_price": Decimal("44.99"),
        "stock": 60,
        "is_available": True,
        "image_url": "https://images.unsplash.com/photo-1609592424109-dd9892f1b177?w=600&auto=format&fit=crop",
    },

    # Laptops & Computers
    {
        "title": "Apple MacBook Pro 16\" M3 Max - Space Black",
        "category_name": "Laptops & Computers",
        "description": "16-core CPU, 40-core GPU, 36GB Unified Memory, 1TB SSD. Liquid Retina XDR display with up to 1600 nits peak brightness and 22-hour battery life.",
        "price": Decimal("3499.00"),
        "discount_price": Decimal("3299.00"),
        "stock": 8,
        "is_available": True,
        "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&auto=format&fit=crop",
    },
    {
        "title": "Dell XPS 15 OLED Touchscreen Laptop",
        "category_name": "Laptops & Computers",
        "description": "13th Gen Intel Core i9-13900H, 32GB DDR5 RAM, 1TB PCIe NVMe SSD, NVIDIA GeForce RTX 4060 8GB graphics, 3.5K OLED InfinityEdge touch display.",
        "price": Decimal("2199.99"),
        "discount_price": Decimal("1949.99"),
        "stock": 14,
        "is_available": True,
        "image_url": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=600&auto=format&fit=crop",
    },
    {
        "title": "Logitech MX Master 3S Performance Wireless Mouse",
        "category_name": "Laptops & Computers",
        "description": "Quiet click switches, 8000 DPI track-on-glass sensor, MagSpeed electromagnetic scrolling, dual Bluetooth / Logi Bolt connectivity.",
        "price": Decimal("99.99"),
        "discount_price": Decimal("89.99"),
        "stock": 50,
        "is_available": True,
        "image_url": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=600&auto=format&fit=crop",
    },

    # Audio & Sound
    {
        "title": "Apple AirPods Pro (2nd Generation) USB-C",
        "category_name": "Audio & Sound",
        "description": "Up to 2x more Active Noise Cancellation, Adaptive Audio, Transparency mode, Personalized Spatial Audio with dynamic head tracking, MagSafe Case with Speaker.",
        "price": Decimal("249.00"),
        "discount_price": Decimal("199.00"),
        "stock": 40,
        "is_available": True,
        "image_url": "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=600&auto=format&fit=crop",
    },
    {
        "title": "Bose SoundLink Flex Portable Bluetooth Speaker",
        "category_name": "Audio & Sound",
        "description": "Rugged waterproof IP67 design, PositionIQ technology automatically optimizes sound quality, up to 12 hours playtime per charge.",
        "price": Decimal("149.00"),
        "discount_price": Decimal("129.00"),
        "stock": 25,
        "is_available": True,
        "image_url": "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=600&auto=format&fit=crop",
    },

    # Wearable Tech
    {
        "title": "Apple Watch Ultra 2 GPS + Cellular 49mm",
        "category_name": "Wearable Tech",
        "description": "Rugged titanium case, bright 3000-nit Always-On Retina display, S9 SiP with Double Tap gesture, precision dual-frequency GPS, 36-hour battery life.",
        "price": Decimal("799.00"),
        "discount_price": Decimal("749.00"),
        "stock": 15,
        "is_available": True,
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop",
    },
    {
        "title": "Garmin Fenix 7 Pro Solar Sapphire Multisport Watch",
        "category_name": "Wearable Tech",
        "description": "Power Sapphire solar charging lens, built-in LED flashlight, endurance score, real-time stamina tracking, preloaded TopoActive maps.",
        "price": Decimal("899.99"),
        "discount_price": Decimal("799.99"),
        "stock": 10,
        "is_available": True,
        "image_url": "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=600&auto=format&fit=crop",
    },

    # Gaming & Gear
    {
        "title": "Sony PlayStation 5 Digital Edition Console",
        "category_name": "Gaming & Gear",
        "description": "Ultra-high speed SSD, ray tracing, 4K TV gaming up to 120fps, Tempest 3D AudioTech, DualSense wireless controller with haptic feedback.",
        "price": Decimal("449.99"),
        "discount_price": Decimal("419.99"),
        "stock": 22,
        "is_available": True,
        "image_url": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=600&auto=format&fit=crop",
    },
    {
        "title": "Keychron Q1 Pro Wireless Custom Mechanical Keyboard",
        "category_name": "Gaming & Gear",
        "description": "75% layout full CNC aluminum body, QMK/VIA programmable, hot-swappable switches, double-gasket design with Bluetooth 5.1 & Type-C connection.",
        "price": Decimal("199.99"),
        "discount_price": Decimal("179.99"),
        "stock": 18,
        "is_available": True,
        "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&auto=format&fit=crop",
    },

    # Home Appliances
    {
        "title": "Dyson V15 Detect Cordless Vacuum Cleaner",
        "category_name": "Home Appliances",
        "description": "Laser reveals invisible dust on hard floors, piezo sensor counts and sizes particles, LCD screen displays real-time particle stats. Up to 60 min runtime.",
        "price": Decimal("749.99"),
        "discount_price": Decimal("649.99"),
        "stock": 9,
        "is_available": True,
        "image_url": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=600&auto=format&fit=crop",
    },
    {
        "title": "Nespresso VertuoPlus Coffee and Espresso Machine",
        "category_name": "Home Appliances",
        "description": "Centrifusion technology gently blends ground coffee with water at 7000 RPM for barista-quality coffee and espresso with luxurious crema.",
        "price": Decimal("169.00"),
        "discount_price": Decimal("139.00"),
        "stock": 30,
        "is_available": True,
        "image_url": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=600&auto=format&fit=crop",
    },

    # Fashion & Accessories
    {
        "title": "Minimalist Top-Grain Leather Backpack 15\"",
        "category_name": "Fashion & Accessories",
        "description": "Handcrafted premium full-grain Italian leather, padded 15-inch laptop compartment, weather-resistant YKK zippers, ergonomic shoulder straps.",
        "price": Decimal("189.00"),
        "discount_price": Decimal("159.00"),
        "stock": 35,
        "is_available": True,
        "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600&auto=format&fit=crop",
    },
    {
        "title": "Classic Wayfarer Polarized Sunglasses",
        "category_name": "Fashion & Accessories",
        "description": "Hand-polished acetate frame with scratch-resistant polarized polycarbonate lenses, 100% UV400 protection, lightweight and durable design.",
        "price": Decimal("89.00"),
        "discount_price": Decimal("69.00"),
        "stock": 50,
        "is_available": True,
        "image_url": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=600&auto=format&fit=crop",
    },
]

async def seed_data():
    async with AsyncSessionLocal() as db:
        print("🌱 Starting database seeding...")
        category_map = {}

        # 1. Seed Categories
        for cat_data in DEMO_CATEGORIES:
            slug = slugify(cat_data["name"])
            stmt = select(Category).where(Category.slug == slug)
            res = await db.execute(stmt)
            existing_cat = res.scalar_one_or_none()

            if existing_cat:
                category_map[cat_data["name"]] = existing_cat.id
                print(f"  ✓ Existing Category: {existing_cat.name} (ID: {existing_cat.id})")
            else:
                new_cat = Category(
                    name=cat_data["name"],
                    slug=slug,
                    description=cat_data["description"],
                    is_active=True
                )
                db.add(new_cat)
                await db.flush()
                category_map[cat_data["name"]] = new_cat.id
                print(f"  + Added Category: {new_cat.name} (ID: {new_cat.id})")

        # 2. Seed Products
        added_count = 0
        updated_count = 0

        for prod_data in DEMO_PRODUCTS:
            cat_name = prod_data["category_name"]
            cat_id = category_map.get(cat_name)
            if not cat_id:
                print(f"  ⚠️ Skipping product '{prod_data['title']}', category '{cat_name}' not found!")
                continue

            slug = slugify(prod_data["title"])
            stmt = select(Product).where(Product.slug == slug)
            res = await db.execute(stmt)
            existing_prod = res.scalar_one_or_none()

            if existing_prod:
                existing_prod.title = prod_data["title"]
                existing_prod.description = prod_data["description"]
                existing_prod.price = prod_data["price"]
                existing_prod.discount_price = prod_data["discount_price"]
                existing_prod.stock = prod_data["stock"]
                existing_prod.is_available = prod_data["is_available"]
                existing_prod.image_url = prod_data["image_url"]
                existing_prod.category_id = cat_id
                updated_count += 1
                print(f"  ↻ Updated Product: {existing_prod.title}")
            else:
                new_prod = Product(
                    title=prod_data["title"],
                    slug=slug,
                    description=prod_data["description"],
                    price=prod_data["price"],
                    discount_price=prod_data["discount_price"],
                    stock=prod_data["stock"],
                    is_available=prod_data["is_available"],
                    image_url=prod_data["image_url"],
                    category_id=cat_id
                )
                db.add(new_prod)
                added_count += 1
                print(f"  + Added Product: {new_prod.title}")

        await db.commit()
        print(f"\n✅ Seeding complete! Added {added_count} products, updated {updated_count} products across {len(category_map)} categories.")

if __name__ == "__main__":
    asyncio.run(seed_data())
