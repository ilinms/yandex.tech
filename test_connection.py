from config import DISK_OAUTH_TOKEN
from src.api_client import YandexDiskClient

print("=" * 50)
print("🔍 Проверка подключения к Яндекс.Диску")
print("=" * 50)

if not DISK_OAUTH_TOKEN:
    print("❌ ОШИБКА: Токен не найден в .env файле!")
    print("   Убедитесь, что в .env нет пробелов вокруг '='")
    print("   Пример правильного формата: DISK_OAUTH_TOKEN=ваш_токен")
    exit(1)

print(f"✅ Токен найден: {DISK_OAUTH_TOKEN[:10]}...")
print(f"🌐 Base URL: {DISK_OAUTH_TOKEN}")

try:
    client = YandexDiskClient(oauth_token=DISK_OAUTH_TOKEN)
    info = client.get_disk_info()
    print(f"✅ Успешно подключено к диску!")
    print(f"   Всего места: {info.get('total_space', 'N/A') / 1024**3:.2f} ГБ")
    print(f"   Использовано: {info.get('used_space', 'N/A') / 1024**3:.2f} ГБ")
except Exception as e:
    print(f"❌ ОШИБКА подключения: {type(e).__name__}: {e}")
    print("\nВозможные причины:")
    print("  1. Неверный/просроченный токен")
    print("  2. Нет доступа к API (проверьте права приложения)")
    print("  3. Проблемы с сетью")
    exit(1)

print("=" * 50)
print("🎉 Всё работает! Можно переходить к тестам.")
print("=" * 50)