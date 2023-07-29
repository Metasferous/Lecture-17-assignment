import os
from dotenv import load_dotenv
import datetime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Select,
    VARCHAR,
    BOOLEAN,
    FLOAT,
    DATE,
    TEXT,
    func,
    desc,
)

load_dotenv()

DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{database}'

engine = create_engine(
    DATABASE_URI.format(
        host='localhost',
        database='postgres',
        user=os.getenv('user_name'),
        password=os.getenv('password'),
        port=5432
    )
)

Base = declarative_base()


# Task 1
class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    def __str__(self):
        return f'It\' {self.name}. {self.age} years old.'


class Subject(Base):
    __tablename__ = 'subject'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


class StudentSubject(Base):
    __tablename__ = 'student_subject'

    student_id = Column(ForeignKey('student.id'), primary_key=True)
    subject_id = Column(ForeignKey('subject.id'), primary_key=True)
    score = Column(Integer)


students = [
    Student(name='Cthulhu',
            age=100500),
    Student(name='Azathoth',
            age=100500),
    Student(name='Yog-Sothoth',
            age=100500),
    Student(name='Shoggoth',
            age=100500),
]

subjects = [
    Subject(name='English'),
    Subject(name='Math'),
    Subject(name='R\'lyehian'),
    Subject(name='PE'),
    Subject(name='Python'),
]

students_subjects = [
    StudentSubject(student_id=1,
                   subject_id=1,  # English
                   score=5),
    StudentSubject(student_id=1,
                   subject_id=2,
                   score=4),
    StudentSubject(student_id=1,
                   subject_id=3,
                   score=4),
    StudentSubject(student_id=1,
                   subject_id=4,
                   score=4),
    StudentSubject(student_id=2,
                   subject_id=5,
                   score=5),
    StudentSubject(student_id=2,
                   subject_id=2,
                   score=4),
    StudentSubject(student_id=2,
                   subject_id=3,
                   score=3),
    StudentSubject(student_id=2,
                   subject_id=4,
                   score=2),
    StudentSubject(student_id=3,
                   subject_id=2,
                   score=4),
    StudentSubject(student_id=3,
                   subject_id=3,
                   score=1),
    StudentSubject(student_id=3,
                   subject_id=4,
                   score=2),
    StudentSubject(student_id=4,
                   subject_id=1,  # English
                   score=5),
    StudentSubject(student_id=4,
                   subject_id=2,
                   score=3),
    StudentSubject(student_id=4,
                   subject_id=3,
                   score=4),
]


# For testing purpose
Base.metadata.drop_all(engine)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

for student in students:
    session.add(student)
# For testing purpose
print(session.query(Student.name,
                    Student.age,
                    Student.id).all())

for subject in subjects:
    session.add(subject)
# For testing purpose
print(session.query(Subject.name,
                    Subject.id).all())

for student_subject in students_subjects:
    session.add(student_subject)
# For testing purpose
print(session.query(StudentSubject.student_id,
                    StudentSubject.subject_id,
                    StudentSubject.score).all())

# Task 2
checked_subject_name = 'English'

subject_id = (
    session
    .query(Subject.id)
    .filter(Subject.name == checked_subject_name)
    .first()
)[0]

subject_students = (
    session
    .query(StudentSubject.student_id)
    .filter(StudentSubject.subject_id == subject_id)
)

students_names = (
    session
    .query(Student.name)
    .where(Student.id.in_(subject_students))
)

print(students_names.all())


# Task 3
# Sub-task defining tables
class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    nickname = Column(VARCHAR(64), nullable=False)
    user_type = Column(VARCHAR(10), nullable=False)


class Rooms(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    host_id = Column(ForeignKey('users.id'))
    beds = Column(Integer, nullable=False)
    air_conditionind = Column(BOOLEAN)
    price = Column(FLOAT, nullable=False)


class Reservations(Base):
    __tablename__ = 'reservations'

    user_id = Column(ForeignKey('users.id'), primary_key=True)
    room_id = Column(ForeignKey('rooms.id'), primary_key=True)
    settling = Column(DATE, nullable=False, primary_key=True)
    departure = Column(DATE, nullable=False)
    paid = Column(FLOAT, nullable=False)


class Reviews(Base):
    __tablename__ = 'reviews'

    host_id = Column(ForeignKey('users.id'), primary_key=True)
    guest_id = Column(ForeignKey('users.id'), primary_key=True)
    rate = Column(FLOAT, nullable=False)
    text = Column(TEXT)


# Sub-task
# Finding user with max amount of reservations
max_reservations_user_id = (
    session
    .query(Reservations.user_id)
    .group_by(Reservations.user_id)
    .order_by(desc(func.count(Reservations.user_id)))
).first()

user_nickname_and_id = (
    session
    .query(Users.nickname, Users.id)
    .filter(Users.id == max_reservations_user_id[0])
).first()

print(user_nickname_and_id)

# Sub-task
# Findig best rated host
best_rated_host_id = (
    session
    .query(Reviews.host_id)
    .group_by(Reviews.host_id)
    .order_by(desc(func.avg(Reviews.rate)))
).first()

host_nickname_and_id = (
    session
    .query(Users.nickname, Users.id)
    .filter(Users.id == best_rated_host_id[0])
).first()

print(host_nickname_and_id)

# Sub-task
# Finding max income during last month
date_to = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
date_from = date_to.replace(day=1)

max_income_last_month_host_id = (
    session
    .query(
        Users.id
    )
    .filter(Reservations.room_id == Rooms.id)
    .filter(Rooms.host_id == Users.id)
    .filter(
        Reservations.settling >= date_from)
    .filter(
        Reservations.settling <= date_to)
    .group_by(Users.id, Reservations.paid)
    .order_by(desc(Reservations.paid))
).first()

max_income_host_nickname_and_id = (
    session
    .query(Users.nickname, Users.id)
    .filter(Users.id == max_income_last_month_host_id[0])
).first()

print(host_nickname_and_id)
