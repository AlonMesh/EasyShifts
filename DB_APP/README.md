## DB APPLICATION (not done yet)

### Requirements:
1. pip install fastapi
2. pip install uvicorn
3. pip install sqlalchemy
4. Must have SQLite3 Install on machine

### Running
On termial `uvicorn books:app --reload` then go to url `127.0.0.1:8000/docs`


### Models
#### Users
```python
    id = Column(Integer, primary_key=True, index=True)  # TODO: Use uuid
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # TODO: Hashing passwords
    isManager = Column(Boolean, nullable=False)
    stillWorks = Column(Boolean, nullable=False)
    # TODO: ADD WORK ID!!!```
```

#### Shifts
```python
    # TBD
```
