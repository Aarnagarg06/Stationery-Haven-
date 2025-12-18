# data.py
import db

def seed_demo_data():
    existing = db.get_all_products()
    if existing:
        return

    stationery_items = [
        ("A4 Paper Ream", 320, 150),
        ("Ball Pen Blue", 10, 500),
        ("Ball Pen Black", 10, 450),
        ("Gel Pen", 25, 300),
        ("HB Pencil", 8, 600),
        ("Eraser", 5, 400),
        ("Sharpener", 7, 350),
        ("Notebook Single Line", 45, 250),
        ("Notebook Double Line", 50, 220),
        ("Notebook Plain", 40, 200),
        ("Sticky Notes", 35, 180),
        ("Highlighter", 60, 120),
        ("Whiteboard Marker", 55, 140),
        ("Permanent Marker", 65, 110),
        ("Plastic File", 25, 300),
        ("Office File Folder", 30, 260),
        ("Exam Pad", 90, 100),
        ("Drawing Book", 70, 130),
        ("Sketch Pen Set", 120, 90),
        ("Crayons Box", 85, 95),
        ("Geometry Box", 150, 80),
        ("Stapler", 180, 60),
        ("Stapler Pins", 40, 200),
        ("Glue Stick", 25, 160),
        ("Correction Pen", 35, 140),
        ("Calculator Basic", 450, 45),
        ("Calculator Scientific", 1200, 30)
    ]

    for item in stationery_items:
        db.insert_product(*item)

