# EasyShifts

## Introduction

EasyShifts is a comprehensive web application designed to streamline the scheduling and shift management process for workplaces operating on a shift-based system. This platform empowers managers to effortlessly handle schedules, assign shifts, and manage employee requests, all within a centralized and user-friendly interface. Employees, on the other hand, can conveniently view their upcoming shifts, submit shift requests, and stay informed about their schedules.

https://github.com/AlonMesh/EasyShifts/assets/97172662/a2ec1f9e-c905-48a0-8183-463563874dac

## Features

- **User Authentication**: Secure registration and login system for managers and employees.
- **Shift Scheduling**: Managers can create, modify, and assign shifts to employees based on availability and requirements.
- **Shift Requests**: Employees can submit requests for specific shifts or indicate their unavailability.
- **Shift Board**: A visual representation of the shift schedule, allowing managers to easily view and adjust assignments.
- **Employee Management**: Managers can approve or reject new employee registrations for their workplaces.
- **Shift Viewing**: Employees can view their assigned shifts for upcoming dates.

## Table of Contents
* [Project Structure](#project-structure)
* [Installation](#installation)
* [Running the Application](#running-the-application)
* [Usage](#usage)
* [Authors](#authors)


## Project Structure

The frontend of EasyShifts is built using React, while the backend is implemented in Python. The backend server listens for incoming requests from the frontend and interacts with a MySQL database.

### Database

The database consists of six tables, each serving a specific purpose:

1. **Users**: Stores user information, including roles (manager or employee).
2. **Workplaces**: Maintains information about workplaces and their associated users.
3. **UserRequests**: Keeps track of shift requests submitted by employees.
4. **Shifts**: Stores shift details, such as start and end times, dates, and associated workplaces.
5. **ShiftWorkers**: Links users to assigned shifts, enabling tracking of shift assignments.
6. **ShiftBoard**: Handles the shift board data, allowing managers to view and manage shifts based on dates and workplaces.

The database follows a model-repository-service-controller pattern.

## Installation

To set up the EasyShifts application locally, follow these steps:

### Backend Setup

1. Clone the repository: 
```bash
git clone https://github.com/AlonMesh/EasyShifts.git
```
2. Navigate to the project directory: `cd easyshifts`

This project is dependent on `sqlalchemy`, `pymysql`, and `websockets`. To install the required packages, run the following command:

```bash
pip install -r Backend/requirements.txt
```

### Frontend Setup

1. Navigate to the frontend directory: `cd App`
2. Install the required dependencies: `npm install`


## Running the Application

### Backend

1. Ensure that the virtual environment is activated.
2. Navigate to the backend directory: `cd Backend`
3. Run the backend server: `python Server.py`

### Frontend

1. Navigate to the frontend directory: `cd app`
2. Start the React development server: `npm start`
3. The application will be accessible at `http://localhost:3000` in your web browser.

## Usage

Once the application is running, you can access the EasyShifts platform through your web browser. Managers can log in and start managing workplaces, schedules, and employee requests. Employees can register, view their shifts, and submit shift requests.
