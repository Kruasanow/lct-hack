# -*- encoding: utf-8 -*-

from apps.api import blueprint
from flask import jsonify
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.api.function_api import get_schedule_for_worker_on_day, get_schedule_for_worker_on_interval, save_task_completed, verify_pass
from datetime import datetime
from apps.api.models import Users, Worker


@blueprint.route('/authorization', methods=['POST'])
def authorization():    # data = {"login": "user_1", "password": '12345678qwerty'}
    try:
        data = request.get_json()

        login = data.get("login")
        password = data.get("password")

        user = Users.query.filter_by(username=login).first()

        data_worker = {}

        if user:
            if verify_pass(password, user.password):
                if user.role == 'Администратор':
                    return jsonify({{'denied': 'Воспользуйтесь веб-интерфейсом администратора'}})
                worker = Worker.query.filter_by(id=user.id).first()
                data_worker['worker_id'] = user.id
                data_worker['worker_FIO'] = worker.FIO
                data_worker['worker_location'] = worker.location
                data_worker['worker_grade'] = worker.grade
                return jsonify({'allowed' : data_worker})
            else:
                return jsonify({'denied': 'Неверный логин и пароль'}), 404
        else:
            return jsonify({'denied': 'Неверный логин и пароль'}), 404
    except Exception as e:
        return jsonify({'denied': 'Произошла ошибка при получении данных авторизации'}), 500

@blueprint.route('/schedule_worker_on_day', methods=['POST'])
def schedule_on_day():
    try:
        data = request.get_json()  # data = {"date": "2023_11_08", "worker_id": 1}
        date = data["date"]
        worker_id = data["worker_id"]
        schedule = get_schedule_for_worker_on_day(date, worker_id)
        if schedule:
            return jsonify(schedule)
        else:
            return jsonify({'error': 'Расписание не найдено'}), 404
    except Exception as e:
        return jsonify({'error': 'Произошла ошибка при получении расписания'}), 500

@blueprint.route('/schedule_worker_on_interval', methods=['POST'])
def schedule_on_interval():
    try:
        data = request.get_json()  # data = {"start_date": "2023_11_01", "end_date": "2023_11_10", "worker_id": 1}
        start_date_str = data.get("start_date")
        end_date_str = data.get("end_date")
        worker_id = data.get("worker_id")

        start_date = datetime.strptime(start_date_str, "%Y_%m_%d")
        end_date = datetime.strptime(end_date_str, "%Y_%m_%d")

        schedule_data = get_schedule_for_worker_on_interval(start_date, end_date, worker_id)

        if schedule_data:
            return jsonify(schedule_data)
        else:
            return jsonify({'error': 'Расписание не найдено'}), 404
    except Exception as e:
        return jsonify({'error': 'Произошла ошибка при получении расписания'}), 500

@blueprint.route('/statistic', methods=['POST'])
def statistic():


    data = {'ТУТ': 'ПОКА', 'НЕ': 'ГОТОВО'}

    return jsonify(data)

@blueprint.route('/task_сompleted', methods=['POST'])
def task_сompleted():
    data = request.get_json()   # data = {"task_idt": "305620464419692773492314257386895579457", "task_comm": "Привет, как дела?"}
    try:
        idt = data.get("task_idt")
        comm = data.get("task_comm")
        if save_task_completed(idt, comm):
            return jsonify({'message': 'Результат сохранен'})
        else:
            return jsonify({'error': 'Ошибка сохранения результата в БД'}), 404
    except Exception as e:
        return jsonify({'error': 'Произошла ошибка при сохранении результата'}), 500

@blueprint.route('/task_failed', methods=['POST'])
def task_failed():
    data = request.get_json()   # data = {"task_idt": "305620464419692773492314257386895579457", "task_comm": "Привет, как дела?"}
    try:
        idt = data.get("task_idt")
        comm = data.get("task_comm")
        if save_task_completed(idt, comm):
            return jsonify({'message': 'Результат сохранен'})
        else:
            return jsonify({'error': 'Ошибка сохранения результата в БД'}), 404
    except Exception as e:
        return jsonify({'error': 'Произошла ошибка при сохранении результата'}), 500

@blueprint.route('/task_notification', methods=['POST'])                        # Скорее всего надо реализовать не тут
def task_notification():                                                        # (или как-то передавать потом на веб)


    data = {'ТУТ': 'ПОКА', 'НЕ': 'ГОТОВО'}

    return jsonify(data)
