# -*- encoding: utf-8 -*-
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from flask import session,Blueprint
from apps import db
from apps.home.models import Worker, Users, Full_tasks, Schedule, Points, Tasks
from apps.home.function import line_tasks, distribute_tasks, get_schedule_for_workers_on_day, address_to_coordinates, add_task
from flask import request, jsonify
import json
from collections import defaultdict
from sqlalchemy import func
# line_tasks()                          # создание очереди
# distribute_tasks()                    # распределение задач
# TODO: для blueprint задач доавить всязь двух таблиц(установление юзера по задачам)
#Получение имени пользователя и роли    
def role():
    username = session.get('username')
    role = session.get('role')
    return username, role

@blueprint.route('/index')
@login_required
def index():
    username, user_role = role()
    users=Users.query.all()
    user_count = Users.query.with_entities(Users.username).count()
    worker_count = Users.query.with_entities(Worker.FIO).count()
    tasks_count = Users.query.with_entities(Tasks.title).count()
    full_tasks_count = Users.query.with_entities(Full_tasks.idt).count()
    schedules = Schedule.query.all()

    # Создаем словарь для хранения количества id для каждой даты
    count_by_date = defaultdict(int)

    # Проходим по каждой записи
    for schedule in schedules:
        date = schedule.date
        schedule_data = json.loads(schedule.schedule)

        # Проходим по каждому id в расписании и увеличиваем счетчик
        for _, data in schedule_data.items():
            for _, id_value in data['schedule'].items():
                count_by_date[date] += 1

    # Преобразуем словарь в массив кортежей
    result_array = list(count_by_date.items())
    tasks_per_day = result_array
    print(tasks_per_day)
    return render_template('home/index.html', segment='index', username=username, role=user_role,users=users,user_count=user_count,worker_count=worker_count,tasks_count=tasks_count,full_tasks_count = full_tasks_count,tasks_per_day=tasks_per_day)

@blueprint.route('/<template>', methods=['GET', 'POST'])
@login_required
def route_template(template):
    username,user_role=role() 
    try:
        if not template.endswith('.html'):
            template += '.html'
        segment = get_segment(request)
        if template == 'tables.html':
            workers=Worker.query.all()[:3]
            users=Users.query.all()[:3]
            points=Points.query.all()[:3]
            return render_template("home/" + template, segment=segment, username=username, role=user_role, workers=workers,users=users,points=points)
        if template == 'workers.html':
            workers=Worker.query.all()
            return render_template("home/" + template, segment=segment, username=username, role=user_role, workers=workers)
        if template == 'users.html':
            users=Users.query.all()
            for user in users:
                user.password='***'
            return render_template("home/" + template, segment=segment, username=username, role=user_role, users=users)
        if template == 'points.html':
            points=Points.query.all()
            return render_template("home/" + template, segment=segment, username=username, role=user_role, points=points)
        if template == 'calendar.html':
            schedules = Schedule.query.all()
            dates = [schedule.date for schedule in schedules]
            return render_template("home/" + template, segment=segment, username=username, role=user_role, schedule=dates)
        if template == 'billing.html':
            data = []
            tasks=Tasks.query.all()
            full_tasks = Full_tasks.query.all()
            for full_task in full_tasks:
                worker = db.session.query(Worker).filter(Worker.id == full_task.worker_id).first()
                task_data = {
                    'idt': full_task.idt,
                    'fio': worker.FIO,
                    'task_title': full_task.task_title,
                    'task_priority': full_task.task_priority,
                    'task_lead_time': full_task.task_lead_time,
                    'point_address': full_task.point_address,
                    'task_status': full_task.status,
                    'task_comment': full_task.comment,
                }
                data.append(task_data)
                entered_values = []

            import re
            def process_expression(input_str):
                regex = re.compile(r'\((.*?)\)')

                def process_sub_expression(sub_expr):

                    if "num_approved_app" in sub_expr or "num_card" in sub_expr:

                        sub_expr = sub_expr.replace('(', '').replace(')', '')

                        return f'CAST({sub_expr})'
                    return sub_expr

                result = regex.sub(lambda match: process_sub_expression(match.group(1)), input_str)

                return result

            
            def transform_str(resArr):
                if '| )' in resArr:
                    resArr = resArr.replace(' | )', ') | ')
                if '& )' in resArr:
                    resArr = resArr.replace(' & )', ') & ')
                return resArr

            def res_arr_form_maker(resArr):
                # print(resArr)
                res_string = ''
                try:
                    for i in resArr:
                        if '|' in i:
                            i = i.replace(' |','')
                            res_string += f"({i}) | "
                        elif '&' in i:
                            i = i.replace(' &','')
                            res_string += f"({i}) & "
                        elif '(' in i:
                            res_string+='('
                        elif ')' in i:
                            res_string+=')'
                        else:
                            print('ne I ne & ne srabotalo')
                    # print(res_string[:-2])
                except Exception:
                    pass
                return process_expression(transform_str(res_string[:-2]))
            import random
            if request.method == 'POST':
                priority = request.form.get('prioritySelect')
                task_name = request.form.get('taskname')
                # dlit = request.form.get('dlit')
                resArr = request.form.get('resArr')
                selected_levels = request.form.getlist('levels')
                
                if resArr:
                    resArr = json.loads(resArr)
                else:
                    resArr = []
                entered_values = [task_name, priority, res_arr_form_maker(resArr), str(selected_levels)]
                print(entered_values)
                add_task(task_name, priority, round(random.uniform(0.0, 5.0), 2), res_arr_form_maker(resArr), str(selected_levels))
            # TODO Здесь необходимо связать таблицы Full_tasks и Worker и подать странице новую БД( строки в html, под них форматировать не обязательно: ID,ФИО,task_title,task_priority,point_address,date,status,comment)

            # idt
            # fio
            # task_title
            # task_priority
            # task_lead_time
            # point_address
            # status
            # comment

            #return render_template("home/" + template, segment=segment, username=username, role=user_role, tasks=tasks,full_tasks=full_tasks)
            return render_template("home/" + template, segment=segment, username=username, role=user_role,tasks=tasks,full_tasks=data)
        else:
            return render_template("home/" + template, segment=segment,username=username, role=user_role)
    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


@blueprint.route('/endpoint', methods=['GET'])
def get_data_by_date():
    selected_date = request.args.get('date')
    schedule_data = get_schedule_for_workers_on_day(selected_date)


    # # Вывод расписания в Jinja2
    # for worker, intervals in schedule_data.items():
    #     print(f"Имя работника: {worker}")
    #     print("Данные:")
    #     for interval, task_data in intervals.items():
    #         print(f" - Интервал времени: {interval}")
    #         print(f"   - Название задачи: {task_data['task_title']}")
    #         print(f"   - Приоритет: {task_data['task_priority']}")
    #         print(f"   - Длительность выполнения: {task_data['task_lead_time']}")
    #         print(f"   - Адрес: {task_data['point_address']}")
    #     print("=" * 30)

    # Форматирование данных для передачи в шаблон
    schedule = [{'worker': worker, 'intervals': intervals} for worker, intervals in schedule_data.items()]
    print(schedule)
    return jsonify(schedule)


def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None
#Обновление строки таблицы users
@blueprint.route('/update_user/<id>', methods=['POST'])
@login_required
def update_users(id):
    try:
        data = request.json
        print(data)
        print(data['id'])
        user = db.session.query(Users).filter(Users.id == data['id']).first()
        if user:
            user.username = data['username']
            user.role = data['role']
            user.worker_FIO= data['worker_FIO']
        db.session.commit()
        return jsonify({'message': 'Данные пользователей успешно обновлены'})
    except Exception as e:
        return jsonify({'error': 'Произошла ошибка при обновлении данных пользователей'}), 500
#Удаление строки из таблицы users    
@blueprint.route('/delete_user/<username>', methods=['POST'])
@login_required
def delete_user(username):
    try:
        row_to_delete = db.session.query(Users).filter(Users.username == username).first()
        print(row_to_delete)
        if  row_to_delete:
            print(row_to_delete)
            db.session.delete(row_to_delete)
            db.session.commit()
            db.session.execute("VACUUM")
            return jsonify({'message': 'Пользователь успешно удален'})
        else:
            return jsonify({'error': 'Пользователь не найден'}), 404
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return jsonify({'error': 'Произошла ошибка при удалении пользователя'}), 500
#изменение сотрудников в таблице workers
@blueprint.route('/update_worker/<id>', methods=['POST'])
@login_required
def update_workers(id):
    try:
        data = request.json 
        print(data)
        print(data['id'])
        worker_id = int(data['id'])
        worker = db.session.query(Worker).filter(Worker.id == worker_id).first()
        if worker:
            print(data['id'])
            worker.FIO = data['FIO']
            print(worker.FIO)
            worker.location_text = data['location']
            worker.grade = data['grade']
            worker.location = address_to_coordinates(data['location'])
        else:
            new_worker = Worker(**data)
            db.session.add(new_worker)
        db.session.commit()  
        return jsonify({'message': 'Данные сотрудников успешно обновлены'})
    except Exception as e:
        print(str(e))  # Добавим вывод ошибки в консоль
        return jsonify({'error': 'Произошла ошибка при обновлении данных сотрудников'}), 500
#добавление сотрудников
@blueprint.route('/add_workers', methods=['POST'])
@login_required
def add():
    fio = request.json.get('fio')
    location = request.json.get('location')
    grade = request.json.get('grade')
    user = Worker.query.filter_by(FIO=fio).first()
    loc = address_to_coordinates(location)
    if not loc:
        loc = "Сервер координат недоступен"
    if user:
        return jsonify({'success': False, 'msg': 'ФИО уже существует'})
    new_worker = Worker(FIO=fio, location=loc, grade=grade, location_text=location)
    db.session.add(new_worker)
    db.session.commit()
    return jsonify({'success': True, 'msg': 'Сотрудник успешно добавлен'})
#удаление сотрудников    
@blueprint.route('/delete_worker/<id>', methods=['POST'])
@login_required
def delete_worker(id):
    try:
        row_to_delete = db.session.query(Worker).filter(Worker.id == id).first()
        print(1)
        print(row_to_delete)
        if  row_to_delete:
            print(row_to_delete)
            db.session.delete(row_to_delete)
            db.session.commit()  # Сохранить изменения
            db.session.execute("VACUUM")
            return jsonify({'message': 'Пользователь успешно удален'})
        else:
            return jsonify({'error': 'Пользователь не найден'}), 404
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return jsonify({'error': 'Произошла ошибка при удалении пользователя'}), 500
#Удаление сотрудников из таблицы points
@blueprint.route('/delete_points/<id>', methods=['POST'])
@login_required
def delete_points(id):
    try:
        row_to_delete = db.session.query(Points).filter(Points.id == id).first()
        print(1)
        print(row_to_delete)
        if  row_to_delete:
            print(row_to_delete)
            db.session.delete(row_to_delete)
            db.session.commit()  # Сохранить изменения
            db.session.execute("VACUUM")
            return jsonify({'message': 'Пользователь успешно удален'})
        else:
            return jsonify({'error': 'Пользователь не найден'}), 404
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return jsonify({'error': 'Произошла ошибка при удалении пользователя'}), 500    
#Добавление/изменение сотрудников в таблице points
@blueprint.route('/update_points/<id>', methods=['POST'])
@login_required
def update_points(id):
    try:
        data = request.json 
        delivered_value = data['delivered'].lower() == 'true'
        point = db.session.query(Points).filter(Points.id == int(data['id'])).first()
        if point:
            loc = address_to_coordinates(data['address'])
            if not loc:
                loc = "Сервер координат недоступен"
            point.address = loc
            point.connected = data['connected']
            point.delivered = delivered_value
            point.days_last_card = data['days_last_card']
            point.num_approved_app = data['num_approved_app']
            point.num_card = data['num_card']
            point.address_text = data['address']
            point.delivered_text = data['delivered']
        else:
            new_point = Points(**data)
            db.session.add(new_point)
        db.session.commit()  
        return jsonify({'message': 'Данные  успешно обновлены'})
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return jsonify({'error': 'Произошла ошибка при обновлении'}), 500
#добавление точки
@blueprint.route('/add_points', methods=['POST'])
@login_required
def add_points():
    print()
    address = request.json.get('address')
    connected = request.json.get('connected')
    delivered = bool(request.json.get('delivered'))
    days_last_card = request.json.get('days_last_card')
    num_approved_app = request.json.get('num_approved_app')
    num_card = request.json.get('num_card')

    # Создание новой точки и добавление в базу данных
    new_point = Points(address=address, connected=connected, delivered=delivered,
                      days_last_card=days_last_card, num_approved_app=num_approved_app, num_card=num_card)
    db.session.add(new_point)
    db.session.commit()

    return jsonify({'success': True, 'msg': 'Точка успешно добавлена'})



#задачи

@blueprint.route('/delete_task/<type>', methods=['POST'])
@login_required
def delete_task(type):
    try:
        print(type)
        row_to_delete = db.session.query(Tasks).filter(Tasks.type == int(type)).first()
        if row_to_delete:
            db.session.delete(row_to_delete)
            db.session.commit()
            return jsonify({'message': 'Задача успешно удалена'})
        else:
            return jsonify({'error': 'Задача не найдена'}), 404
    except Exception as e:
        return jsonify({'error': 'Произошла ошибка при удалении задачи'}), 500

@blueprint.route('/update_task/<type>', methods=['POST'])
@login_required
def update_task(type):
    try:
        data = request.json
        updated_title = data['title']
        updated_priority = data['priority']
        updated_lead_time = data['lead_time']
        updated_condition = data['condition']
        updated_level = data['level']

        task = db.session.query(Tasks).filter(Tasks.type == int(type)).first()
        if task:
            task.title = updated_title
            task.priority = updated_priority
            task.lead_time = updated_lead_time
            task.condition = updated_condition
            task.level = updated_level
        else:
            new_task = Tasks(type=type, title=updated_title, priority=updated_priority,
                             lead_time=updated_lead_time, condition=updated_condition, level=updated_level)
            db.session.add(new_task)

        db.session.commit()
        return jsonify({'message': 'Данные успешно обновлены'})
    except Exception as e:
        return jsonify({'error': 'Произошла ошибка при обновлении данных'}), 500

# @blueprint.route('/add_task', methods=['POST'])
# @login_required
# def add_task():
#     try:
#         data = request.json
#         new_type = data['type']
#         new_title = data['title']
#         new_priority = data['priority']
#         new_lead_time = data['lead_time']
#         new_condition = data['condition']
#         new_level = data['level']

#         new_task = Tasks(type=new_type, title=new_title, priority=new_priority,
#                          lead_time=new_lead_time, condition=new_condition, level=new_level)
#         db.session.add(new_task)
#         db.session.commit()

#         return jsonify({'success': True, 'msg': 'Задача успешно добавлена'})
#     except Exception as e:
#         return jsonify({'error': 'Произошла ошибка при добавлении задачи'}), 500

@blueprint.route('/get_worker_locations', methods=['POST'])
@login_required
def get_worker_locations():
    workers = Worker.query.all()
    locations = [{'FIO': worker.FIO, 'location': [float(coord) for coord in worker.location.split(',')]} for worker in workers]
    print(locations)
    return jsonify(locations)

@blueprint.route('/init_task', methods=['POST'])
@login_required
def init_task():
    if line_tasks():
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

@blueprint.route('/distr_task', methods=['POST'])
@login_required
def distr_task():
    if distribute_tasks():
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})