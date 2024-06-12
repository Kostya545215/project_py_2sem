import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('физика.db')

# Создание курсора
cursor = conn.cursor()

# Очистка всех записей в таблице 'your_table'
cursor.execute("DELETE FROM задачи")

# Сохранение изменений
conn.commit()

# Закрытие соединения
conn.close()
 
