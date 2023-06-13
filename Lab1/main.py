import mysql.connector

# Підключення до бази даних
conn = mysql.connector.connect(
  host="дщсф",
  user="your_username",
  password="your_password",
  database="your_database"
)

# Створення таблиці students
cursor = conn.cursor()
cursor.execute("CREATE TABLE students (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), age INT, email VARCHAR(255))")

# Додавання студентів до таблиці students
students = [
  ('John Doe', 20, 'john@example.com'),
  ('Jane Smith', 22, 'jane@example.com'),
  ('David Johnson', 19, 'david@example.com'),
  ('Sarah Williams', 21, 'sarah@example.com'),
  ('Michael Brown', 23, 'michael@example.com')
]
cursor.executemany("INSERT INTO students (name, age, email) VALUES (%s, %s, %s)", students)

# Вибірка всіх студентів з таблиці students
cursor.execute("SELECT * FROM students")
all_students = cursor.fetchall()
for student in all_students:
  print(student)

# Вибірка студента за ім'ям
name = 'John Doe'
cursor.execute("SELECT * FROM students WHERE name = %s", (name,))
student_by_name = cursor.fetchone()
print(student_by_name)

# Оновлення віку студента
new_age = 25
student_id = 1
cursor.execute("UPDATE students SET age = %s WHERE id = %s", (new_age, student_id))

# Видалення студента за ідентифікатором
student_id = 2
cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))

# Додавання студентів з використанням транзакцій
new_students = [
  ('Emily Davis', 21, 'emily@example.com'),
  ('Daniel Wilson', 20, 'daniel@example.com')
]
try:
  conn.start_transaction()
  cursor.executemany("INSERT INTO students (name, age, email) VALUES (%s, %s, %s)", new_students)
  conn.commit()
except mysql.connector.Error as error:
  print("Error occurred during transaction. Rolling back changes.")
  conn.rollback()

# Створення таблиці courses
cursor.execute("CREATE TABLE courses (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), description VARCHAR(255), credits INT)")

# Додавання курсів до таблиці courses
courses = [
  ('Mathematics', 'Advanced calculus', 5),
  ('Physics', 'Quantum mechanics', 4),
  ('Computer Science', 'Programming fundamentals', 3)
]
cursor.executemany("INSERT INTO courses (name, description, credits) VALUES (%s, %s, %s)", courses)

# Створення таблиці student_courses
cursor.execute("CREATE TABLE student_courses (student_id INT, course_id INT, FOREIGN KEY (student_id) REFERENCES students(id), FOREIGN KEY (course_id) REFERENCES courses(id))")

# Заповнення таблиці student_courses
student_courses = [
  (1, 1),
  (1, 2),
  (2, 3),
  (3, 1),
  (4, 2),
  (5, 3)
]
cursor.executemany("INSERT INTO student_courses (student_id, course_id) VALUES (%s, %s)", student_courses)

# Вибірка студентів, які вибрали певний курс
course_id = 1
cursor.execute("SELECT students.* FROM students JOIN student_courses ON students.id = student_courses.student_id WHERE student_courses.course_id = %s", (course_id,))
students_for_course = cursor.fetchall()
for student in students_for_course:
  print(student)

# Вибірка курсів, які вибрали студенти за певним ім'ям
student_name = 'John Doe'
cursor.execute("SELECT courses.* FROM courses JOIN student_courses ON courses.id = student_courses.course_id JOIN students ON students.id = student_courses.student_id WHERE students.name = %s", (student_name,))
courses_for_student = cursor.fetchall()
for course in courses_for_student:
  print(course)

# Вибірка всіх студентів та їх курсів, використовуючи JOIN
cursor.execute("SELECT students.name, courses.name FROM students JOIN student_courses ON students.id = student_courses.student_id JOIN courses ON courses.id = student_courses.course_id")
student_course_data = cursor.fetchall()
for data in student_course_data:
  print(data)

# Закриття підключення до бази даних
cursor.close()
conn.close()
