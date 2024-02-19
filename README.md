# EasyShifts

EasyShifts is a platform designed to simplify shift management for workplaces that operate on a shift-based system, such as restaurants, security companies, and hospitals. The goal is to streamline communication and scheduling processes for both workers and managers.

## Table of Contents
* [Features](#features)
* [Project Status](#project-status)
* [Project Structure](#project-structure)
* [Installation](#installation)
* [Usage](#usage)
* [Authors](#authors)

## Features
* **Unified Communication** - One platform and one place for all communication.
  * Managers can open (and close) a window for sending requests for shifts.
  * Workers can submit shifts requests easily during the open window.
* **Efficient Scheduling** - Clear and easy-to-use scheduling interface.
  * Requests are visible to managers in real-time alongside the shift scheduling interface.
  * Managers can schedule shifts using a simple board.

## Project Status
The project is currently in development. The frontend is in its early stages and has a simple design. Work is ongoing to enhance and expand its features.

## Project Structure
The project is divided into two main components: the backend and the frontend.

### Frontend
* Implemented in JavaScript.
* Pages for workers and managers interact with the backend using websockets.
* Includes wide functionality for shift requests, shift scheduling, and shift management.

### Backend
* Implemented in Python.
* Includes a server that listens for incoming requests from the frontend.
* Connects to a MySQL database using the `sqlalchemy` library.
* Follows the model-repository-service-controller pattern.

### Database
* **User**
  * Attributes: `id`, `username`, `password`, `isManager`, `isActive`, and `name`.
* **WorkPlace** (Represents a user in the system)
  * Attributes: `id`, `workPlaceID`.
* **UserRequest** (Represents a request for a shift)
  * Attributes:  `id`, `modifyAt`, and `requests`.
* **Shift**
  * Attributes include `id,` `workPlaceID`, `shiftDate`, and `shiftPart`.
* ShiftWorker (Represents all shifts of all workers)
  * Attributes: `userID`, `shiftID`.

## Installation

### Prerequisites

This project requires [Python 3.8](https://www.python.org/downloads/release/python-380/) and [pip](https://pip.pypa.io/en/stable/installing/) to run. 
It is dependent on `sqlalchemy`, `pymysql`, and `websockets`.

To install the required packages, run the following command:

```bash
pip install -r Backend/requirements.txt
```

### Running the Application
Clone the repository:

```bash
git clone https://github.com/your-username/EasyShifts.git
cd EasyShifts
```

## Usage
[Provide instructions on how to use the project. Include examples or commands if applicable.]

## Authors
* [Alon Meshulam](https://github.com/AlonMesh/EasyShifts)
* [Halel Itzhaki](https://github.com/halelitzhaki)
* [Neta Cohen](https://github.com/NetaCohen4)
* [Ori Ekshtein](https://github.com/ori-eksh)
* [Shoval Nahmias](https://github.com/Shovshi)