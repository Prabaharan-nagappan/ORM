# Import necessary modules
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create an SQLite database in memory for demonstration
engine = create_engine('sqlite:///:memory:')
Base = declarative_base()

# Define the Task model
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)

# Create the table in the database
Base.metadata.create_all(engine)

# Function to create a new task
def create_task(title, description):
    Session = sessionmaker(bind=engine)
    session = Session()

    new_task = Task(title=title, description=description)
    session.add(new_task)
    session.commit()
    session.close()

# Function to read tasks
def read_tasks():
    Session = sessionmaker(bind=engine)
    session = Session()

    tasks = session.query(Task).all()
    session.close()

    return tasks

# Function to update a task
def update_task(task_id, new_title, new_description):
    Session = sessionmaker(bind=engine)
    session = Session()

    task_to_update = session.query(Task).filter_by(id=task_id).first()
    if task_to_update:
        task_to_update.title = new_title
        task_to_update.description = new_description
        session.commit()

    session.close()

# Function to delete a task
def delete_task(task_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    task_to_delete = session.query(Task).filter_by(id=task_id).first()
    if task_to_delete:
        session.delete(task_to_delete)
        session.commit()

    session.close()

# Example usage of the functions
if __name__ == "__main__":
    # Create tasks
    create_task("Task 1", "This is the first task")
    create_task("Task 2", "This is the second task")

    # Read tasks
    tasks = read_tasks()
    for task in tasks:
        print(f"Task {task.id}: {task.title} - {task.description}")

    # Update a task
    update_task(1, "Updated Task 1", "This task has been updated")

    # Delete a task
    delete_task(2)

    # Read tasks after the update and delete
    tasks = read_tasks()
    for task in tasks:
        print(f"Task {task.id}: {task.title} - {task.description}")

