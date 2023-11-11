
from apps import db
from apps.api.models import Worker, Tasks, Schedule, Full_tasks, Points
from datetime import datetime, timedelta, date
from sqlalchemy import text, case, select, create_engine

import json
import os
import hashlib
import binascii


def verify_pass(provided_password, stored_password):

    stored_password = stored_password.decode('ascii')
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def get_schedule_for_worker_on_day(date, worker_id):
    # print(date, worker_id)
    schedule_record = db.session.query(Schedule).filter_by(date=date).first()
    # print('sched', schedule_record)
    if schedule_record:
        schedule_data = {}
        task_data = {}
        json_data = json.loads(schedule_record.schedule)
        id_worker = str(worker_id)
        # print(json_data[id_worker]['schedule'])
        worker_schedule = json_data[id_worker]['schedule']
        for interval, idt in worker_schedule.items():
            task = db.session.query(Full_tasks).filter_by(idt=idt).first()
            # print('task', task)
            if task:
                idt = task.idt
                task_type = task.task_type
                task_lead_time = ((db.session.query(Tasks).filter_by(type=task_type).first())).lead_time
                task_title = task.task_title
                task_priority = task.task_priority
                point_id = task.point_id
                # print(vars(db.session.query(Points).filter_by(address=task.point_address).first()))
                point_address = (db.session.query(Points).filter_by(address=task.point_address).first()).address_text
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
            print(schedule_data)
        return schedule_data
    else:
        return None


def get_schedule_for_worker_on_interval(start_date, end_date, worker_id):
    schedule_data = {}

    schedule_records = db.session.query(Schedule).filter(
        Schedule.date >= start_date.strftime("%Y_%m_%d"),
        Schedule.date <= end_date.strftime("%Y_%m_%d")
    ).all()
    # print(schedule_records)
    for schedule_record in schedule_records:
        json_data = json.loads(schedule_record.schedule)
        # print('JSON', json_data)
        if str(worker_id) in json_data:
            worker_schedule = json_data[str(worker_id)]['schedule']
            # print('WORKER_SHED')
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

def save_task_completed(idt, comm):
    row_to_update = db.session.query(Full_tasks).filter(Full_tasks.idt == str(idt)).first()
    if row_to_update:
        row_to_update.status = 'finish'
        row_to_update.comment = comm
        db.session.commit()
        return True
    else:
        return False

def task_failed(idt, comm):
    row_to_update = db.session.query(Full_tasks).filter(Full_tasks.idt == str(idt)).first()
    if row_to_update:
        row_to_update.status = 'problem'
        row_to_update.comment = comm
        db.session.commit()
        return True
    else:
        return False