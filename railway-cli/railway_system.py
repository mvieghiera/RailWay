# demo.py
from railway_system import RailwaySystem
from datetime import datetime
import sys


def print_menu():
    """Выводит главное меню"""
    print("\n" + "=" * 50)
    print("🚆 СИСТЕМА УПРАВЛЕНИЯ ЖЕЛЕЗНОЙ ДОРОГОЙ")
    print("=" * 50)
    print("1.  ➕ Добавить железнодорожный путь")
    print("2.  🚉 Добавить станцию")
    print("3.  🚂 Добавить локомотив")
    print("4.  🚃 Добавить вагон")
    print("5.  🚋 Собрать поезд")
    print("6.  🛡️  Проверка безопасности поезда")
    print("7.  🚀 Отправить поезд (движение)")
    print("8.  🔧 Техническое обслуживание")
    print("9.  🎫 Продать билет")
    print("10.  Обслуживание станции")
    print("11. 📊 Показать статус системы")
    print("12. 📋 Показать все поезда")
    print("13. 📋 Показать расписание")
    print("0.  🚪 Выход")
    print("=" * 50)


def add_track(system: RailwaySystem):
    """Добавление пути"""
    print("\n--- Добавление железнодорожного пути ---")
    track_id = input("ID пути (например, T1): ").strip()
    name = input("Название пути: ").strip()
    try:
        length = float(input("Длина пути (км): ").strip())
        system.add_track(track_id, name, length)
        print(f"✅ Путь '{track_id}' успешно добавлен!")
    except ValueError:
        print("❌ Ошибка: длина должна быть числом!")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


def add_station(system: RailwaySystem):
    """Добавление станции"""
    print("\n--- Добавление станции ---")
    station_id = input("ID станции (например, S1): ").strip()
    name = input("Название станции: ").strip()

    # Опционально: добавить пути
    track_ids = []
    add_tracks = input("Добавить пути к станции? (y/n): ").strip().lower()
    if add_tracks == 'y':
        tracks_input = input("Введите ID путей через пробел: ").strip()
        track_ids = tracks_input.split()

    try:
        system.add_station(station_id, name, track_ids if track_ids else None)
        print(f"✅ Станция '{station_id}' успешно добавлена!")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


def add_locomotive(system: RailwaySystem):
    """Добавление локомотива"""
    print("\n--- Добавление локомотива ---")
    loco_id = input("ID локомотива (например, L1): ").strip()
    model = input("Модель локомотива: ").strip()
    try:
        power = int(input("Мощность (кВт): ").strip())
        system.add_locomotive(loco_id, model, power)
        print(f"✅ Локомотив '{loco_id}' успешно добавлен!")
    except ValueError:
        print("❌ Ошибка: мощность должна быть числом!")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


def add_wagon(system: RailwaySystem):
    """Добавление вагона"""
    print("\n--- Добавление вагона ---")
    wagon_id = input("ID вагона (например, W1): ").strip()
    wagon_type = input("Тип вагона (passenger/cargo): ").strip()
    try:
        capacity = int(input("Вместимость: ").strip())
        system.add_wagon(wagon_id, wagon_type, capacity)
        print(f"✅ Вагон '{wagon_id}' успешно добавлен!")
    except ValueError:
        print("❌ Ошибка: вместимость должна быть числом!")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


def assemble_train(system: RailwaySystem):
    """Сборка поезда"""
    print("\n--- Сборка поезда ---")
    train_id = input("ID поезда (например, TR1): ").strip()
    loco_id = input("ID локомотива: ").strip()

    wagons_input = input("ID вагонов (через пробел): ").strip()
    wagon_ids = wagons_input.split() if wagons_input else []

    route_input = input("ID станций маршрута (через пробел, минимум 2): ").strip()
    route_ids = route_input.split()

    if len(route_ids) < 2:
        print("❌ Ошибка: маршрут должен содержать минимум 2 станции!")
        return

    try:
        system.assemble_train(train_id, loco_id, wagon_ids, route_ids)
        print(f"✅ Поезд '{train_id}' успешно собран!")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


def security_check(system: RailwaySystem):
    """Проверка безопасности"""
    print("\n--- Проверка безопасности поезда ---")
    train_id = input("ID поезда: ").strip()
    try:
        system.operation_security_control(train_id)
    except Exception as e:
        print(f"❌ Ошибка: {e}")


def move_train(system: RailwaySystem):
    """Отправка поезда"""
    print("\n--- Отправка поезда ---")
    train_id = input("ID поезда: ").strip()

    try:
        dep_str = input("Время отправления (YYYY-MM-DD HH:MM): ").strip()
        arr_str = input("Время прибытия (YYYY-MM-DD HH:MM): ").strip()

        dep_time = datetime.strptime(dep_str, "%Y-%m-%d %H:%M")
        arr_time = datetime.strptime(arr_str, "%Y-%m-%d %H:%M")

        system.operation_movement(train_id, dep_time, arr_time)
    except ValueError as e:
        print(f"❌ Ошибка формата даты/времени: {e}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


def maintenance(system: RailwaySystem):
    """Техническое обслуживание"""
    print("\n--- Техническое обслуживание ---")
    entity_id = input("ID объекта: ").strip()
    print("Тип объекта:")
    print("  1 - путь (track)")
    print("  2 - локомотив (locomotive)")
    print("  3 - поезд (train)")

    choice = input("Выберите тип (1-3): ").strip()
    type_map = {"1": "track", "2": "locomotive", "3": "train"}
    entity_type = type_map.get(choice)

    if not entity_type:
        print("❌ Неверный выбор!")
        return

    try:
        system.operation_maintenance(entity_id, entity_type)
    except Exception as e:
        print(f"❌ Ошибка: {e}")


def sell_ticket(system: RailwaySystem):
    """Продажа билета"""
    print("\n--- Продажа билета ---")
    train_id = input("ID поезда: ").strip()
    passenger = input("ФИО пассажира: ").strip()

    try:
        price = float(input("Цена билета (руб): ").strip())
        system.operation_ticket_sales(train_id, passenger, price)
    except ValueError:
        print("❌ Ошибка: цена должна быть числом!")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


def station_service(system: RailwaySystem):
    """Обслуживание станции"""
    print("\n--- Обслуживание станции ---")
    station_id = input("ID станции: ").strip()
    try:
        system.operation_station_service(station_id)
    except Exception as e:
        print(f"❌ Ошибка: {e}")


def show_status(system: RailwaySystem):
    """Показать статус системы"""
    print("\n" + "=" * 50)
    print("📊 СТАТУС СИСТЕМЫ")
    print("=" * 50)
    print(f" Путей: {len(system.tracks)}")
    print(f"🚉 Станций: {len(system.stations)}")
    print(f"🚂 Локомотивов: {len(system.locomotives)}")
    print(f"🚃 Вагонов: {len(system.wagons)}")
    print(f"🚋 Поездов: {len(system.trains)}")
    print(f"📅 Расписаний: {len(system.schedules)}")
    print(f"🎫 Билетов: {len(system.tickets)}")
    print("=" * 50)


def show_trains(system: RailwaySystem):
    """Показать все поезда"""
    print("\n" + "=" * 50)
    print("🚋 СПИСОК ПОЕЗДОВ")
    print("=" * 50)
    if not system.trains:
        print("Поезда не созданы")
    else:
        for train_id, train in system.trains.items():
            print(f"\nПоезд: {train_id}")
            print(f"  Локомотив: {train.locomotive.id} ({train.locomotive.model})")
            print(f"  Вагонов: {len(train.wagons)}")
            print(f"  Статус: {train.status.value}")
            print(f"  Безопасность: {train.security_status.value}")
            if train.route:
                route_names = [s.name for s in train.route]
                print(f"  Маршрут: {' -> '.join(route_names)}")
    print("=" * 50)


def show_schedules(system: RailwaySystem):
    """Показать расписание"""
    print("\n" + "=" * 50)
    print("📅 РАСПИСАНИЕ ДВИЖЕНИЯ")
    print("=" * 50)
    if not system.schedules:
        print("Расписание пусто")
    else:
        for schedule in system.schedules:
            print(f"\nПоезд {schedule.train_id}:")
            print(f"  Отправление: {schedule.departure_time}")
            print(f"  Прибытие: {schedule.arrival_time}")
            print(f"  Маршрут: {schedule.station_from} -> {schedule.station_to}")
    print("=" * 50)


def main():
    """Главная функция"""
    system = RailwaySystem()

    # Словарь функций для меню
    menu_functions = {
        "1": add_track,
        "2": add_station,
        "3": add_locomotive,
        "4": add_wagon,
        "5": assemble_train,
        "6": security_check,
        "7": move_train,
        "8": maintenance,
        "9": sell_ticket,
        "10": station_service,
        "11": show_status,
        "12": show_trains,
        "13": show_schedules,
    }

    print("\n👋 Добро пожаловать в систему управления железной дорогой!")

    while True:
        print_menu()
        choice = input("Выберите действие (0-13): ").strip()

        if choice == "0":
            print("\n👋 Спасибо за использование системы. До свидания!")
            break

        if choice in menu_functions:
            menu_functions[choice](system)
        else:
            print("❌ Неверный выбор! Попробуйте снова.")

        # Предложение продолжить
        if choice != "0":
            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()