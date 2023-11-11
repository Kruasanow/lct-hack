
from apps import db
from apps.home.models import Worker, Tasks, Points, Schedule, Full_tasks, Undistr_tasks, Worker_last_location
from datetime import datetime, timedelta, date
from sqlalchemy import text, case, select, create_engine
from sqlalchemy.orm import sessionmaker
from geopy.distance import geodesic
import json
import uuid
from geopy.geocoders import Nominatim
from sqlalchemy.orm.session import make_transient

# TODO: обновить home.models (не все модели там есть и убрать лишнее)


# def manual_add(task_type, task_title, task_priority, task_lead_time, task_level, point_id, point_address, date):
#     new_full_task = Full_tasks(
#         idt=generate_uuid_as_int(),
#         task_type=task_type,
#         task_title=task_title,
#         task_priority=task_priority,
#         task_lead_time=task_lead_time,
#         task_level=task_level,
#         point_id=point_id,
#         point_address=point_address,
#         date=date,
#         status='active'
#     )
#     db.session.add(new_full_task)

#     # TODO: тут еще нужно добавление задачи в расписание сотрудника,
#     #  мб написать еще функцию удаления ("отмены") задачи из расписания сотрудника!!!!!!!!

#     db.session.commit()
    
# def add_holiday_worker(date_start, date_end, worker_id):
#     # TODO: нужно добавить таблицу отпусков сотрудников (два столбца - worker_id и holiday)
#     row_to_update = db.session.query(Holiday).filter(Holidays.worker_id == worker_id).first()
    
#     holiday = row_to_update.holiday.split(',')
    
#     delta = int((date_end - date_start).days)

#     day_hol = date_start
    
#     holiday.append(date_start.strftime('%Y_%m_%d'))

#     while delta > 0:
#         day_hol += timedelta(days=1)
#         holiday.append(day_hol.strftime('%Y_%m_%d'))
#         delta -= 1

#     holiday.append(date_end.strftime('%Y_%m_%d'))

#     row_to_update.holiday = ','.join(holiday)
#     db.session.commit()

def address_to_coordinates(address):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(address)

    if location:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    else:
        return None
def get_schedule_for_worker_on_day(date, worker_id):
    schedule_record = db.session.query(Schedule).filter_by(date=date).first()
    if schedule_record:
        schedule_data = {}
        task_data = {}
        json_data = json.loads(schedule_record.schedule)
        worker_schedule = json_data[worker_id]['schedule']
        for interval, idt in worker_schedule.items():
            task = db.session.query(Full_tasks).filter_by(idt=idt).first()
            if task:
                idt = task.idt
                task_type = task.task_type
                task_lead_time = db.session.query(Tasks).filter_by(type=task_type).first()
                task_title = task.task_title
                task_priority = task.task_priority
                point_id = task.point_id
                point_address = task.point_address
                status = task.status
            task_data['task_title'] = task_title
            task_data['task_priority'] = task_priority
            task_data['task_lead_time'] = task_lead_time
            task_data['point_address'] = point_address
            task_data['task_status'] = status
            task_data['point_id'] = point_id
            task_data['task_idt'] = idt
            task_data['task_type'] = task_type
            schedule_data[interval] = task_data
        return schedule_data
    else:
        return None


def get_schedule_for_worker_on_interval(start_date, end_date, worker_id):
    schedule_data = {}

    schedule_records = db.session.query(Schedule).filter(
        Schedule.date >= start_date.strftime("%Y_%m_%d"),
        Schedule.date <= end_date.strftime("%Y_%m_%d")
    ).all()

    for schedule_record in schedule_records:
        json_data = json.loads(schedule_record.schedule)
        if worker_id in json_data:
            worker_schedule = json_data[worker_id]['schedule']
            for interval, idt in worker_schedule.items():
                task = db.session.query(Full_tasks).filter_by(idt=idt).first()
                if task:
                    task_data = {
                        'task_title': task.task_title,
                        'task_priority': task.task_priority,
                        'task_lead_time': task.task_lead_time,
                        'point_address': task.point_address,
                        'task_status': task.status,
                        'point_id': task.point_id,
                        'task_idt': task.idt,
                        'task_type': task.task_type
                    }

                    if schedule_record.date not in schedule_data:
                        schedule_data[schedule_record.date] = {}
                    schedule_data[schedule_record.date][interval] = task_data

    return schedule_data

def save_task_сompleted(idt):
    row_to_update = db.session.query(Full_tasks).filter(Full_tasks.idt == str(idt)).first()
    if row_to_update:
        row_to_update.status = 'finish'
        db.session.commit()
        return True
    else:
        return False


def add_worker(FIO, location, grade):
    new_worker = Worker(FIO=FIO, location=location, grade=grade)
    db.session.add(new_worker)
    db.session.commit()

def add_task(title, priority, lead_time, condition, level):
    new_task = Tasks(title=title, priority=priority, lead_time=lead_time, condition=condition, level=level)
    db.session.add(new_task)
    db.session.commit()

def add_point(address, connected, delivered, days_last_card, num_approved_app, num_card):
    new_point = Points(address=address, connected=connected, delivered=delivered, days_last_card=days_last_card, num_approved_app=num_approved_app, num_card=num_card)
    db.session.add(new_point)
    db.session.commit()


def add_schedule(date):                              # TODO: обработать исключения, когда добавляется такая же дата
    schedule_data = {
        "1": {"schedule": {}
              },
        "2": {"schedule": {}
              },
        "3": {"schedule": {}
              },
        "4": {"schedule": {}
              },
        "5": {"schedule": {}
              },
        "6": {"schedule": {}
              },
        "7": {"schedule": {}
              },
        "8": {"schedule": {}
              }
    }
    existing_schedule = Schedule.query.filter_by(
        date=date
    ).first()

    if not existing_schedule:
        schedule_blob = json.dumps(schedule_data).encode('utf-8')
        new_schedule = Schedule(date=date, schedule=schedule_blob)
        db.session.add(new_schedule)
        db.session.commit()


def get_schedule(date):
    schedule_record = db.session.query(Schedule).filter_by(date=date).first()

    if schedule_record:
        schedule_blob = schedule_record.schedule

        schedule_data = json.loads(schedule_blob.decode('utf-8'))

        return schedule_data
    else:
        return None


def dict_task_points():
    tasks = Tasks.query.all()
    task_points = {}
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y_%m_%d')

    for task in tasks:
        condition = task.condition

        if 'yesterday' in condition:
            condition = condition.replace('yesterday', yesterday)

        # condition = text(condition)
        print(condition)
        print(Points.query.filter(text(condition)).statement)
        # task_results[task.type] = Points.query.filter(condition).all()
        task_points[task.type] = [point.id for point in Points.query.filter(text(condition))]

    print('dict_task_points', task_points)

    return task_points


# def dict_task_worker():
#     workers = Worker.query.all()
#     tasks = Tasks.query.all()
#     task_workers = {}
#
#     for task in tasks:
#         level = task.level
#         worker_for_id = []
#         for worker in workers:
#             grade = worker.grade
#             if grade == 'синьор':
#                 if 'синьор' in level or 'мидл' in level or 'джун' in level:
#                     worker_for_id.append(worker.id)
#             if grade == 'мидл':
#                 if 'мидл' in level or 'джун' in level:
#                     worker_for_id.append(worker.id)
#             if grade == 'джун':
#                 if grade in level:
#                     worker_for_id.append(worker.id)
#
#         task_workers[task.type] = worker_for_id
#
#     # print(task_workers)
#
#     return task_workers

def generate_uuid_as_int():
    unique_id = uuid.uuid4()
    unique_id_as_int = int(unique_id.hex, 16)
    return unique_id_as_int

def line_tasks():
    stack_tasks = []
    task_points = dict_task_points()
    day_t = datetime.today().strftime('%Y_%m_%d')

    # idt = 1

    for task in task_points:
        type_t = task
        task_info_bd = db.session.query(Tasks).filter(Tasks.type == type_t).all()
        for t in task_info_bd:
            task_tuple = (t.type, t.title, t.priority, t.lead_time, t.level)
        for point in task_points[task]:
            task_info = {}
            id_p = point
            point_info_bd = db.session.query(Points).filter(Points.id == id_p).all()
            for p in point_info_bd:
                point_tuple = (p.id, p.address)
                # task_info['IDT'] = idt
                task_info['IDT'] = str(generate_uuid_as_int())
                task_info['Task_info'] = task_tuple
                task_info['Point_info'] = point_tuple
                task_info['Today'] = day_t
                # idt += 1
                stack_tasks.append(task_info)
        # print('task', task, 'line_tasks', stack_tasks)
        for item in stack_tasks:
            existing_task = Full_tasks.query.filter_by(
                task_type=item['Task_info'][0],
                task_title=item['Task_info'][1],
                task_priority=item['Task_info'][2],
                task_lead_time=item['Task_info'][3],
                task_level=item['Task_info'][4],
                point_id=item['Point_info'][0],
                point_address=item['Point_info'][1],
                date=day_t
            ).first()

            if not existing_task:
                new_undistr_task = Undistr_tasks(
                    idt=item['IDT'],
                    task_type=item['Task_info'][0],
                    task_title=item['Task_info'][1],
                    task_priority=item['Task_info'][2],
                    task_lead_time=item['Task_info'][3],
                    task_level=item['Task_info'][4],
                    point_id=item['Point_info'][0],
                    point_address=item['Point_info'][1],
                    date=day_t
                )
                new_full_task = Full_tasks(
                    idt=item['IDT'],
                    task_type=item['Task_info'][0],
                    task_title=item['Task_info'][1],
                    task_priority=item['Task_info'][2],
                    task_lead_time=item['Task_info'][3],
                    task_level=item['Task_info'][4],
                    point_id=item['Point_info'][0],
                    point_address=item['Point_info'][1],
                    date=day_t,
                    status='wait'
                )

                db.session.add(new_undistr_task)
                db.session.add(new_full_task)
        db.session.commit()
    return stack_tasks

# def custom_sort(item):
#     priority_order = {"Высокий": 1, "Средний": 2, "Низкий": 3}
#     return priority_order.get(item['Task_info'][2])
#
# def sort_priority_line_tasks(data):
#     sorted_data = sorted(data, key=custom_sort)
#     for item in sorted_data:
#         existing_task = Undistr_tasks.query.filter_by(
#             task_type=item['Task_info'][0],
#             task_title=item['Task_info'][1],
#             task_priority=item['Task_info'][2],
#             task_lead_time=item['Task_info'][3],
#             task_level=item['Task_info'][4],
#             point_id=item['Point_info'][0],
#             point_address=item['Point_info'][1]
#         ).first()
#
#         if not existing_task:
#             new_undistr_task = Undistr_tasks(
#                 task_type=item['Task_info'][0],
#                 task_title=item['Task_info'][1],
#                 task_priority=item['Task_info'][2],
#                 task_lead_time=item['Task_info'][3],
#                 task_level=item['Task_info'][4],
#                 point_id=item['Point_info'][0],
#                 point_address=item['Point_info'][1]
#             )
#
#             db.session.add(new_undistr_task)  # Добавляем запись в таблицу БД
#     db.session.commit()
#     return sorted_data

def filter_worker(task_level, workers):
    filtered_workers = []
    for worker in workers:
        grade = worker.grade
        if grade in task_level:
            filtered_workers.append(worker)
    return filtered_workers

# def sort_workers_by_distance(task_location, workers):
#     sorted_workers = sorted(workers, key=lambda worker: geodesic(worker.location, task_location).kilometers)
#     # print(sorted_workers)
#     return sorted_workers

def sort_workers_by_distance(task_location, workers, workers_last_locations):
    def calc_dist(worker):
        worker_location = Worker_last_location.query.get(worker.id).last_location.split(', ')
        worker_lat, worker_lon = map(float, worker_location)
        return geodesic((worker_lat, worker_lon), task_location).kilometers

    sorted_workers = sorted(workers, key=calc_dist)
    return sorted_workers

def is_free_time_available(schedule, worker_id, lead_time):
    start_time = datetime.strptime("09:00", "%H:%M")
    end_time = datetime.strptime("18:00", "%H:%M")

    # worker_schedule = schedule.get(worker_id, {}).get('schedule', {})
    worker_schedule = schedule[str(worker_id)]['schedule']

    if not worker_schedule:  # Если у сотрудника нет расписания, то всё рабочее время свободно
        return '09:00 - 18:00'

    current_time = start_time

    for time_slot, task_id in sorted(worker_schedule.items(),
                                     key=lambda x: datetime.strptime(x[0].split(" - ")[0], "%H:%M")):
        slot_start, slot_end = map(lambda x: datetime.strptime(x, "%H:%M"), time_slot.split(" - "))

        if current_time + timedelta(hours=lead_time) <= slot_start:
            result = f"{current_time.strftime('%H:%M')} - {slot_start.strftime('%H:%M')}"
            # print(result)
            return result  # Найдено свободное время с достаточной продолжительностью

        current_time = slot_end

    if current_time + timedelta(hours=lead_time) <= end_time:
        result = f"{current_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
        return result  # Последний временной интервал в рабочем дне

    return False

def calculate_travel_time(coord1, coord2):
    lat1, lon1 = map(float, coord1.split(', '))
    lat2, lon2 = map(float, coord2.split(', '))

    distance = geodesic((lat1, lon1), (lat2, lon2)).kilometers

    average_speed = 40

    travel_time_hours = distance / average_speed

    return travel_time_hours

def check_schedule(worker, task, today):
    schedules = Schedule.query.all()
    for sh in schedules:
        year, month, day = map(int, sh.date.split('_'))
        sh_date = datetime(year, month, day).date()
        if sh_date <= today:
            pass
        else:
            sched = json.loads(sh.schedule.decode('utf-8'))
            coord1 = worker.location
            coord2 = task.point_address
            travel_time = calculate_travel_time(coord1, coord2)
            full_time = task.task_lead_time + travel_time
            if is_free_time_available(sched, worker.id, full_time):
                # print("True")
                free_interval = is_free_time_available(sched, worker.id, full_time)
                return sh.date, free_interval, full_time, task.task_type

    return False


def assign_task_to_worker(idt, worker_id, date_free, free_interval, task_lead_time, point_address):
    start_time = datetime.strptime(free_interval.split(' - ')[0], "%H:%M")
    end_time = start_time + timedelta(hours=float(task_lead_time))
    formatted_interval = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"

    schedule_record = db.session.query(Schedule).filter_by(date=date_free).first()
    # print(schedule_record)

    if schedule_record:

        schedule = json.loads(schedule_record.schedule.decode("utf-8"))

        if worker_id in schedule:
            worker_schedule = schedule[worker_id]["schedule"]
            # print(worker_schedule)

            intervals = list(worker_schedule.keys())
            insert_index = 0
            for interval in intervals:
                if formatted_interval < interval:
                    break
                insert_index += 1

            worker_schedule[formatted_interval] = str(idt)
            new_schedule = dict(list(worker_schedule.items())[:insert_index] +
                                [(formatted_interval, str(idt))] +
                                list(worker_schedule.items())[insert_index:])
            schedule[worker_id]["schedule"] = new_schedule
            duration_to_update = db.session.query(Full_tasks).filter(Full_tasks.idt == str(idt)).first()
            duration_to_update.task_lead_time = task_lead_time

            row_to_update = db.session.query(Full_tasks).filter(Full_tasks.idt == str(idt)).first()
            row_to_update.status = 'active'

            row_to_update = db.session.query(Full_tasks).filter(Full_tasks.idt == str(idt)).first()
            row_to_update.worker_id = worker_id

            last_location_update = db.session.query(Worker_last_location).filter(Worker_last_location.id == int(worker_id)).first()
            print("Обновление", last_location_update.last_location, 'на', point_address, 'для сотрудника', worker_id)
            last_location_update.last_location = point_address

            row_to_delete = db.session.query(Undistr_tasks).filter(Undistr_tasks.idt == str(idt)).first()
            db.session.delete(row_to_delete)

        else:
            raise Exception("Сотрудник не найден в расписании.")

        schedule_record.schedule = json.dumps(schedule).encode("utf-8")
        db.session.commit()
    else:
        raise Exception(f"Расписание для даты {date_free} не найдено.")

def distribute_tasks():
    workers = Worker.query.all()
    workers_last_locations = Worker_last_location.query.all()
    # tasks = Undistr_tasks.query.all()

    priority_order = {"Высокий": 1, "Средний": 2, "Низкий": 3}

    order_conditions = case(
        *[
            (Undistr_tasks.task_priority == priority, order)
            for priority, order in priority_order.items()
        ],
        else_=len(priority_order) + 1
    )

    # tasks = Undistr_tasks.query.order_by(order_conditions).all()
    record_count = db.session.query(Undistr_tasks).count()

    if record_count <= 0:
        return False

    today = date.today()

    end_day = today.strftime("%Y_%m_%d")

    while record_count > 0:

        tasks = Undistr_tasks.query.order_by(order_conditions).all()

        record_count = db.session.query(Undistr_tasks).count()
        # print(record_count)
        r_c = record_count

        for task in tasks:
            # print(task.task_level)
            eligible_workers = filter_worker(task.task_level, workers)  # Фильтрация сотрудников по грейду и сложности задачи
            # print("Сотрудники по грейду: ", eligible_workers)

            sorted_workers = sort_workers_by_distance(task.point_address, eligible_workers, workers_last_locations)  # Сортировка сотрудников по расстоянию от места задачи

            # print("Сотрудники по удаленности от задачи: ", sorted_workers)
            # print('LEVEL: ', task.task_level, 'TASK NAME: ', task.task_title)
            # print('WORKERS: ', sorted_workers)
            for worker in sorted_workers:
                # print('WORKER FIO', worker.FIO, 'GRADE: ', worker.grade)
                if check_schedule(worker, task, today):  # Проверка наличия свободного времени и места в расписании
                    date_free, free_interval, task_lead_time, task_type = check_schedule(worker, task, today)
                    assign_task_to_worker(task.idt, str(worker.id), date_free, free_interval, str(task_lead_time), task.point_address)   # Назначить задачу сотруднику и обновить его расписание
                    last_day = date_free
                    # print('FREE DATE', date_free, 'FREE INTERVAL: ', free_interval, '\n')
                    break
                else:
                    # print('ЗАНЯТОЙ СОТРУДНИК!!!!!!!!!!!!!!!!!!!!!!')
                    pass

            r_c -= 1

        for worker_l_l in workers_last_locations:
            worker_l_p = Worker.query.get(worker_l_l.id).location
            last_location_update = db.session.query(Worker_last_location).filter(
                Worker_last_location.id == worker_l_l.id).first()
            last_location_update.last_location = worker_l_p
            print("Замена", worker_l_l.last_location, 'на', worker_l_p)

        db.session.commit()

        end_day = datetime.strptime(end_day, "%Y_%m_%d")
        end_day = (end_day + timedelta(days=1)).strftime("%Y_%m_%d")
        end_day = datetime.strptime(end_day, "%Y_%m_%d")

        def is_weekend(end_day):
            return end_day.weekday() in [5, 6]

        while is_weekend(end_day):
            end_day += timedelta(days=1)

        end_day = end_day.strftime("%Y_%m_%d")
        add_schedule(end_day)
        print('Создал день')

    delete_last_two_schedule()
    return True
def delete_last_two_schedule():
    all_rows = Schedule.query.all()
    all_rows = [(row, datetime.strptime(row.date, '%Y_%m_%d')) for row in all_rows]

    sorted_rows = sorted(all_rows, key=lambda x: x[1], reverse=True)

    if len(sorted_rows) >= 2:
        for row, _ in sorted_rows[:2]:
            row = db.session.query(Schedule).get(row.id)
            print(row)
            db.session.delete(row)
        db.session.commit()
    else:
        print("В базе данных меньше чем 2 строки")

def get_schedule_for_workers_on_day(date):
    # print("DATE", date)
    schedule_record = db.session.query(Schedule).filter_by(date=date).first()
    if schedule_record:
        schedule_data = {}
        json_data = json.loads(schedule_record.schedule)
        for worker_id, worker_schedule in json_data.items():
            # print("WORKER_ID", worker_id)
            # print("worker_schedule", worker_schedule)
            # worker_schedule = json_data[worker_id]['schedule']
            worker_fio = (db.session.query(Worker).filter_by(id=worker_id).first()).FIO
            # print("worker_fio", worker_fio)
            intervals = {}
            for interval, idt in worker_schedule['schedule'].items():
                task_data = {}
                # print("interval", interval)
                # print("idt", idt)
                task = db.session.query(Full_tasks).filter_by(idt=idt).first()
                if task:
                    task_data['task_title'] = task.task_title
                    task_data['task_priority'] = task.task_priority
                    task_data['task_lead_time'] = (db.session.query(Tasks).filter_by(type=task.task_type).first()).lead_time
                    # print("point_address", (db.session.query(Points).filter_by(address=task.point_address).first()).address_text)
                    task_data['point_address'] = (db.session.query(Points).filter_by(address=task.point_address).first()).address_text
                    # print(task_data['point_address'])
                    intervals[interval] = task_data
            schedule_data[worker_fio] = intervals
            print(intervals)

                # print('INTERVAL', intervals)
            # schedule_data[worker_fio] = intervals
        # print('SCHEDULE', schedule_data)
        print('!'*100, schedule_data, '!'*100)
        return schedule_data
    else:
        return None

# -----------------TODO: есть проблема с тем, что цикл назначения настроен неправильно, надо отредачить
#                   (задача не ищет ближайшее свободное время среди всех сотрудников с удовлетворяющим грейдом, а ищет время
#                   у более подходящего сотрудника)
# - это решено !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# (т.к. мы находим ближайшего сотрудника к этой задаче, учитывая их "текущую" задачу)

# -----------------TODO: есть проблема с тем, что при добавлении задачи не учитывается что сотрудник находится уже
#                   не на адресе локации(работы)(если это не первая задача на день), а на координатах прошлой задачи
# - это решено !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# -----------------TODO: Если не все задачи были выполнены в течение дня, оставшиеся переносятся на следующий день с высоким приоритетом
# - это вроде решено автоматом(т.к. я не создам новый день, пока не распределю все задачи и потом все равно
# отсортирую задачи по приоритету)!!!!!!!!!!!!!!!!!!!!

# TODO: есть проблема с тем, что при добавлении задачи не учитывается время в дороге до точки
# - это решено (не полностью) !!!!!!!!!!!!!!!!!!!!!
#  НО нужно прикрутить норм определение, а не просто по прямой от точки до точки с помощью geopy

# TODO: В каждой агентской точке выполняется только одна задача за день (хз на скок это важно
#  и нужно ли для этого отдельное ограничение)

# TODO: удалить дублирование вызова функций в if и сразу после

# TODO: реализовать функции агрегации данных для выдачи в удобном виде для веба и мобилки

# -----------------TODO: удаление пустых расписаний на день после распределения всех задач
# - это решено !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# TODO: быстрая проверка каждого расписания(дня) на полную заполненность после while в distribute_tasks()

# TODO: написать функцию загрузки инфы из exel по агентским точкам (для примера, а в докладе можно сказать про то,
#  что для реальных данных скорее всего нужен будет адаптер или нормализатор, смотря как захотят загружать)

# TODO: реализовать формирование отчетности (возможно в виде каких-то ворд или pdf документов)

# TODO: реализовать функционал ручного добавления "справочных"/"спец" задач (хотя бы на бэке,
#  чтобы можно было сказать в планах доработки)

# TODO: реализовать функционал добавления отпусков сотрудников (выключение их из получателей задач в алгоритме,
#  тоже хотя бы на бэке)

# TODO: проверить, сортировал ли задачи по приоритету в очереди (вероятнее всего не нужно, так как они отсортированы
#  на данный момент в tasks(просто задачи в справочнике)), но стоит реализовать сортировку задач
#  в dict_task_points() по приоритету

# TODO: написать функционал логирования, при изменении/удалении справочников, юзеров, загрузке данных и тд

# TODO: попробовать реализовать модельку или ещё что-то для распознавания условий в текстовом виде
#  (перевод в "машинопонятный" язык)

# TODO: спросить на митапе про "доучивание сервиса" или поискать ответ на прошлом митапе

