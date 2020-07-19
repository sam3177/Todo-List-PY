from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class Menu:
    def ui_input(self):
        a = input()
        self.make(a)

    def __init__(self):
        self.state = 'action'
        self.task_ = ''
        self.today = datetime.today().date()
        self.ui_input()

    def today_task(self):
        print('\nToday {} {}:'.format(self.today.day, self.today.strftime('%b')))
        rows = session.query(Table).filter(Table.deadline == self.today).all()
        if len(rows) == 0:
            print('Nothing to do!')
        else:
            for i in range(len(rows)):
                print('{}. {}'.format(i + 1, rows[i].task))
        print("\n1) Today's tasks\n2) Week's tasks\n3) All tasks")
        print("4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
        return self.ui_input()

    def week_tasks(self):
        print('')
        day_ = self.today
        for i in range(7):
            print('{} {} {}:'.format(day_.strftime('%A'), day_.day, day_.strftime('%b')))
            rows = session.query(Table).filter(Table.deadline == day_).all()
            if len(rows) == 0:
                print('Nothing to do!')
            else:
                for j in range(len(rows)):
                    print('{}. {}'.format(j + 1, rows[j].task))
            print('')
            day_ += timedelta(days=1)
        print("1) Today's tasks\n2) Week's tasks\n3) All tasks")
        print("4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
        return self.ui_input()

    def all_tasks(self):
        print('All tasks:')
        rows = session.query(Table).all()
        if len(rows) == 0:
            print('Nothing to do!')
        else:
            for i in range(len(rows)):
                print('{}. {}'.format(i + 1, rows[i].task))
        print("\n1) Today's tasks\n2) Week's tasks\n3) All tasks")
        print("4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
        return self.ui_input()

    def add_task(self, x):
        new_row = Table(task=self.task_, deadline=datetime(int(x.split('-')[0]), int(x.split('-')[1]), int(x.split('-')[2])))
        session.add(new_row)
        session.commit()
        print("The task has been added!\n")
        print("1) Today's tasks\n2) Week's tasks\n3) All tasks")
        print("4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
        return self.ui_input()

    def missed_tasks(self):
        print('\nMissed tasks:' if self.state == 'action' else '\nChose the number of the task you want to delete:')
        rows = session.query(Table).filter(Table.deadline < datetime.today()).order_by(Table.deadline).all()
        if len(rows) == 0:
            print('Nothing is missed!' if self.state == 'action' else 'Nothing to delete')
        else:
            for i in range(len(rows)):
                print('{}. {} {} {}'.format(i + 1, rows[i].task, rows[i].deadline.day, rows[i].deadline.strftime('%b')))
        if self.state == 'action':
            print("\n1) Today's tasks\n2) Week's tasks\n3) All tasks")
            print("4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
        return self.ui_input()

    def task_del(self, x):
        rows = session.query(Table).filter(Table.deadline < datetime.today()).order_by(Table.deadline).all()
        session.delete(rows[int(x)-1])
        session.commit()
        print('The task has been deleted!')
        print("\n1) Today's tasks\n2) Week's tasks\n3) All tasks")
        print("4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")

        return self.ui_input()

    def make(self, xxx):
        if self.state == 'action':
            if xxx == '1':
                return self.today_task()
            elif xxx == '2':
                return self.week_tasks()
            elif xxx == '3':
                return self.all_tasks()
            elif xxx == '4':
                return self.missed_tasks()
            elif xxx == '5':
                print('\nEnter task')
                self.state = 'add_task'
                return self.ui_input()
            elif xxx == '6':
                self.state = 'delete_task'
                return self.missed_tasks()
            elif xxx == '0':
                print('\nBye!')
                self.state = None
                return None
        elif self.state == 'add_task':
            print('\nEnter deadline')
            self.state = 'add_deadline'
            self.task_ = xxx
            return self.ui_input()
        elif self.state == 'add_deadline':
            self.state = 'action'
            return self.add_task(xxx)
        elif self.state == 'delete_task':
            self.state = 'action'
            return self.task_del(xxx)


print("1) Today's tasks\n2) Week's tasks\n3) All tasks")
print("4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")

todo = Menu()
