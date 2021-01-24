from sqlalchemy import create_engine, Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

bd = create_engine('sqlite:///todo.db?check_same_thread=False')
def today(): return datetime.today()

Base = declarative_base()
class TaskTable(Base):
	__tablename__ = 'task'
	id = Column(Integer, primary_key=True)
	task = Column(String)
	deadline = Column(Date, default=today())

Base.metadata.create_all(bd)

Session = sessionmaker(bind=bd)
session = Session()

def add_task(task: str, deadline: datetime):
	new_row = TaskTable(task=task, deadline=deadline)
	session.add(new_row)
	session.commit()

def get_tasks():
	rows = session.query(TaskTable).order_by(TaskTable.deadline).all()
	return rows

def get_today_tasks():
	rows = session.query(TaskTable).filter(TaskTable.deadline == today().date()).all()
	return rows

while True:
	print('1) Today\'s tasks'
	      '\n2) Week\'s tasks'
	      '\n3) All tasks'
	      '\n4) Missed tasks'
	      '\n5) Add task'
	      '\n6) Delete task'
	      '\n0) Exit')
	print('> ', end='')
	command = input()
	print()
	if command.isdigit():
		command = int(command)
	else:
		print('Wrong input!')
		continue  # проверка на правильность ввода команды
	if   command == 0:  # выход
		print('Bye!')
		break
	elif command == 1:  # за день
		tasks = get_today_tasks()
		print(f'Today {today().day} {today().strftime("%b")}:')
		if tasks:  # проверка на то, есть ли таски
			for i in range(len(tasks)):
				print(f'{i + 1}. {tasks[i].task}. {tasks[i].deadline.day} {tasks[i].deadline.strftime("%b")}')
			print()
		else:
			print('Nothing to do!')
		print()
	elif command == 2:  # за неделю
		week = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
		# weekday = today().weekday()
		for i in range(7):
			# weekday = (weekday + i) % 7
			day = today().date() + timedelta(days=i)
			tasks = session.query(TaskTable).filter(TaskTable.deadline == day).all()
			print(f'{week[day.weekday()]} {day.day} {day.strftime("%b")}:')
			if tasks:  # проверка на то, есть ли таски
				for l in range(len(tasks)):
					print(f'{l + 1}. {tasks[l].task}')
			else:
				print('Nothing to do!')
			print()


	elif command == 3:  # за всё время
		print('All tasks:')
		tasks = get_tasks()
		if tasks:  # проверка на то, есть ли таски
			for i in range(len(tasks)):
				print(f'{i + 1}. {tasks[i].task}. {tasks[i].deadline.day} {tasks[i].deadline.strftime("%b")}')
			print()
		else:
			print('Nothing to do!')
			print()
	elif command == 4:
		tasks = session.query(TaskTable).filter(TaskTable.deadline < datetime.today().date()).all()
		if tasks:  # проверка на то, есть ли таски
			for i in range(len(tasks)):
				print(f'{i + 1}. {tasks[i].task}. {tasks[i].deadline.day} {tasks[i].deadline.strftime("%b")}')
			print()
		else:
			print('Nothing to do!')
			print()
	elif command == 5:  # добавить таск
		print('Enter task')
		print('> ', end='')
		task = input()
		print('Enter deadline')
		print('> ', end='')
		deadline = datetime(*[int(d) for d in input().split('-')])
		add_task(task, deadline)
		print('The task has been added!')
		print()
	elif command == 6:
		# session.query(TaskTable).filter(TaskTable.date == datetime.today().date()).delete()
		tasks = get_tasks()
		if tasks:  # проверка на то, есть ли таски
			print('Choose the number of the task you want to delete:')
			for i in range(len(tasks)):
				print(f'{i + 1}. {tasks[i].task}. {tasks[i].deadline.day} {tasks[i].deadline.strftime("%b")}')
			print('> ', end='')
			task_to_delete = tasks[int(input()) - 1]
			session.delete(task_to_delete)
			session.commit()
			print('The task has been deleted!')
		else:
			print('Nothing to delete')
			print()

	else: print('Wrong input!')

