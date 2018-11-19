'''


'''
from IPCMS import db


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    task_code = db.Column(db.String(80))
    task_name = db.Column(db.String(255))
    early_end_date = db.Column(db.DateTime)
    early_start_date = db.Column(db.DateTime)
    remain_drtn_hr_cnt = db.Column(db.Integer)
    target_drtn_hr_cnt = db.Column(db.Integer)


    def __init__(self, task_code, task_name, early_end_date, early_start_date, remain_drtn_hr_cnt, target_drtn_hr_cnt):
        self.task_code = task_code
        self.task_name = task_name
        self.early_end_date = early_end_date
        self.early_start_date = early_start_date
        self.remain_drtn_hr_cnt = remain_drtn_hr_cnt
        self.target_drtn_hr_cnt = target_drtn_hr_cnt