# DB_APP

## Overview

This folder contains the code for a database application that interacts with a **MySQL** database containing 5 models.

## Contents

`main.py` - The main entry point for the application.

`db/`

* `models.py` - Defines the architecture of all database tables.
* `session.py` - manages database sessions by using a context manager and enabling manual transaction/flush control

`routers/` - For entities-related operations (Create, Read, Update and Delete)
* `users.py` - Partly implementation
* `workplace.py` - Partly implementation

`requirements.txt` - Lists the required Python packages.
## Running the Application

Install the required packages:
```Bash
pip install -r requirements.txt
```

Run the application:
```Bash
uvicorn DB_APP.main:app --reload
```

## Model Information

1. **User:** Stores user information (username, password, name, manager status, active status).
2. **WorkPlace:** Associates workplaces with users.
3. **UserRequests:** Captures user shift requests.
4. **Shifts:** Represents shifts, including workplace, date, and part.
5. **ShiftWorkers:** Records shifts assigned to workers.

