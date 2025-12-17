# Flask Todo API

A **RESTful backend for managing todos** built with Flask, Flask-SQLAlchemy, Flask-Migrate, and Flask-RESTful.  
**No UI included**—pure API for integration with web or mobile frontends.

## Features

- **CRUD operations** for todos (Create, Read, Update, Delete)
- **SQLite** by default (easy to change via config)
- **Database migrations** via Flask-Migrate
- Clean project structure for easy maintenance
- **Configuration settings** separated in `config.py`
- **Database seeding** using a sample script (to add sample todos)

## Setup

1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure settings**

   Edit `config.py` as needed (you can use environment variables for production secrets):
   ```python
   class Config:
       SQLALCHEMY_DATABASE_URI = "sqlite:///todos.db"  # or use environment variable
       SQLALCHEMY_TRACK_MODIFICATIONS = False
   ```

4. **Set up the database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```
5. **Add sample todos to the database**
   ```bash
   python seed.py
   ```

6. **Run the application**
   ```bash
   python app.py
   ```
   The API will run at `http://localhost:5000`

## API Endpoints

| Method | Endpoint             | Description               |
| ------ | ------------------- | ------------------------- |
| GET    | /todos              | List all todos            |
| POST   | /todos              | Create a new todo         |
| GET    | /todos/<todo_id>    | Get single todo           |
| PUT    | /todos/<todo_id>    | Update todo               |
| DELETE | /todos/<todo_id>    | Delete todo               |

All endpoints accept and return **JSON**.

### Sample Todo JSON

```json
{
  "title": "Sample Task",
  "description": "Do something useful",
  "done": false
}
```

## Project Structure

- **app.py** – App entrypoint
- **config.py** – Configuration file (database URI, settings)
- **models.py** – Database models
- **resources.py** – API endpoint logic
- **extensions.py** – Extensions (SQLAlchemy, Migrate)
- **requirements.txt** – Dependency list
- **seed.py** – Script to add sample todos to the database
- **migrations/** – DB migration scripts

## Customization

- Change `SQLALCHEMY_DATABASE_URI` in `config.py` for another database (e.g. PostgreSQL)
- Expand `config.py` with classes for dev/prod/test environments as needed
- Add authentication or more features as desired

***