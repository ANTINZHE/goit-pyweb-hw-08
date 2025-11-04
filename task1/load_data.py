# load_data.py
import os
import json
import sys
from mongoengine import connect, NotUniqueError
from models import Author, Quote
from dotenv import load_dotenv

# ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

MONGODB_URI = os.environ.get("MONGODB_URI")
if not MONGODB_URI:
    raise SystemExit(1)

# connect to MongoDB using mongoengine
connect(host=MONGODB_URI)

def load_authors(path="authors.json", drop_existing=False):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if drop_existing:
        Author.drop_collection()
        print("Колекцію authors очищено.")

    count = 0
    for item in data:
        fullname = item.get("fullname")
        try:
            author = Author(
                fullname=fullname,
                born_date=item.get("born_date"),
                born_location=item.get("born_location"),
                description=item.get("description")
            )
            author.save()
            count += 1
        except NotUniqueError:
            # якщо вже є, оновимо
            author = Author.objects(fullname=fullname).first()
            if author:
                author.update(
                    born_date=item.get("born_date"),
                    born_location=item.get("born_location"),
                    description=item.get("description")
                )
    print(f"Завантажено / оновлено авторів: {count}")

def load_quotes(path="qoutes.json", drop_existing=False):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if drop_existing:
        Quote.drop_collection()
        print("Колекцію quotes очищено.")

    count = 0
    for item in data:
        author_name = item.get("author")
        author = Author.objects(fullname=author_name).first()
        if not author:
            print(f"Попередження: автор '{author_name}' не знайдений у колекції authors. Створюю пустий запис автора.")
            author = Author(fullname=author_name).save()

        q = Quote(
            author=author,
            quote=item.get("quote"),
            tags=item.get("tags", [])
        )
        q.save()
        count += 1
    print(f"Завантажено цитат: {count}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Завантажити authors.json і qoutes.json в MongoDB через mongoengine.")
    parser.add_argument("--authors", default="authors.json", help="Шлях до файлу authors.json")
    parser.add_argument("--quotes", default="qoutes.json", help="Шлях до файлу qoutes.json")
    parser.add_argument("--drop", action="store_true", help="Очистити колекції перед завантаженням")
    args = parser.parse_args()

    load_authors(args.authors, drop_existing=args.drop)
    load_quotes(args.quotes, drop_existing=args.drop)
    print("Завантаження завершено.")
