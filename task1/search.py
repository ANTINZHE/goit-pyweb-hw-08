# search.py
import os
import sys
from mongoengine import connect, Q
from models import Author, Quote
from dotenv import load_dotenv

# ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()
MONGODB_URI = os.environ.get("MONGODB_URI")
if not MONGODB_URI:
    print("Помилка: змінна оточення MONGODB_URI не встановлена.")
    raise SystemExit(1)

connect(host=MONGODB_URI)

def print_quote(q):
    # q is Quote Document
    print("—" * 60)
    # author fullname
    try:
        author_name = q.author.fullname if q.author else "Unknown"
    except Exception:
        author_name = "Unknown"
    print(f"Автор: {author_name}")
    print(f"Цитата: {q.quote}")
    print(f"Теги: {', '.join(q.tags)}")

def find_by_name(value):
    # точне співпадіння повного імені
    authors = Author.objects(fullname__iexact=value)
    if not authors:
        print(f"Автор з ім'ям '{value}' не знайдений.")
        return []
    quotes = Quote.objects(author__in=authors)
    return list(quotes)

def find_by_tag(value):
    # знайти цитати, де tags містить цей тег (case-insensitive)
    tag = value.strip()
    quotes = Quote.objects(tags__icontains=tag)
    return list(quotes)

def find_by_tags(values_csv):
    # values_csv: 'life,live' — означає OR: life OR live
    tags = [t.strip() for t in values_csv.split(",") if t.strip()]
    if not tags:
        return []
    # побудуємо Q-запит: tags__icontains=tag1 OR tags__icontains=tag2 ...
    query = Q()
    for t in tags:
        query |= Q(tags__icontains=t)
    quotes = Quote.objects(query)
    return list(quotes)

def main_loop():
    print("Пошук цитат. Введіть команду у форматі команда:значення (приклад: name: Steve Martin).")
    print("Підтримувані команди: name, tag, tags, exit")
    while True:
        try:
            raw = input(">>> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nВихід.")
            break
        if not raw:
            continue

        if raw.lower() == "exit":
            print("Вихід.")
            break

        if ":" not in raw:
            print("Невірний формат. Повинно бути команда:значення")
            continue

        cmd, val = raw.split(":", 1)
        cmd = cmd.strip().lower()
        val = val.strip()
        if not val:
            print("Значення порожнє.")
            continue

        if cmd == "name":
            results = find_by_name(val)
        elif cmd == "tag":
            results = find_by_tag(val)
        elif cmd == "tags":
            results = find_by_tags(val)
        else:
            print("Невідома команда. Використовуйте name, tag, tags або exit.")
            continue

        if not results:
            print("Результатів не знайдено.")
            continue

        for q in results:
            print_quote(q)
        print(f"\nЗнайдено {len(results)} результат(ів).")

if __name__ == "__main__":
    main_loop()
