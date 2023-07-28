import os
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey
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
                   subject_id=1,
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
                   subject_id=1,
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


checked_subject_name = 'English'

subject_id = (
    session
    .query(Subject.id)
    .filter(Subject.name == checked_subject_name)
    .first()
)[0]
print(subject_id)

subject_students = (
    session
    .query(StudentSubject.student_id)
    .filter(StudentSubject.subject_id == subject_id)
)

print(subject_students.all())

students_names = (
    session
    .query(Student.name)
    .where(Student.id.in_(subject_students))
)

print(students_names.all())
