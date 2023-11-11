
from apps import db


class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)  #
    FIO = db.Column(db.String(80), unique=True, nullable=False)  # фио
    location = db.Column(db.String(80), nullable=False)  # адрес локации
    grade = db.Column(db.String(80), nullable=False)  # грейд
    location_text = db.Column(db.String(80), nullable=False)


class Tasks(db.Model):
    type = db.Column(db.Integer, primary_key=True)  # тип
    title = db.Column(db.String(100), nullable=False)  # название
    priority = db.Column(db.String(30), nullable=False)  # приоритет
    lead_time = db.Column(db.Float, nullable=False)  # время
    condition = db.Column(db.String(120), nullable=False)  # условие
    level = db.Column(db.String(30), nullable=False)  # требуемый уровень сотрудника


class Points(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # номер точки
    address = db.Column(db.String(100), nullable=False)  # адрес точки
    connected = db.Column(db.String(80), nullable=False)  # когда подключена точка
    delivered = db.Column(db.Boolean, default=False)  # карты и материалы доставлены
    days_last_card = db.Column(db.Integer)  # кол-во дней после выдачи последней карты
    num_approved_app = db.Column(db.Integer)  # кол-во одобренных заявок
    num_card = db.Column(db.Integer)  # кол-во выданных карт
    address_text = db.Column(db.String(100), nullable=False)
    delivered_text = db.Column(db.String(10), nullable=False)


class Undistr_tasks(db.Model):
    idt = db.Column(db.String(100), primary_key=True)
    task_type = db.Column(db.Integer, nullable=False)  # тип задачи
    task_title = db.Column(db.String(100), nullable=False)  # название задачи
    task_priority = db.Column(db.String(30), nullable=False)  # приоритет задачи
    task_lead_time = db.Column(db.Float, nullable=False)  # время выполнения задачи
    task_level = db.Column(db.String(30), nullable=False)  # требуемый уровень сотрудника для выполнения задачи
    point_id = db.Column(db.Integer, nullable=False)  # номер точки
    point_address = db.Column(db.String(100), nullable=False)  # адрес точки
    date = db.Column(db.String(10), nullable=False)  # дата создания задачи


class Full_tasks(db.Model):
    idt = db.Column(db.String(100), primary_key=True)
    task_type = db.Column(db.Integer, nullable=False)  # тип задачи
    task_title = db.Column(db.String(100), nullable=False)  # название задачи
    task_priority = db.Column(db.String(30), nullable=False)  # приоритет задачи
    task_lead_time = db.Column(db.Float,
                               nullable=False)  # время выполнения задачи + время в пути (если задача уже назначена)
    task_level = db.Column(db.String(30), nullable=False)  # требуемый уровень сотрудника для выполнения задачи
    point_id = db.Column(db.Integer, nullable=False)  # номер точки
    point_address = db.Column(db.String(100), nullable=False)  # адрес точки
    date = db.Column(db.String(10), nullable=False)  # дата создания задачи
    status = db.Column(db.String(10), nullable=False)  # статус задачи ('finish' - завершена,
    comment = db.Column(db.String(100))  # 'active' - в расписании сотрудника,
    worker_id = db.Column(db.Integer)  # 'wait' - в очереди,
    # 'problem' - имеются проблемы с задачей)


class Worker_last_location(db.Model):
    id = db.Column(db.Integer, primary_key=True)  #
    last_location = db.Column(db.String(80), nullable=False)  # адрес последней локации


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)  # дата в формате 'гггг_мм_дд'
    schedule = db.Column(db.LargeBinary, nullable=False)  # JSON данные как BLOB


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True)
    role = db.Column(db.String(64), unique=True)
    worker_FIO = db.Column(db.Integer)
    password = db.Column(db.LargeBinary)