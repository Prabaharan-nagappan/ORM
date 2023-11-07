# Import necessary modules
from sqlalchemy import create_engine, Column, Integer, String, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a database connection (replace with your actual database URL)
engine = create_engine('sqlite:///my_database.db')  # Use a persistent database

Base = declarative_base()

# Define the Task model
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)

# Create the table in the database (with error handling for existing table)
try:
    Base.metadata.create_all(engine)
except Exception as e:
    print(f"Error creating table: {e}")

# Function to create a new task with error handling
def create_task(title, description):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        new_task = Task(title=title, description=description)
        session.add(new_task)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error creating task: {e}")
    finally:
        session.close()

# Function to read tasks with error handling
def read_tasks():
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        tasks = session.query(Task).all()
    except Exception as e:
        print(f"Error reading tasks: {e}")
        tasks = []
    finally:
        session.close()

    return tasks

# Function to search tasks by title or description with error handling
def search_tasks(search_query):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        search_results = session.query(Task).filter(
            or_(Task.title.ilike(f'%{search_query}%'), Task.description.ilike(f'%{search_query}%'))
        ).all()
    except Exception as e:
        print(f"Error searching tasks: {e}")
        search_results = []
    finally:
        session.close()

    return search_results

# Function to update a task with error handling
def update_task(task_id, new_title, new_description):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        task_to_update = session.query(Task).filter_by(id=task_id).first()
        if task_to_update:
            task_to_update.title = new_title
            task_to_update.description = new_description
            session.commit()
        else:
            print(f"Task with ID {task_id} not found.")
    except Exception as e:
        session.rollback()
        print(f"Error updating task: {e}")
    finally:
        session.close()

# Function to delete a task with error handling
def delete_task(task_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        task_to_delete = session.query(Task).filter_by(id=task_id).first()
        if task_to_delete:
            session.delete(task_to_delete)
            session.commit()
        else:
            print(f"Task with ID {task_id} not found.")
    except Exception as e:
        session.rollback()
        print(f"Error deleting task: {e}")
    finally:
        session.close()

# Example usage of the functions
if __name__ == "__main__":
    # Create tasks with error handling
    create_task("Task 1", "This is the first task")
    create_task("Task 2", "This is the second task")

    # Read tasks with error handling
    tasks = read_tasks()
    for task in tasks:
        print(f"Task {task.id}: {task.title} - {task.description}")

    # Search for tasks with error handling
    search_query = "task"
    search_results = search_tasks(search_query)
    print(f"Search results for '{search_query}':")
    for task in search_results:
        print(f"Task {task.id}: {task.title} - {task.description}")

    # Update a task with error handling
    update_task(1, "Updated Task 1", "This task has been updated")

    # Delete a task with error handling
    delete_task(2)

    # Read tasks after the update and delete with error handling
    tasks = read_tasks()
    for task in tasks:
        print(f"Task {task.id}: {task.title} - {task.description}")

# Note: In a real-world project, you would need to handle more complex structures, validate input, and implement more robust error handling.
