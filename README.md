# SC_TaskManager
Task Manager for Supercomputer


### Description
ИС «Диспетчер суперкомпьютера».

Есть суперкомпьютер, содержащий N процессорных ядер.

На нем некоторое количество пользователей запускает параллельные программы(написанные, скажем, на С/C++ с помощью библиотеки MPI).

Диспетчер выполняет следующие функции:

1. Добавление задачи в очередь

2. Запуск задачи на выполнение(если есть свободные процессорные ядра)

3. Принудительная остановка задачи

4. Возобновление выполнения задачи

5. Изменение приоритета задачи(что может приводить к действиям 1, 2, 3 как для данной, так и для других задач)

6. Фиксация факта завершения задачи

7. Полное удаление задачи из системы

После каждого изменения состояния системы происходит передиспетчеризация.

### Deploy

- `python manage.py migrate` для применения всех миграций
- Добавить сведения о системе через базу данных, либо через админ-панель django
- `python manage.py runserver` для старта локального сервера на 8000 порту


### Refactoring

1. Добавить привязку сервиса к системе, чтобы была возможность работать с MPI
------

​																																									Author: deorz
