import os
import shutil
from datetime import datetime, timedelta
import asyncio


def delete_old_files(upload_dir: str, days_old: int = 30):
    """
    Удаляет файлы, которые были созданы более days_old дней назад
    """
    cutoff_time = datetime.now() - timedelta(days=days_old)

    for root, dirs, files in os.walk(upload_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))

            if file_time < cutoff_time:
                try:
                    os.remove(file_path)
                    if not os.listdir(root):
                        shutil.rmtree(root)
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")


async def periodic_cleanup():
    while True:
        delete_old_files("uploads")
        await asyncio.sleep(24 * 60 * 60)
