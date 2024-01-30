from initializtion import initialize_database_and_session
from controllers import (shifts_controller, shiftWorkers_controller, userRequests_controller,
                         users_controller, workPlaces_controller)


def check_setup():
    db, _ = initialize_database_and_session()

    # Check User creation
    user_data = {
        "username": "LastOne5",
        "password": "123456",
        "isManager": 0,
        "isActive": 1,
        "name": "jon jon"
    }

    # Initialize Controller
    controller = users_controller.UsersController(db)

    created_user = controller.create_entity(entity_data=user_data)
    print("User created:", created_user)

    # Check WorkPlace creation
    workplace_data = {
        "userID": 1,  # Replace with a valid user ID
        "workPlaceID": 1
    }

    # Initialize Controller
    controller = workPlaces_controller.WorkPlacesController(db)

    created_workplace = controller.create_entity(entity_data=workplace_data)
    print("Workplace created:", created_workplace)

    # Check UserRequest creation
    user_request_data = {
        "userID": 1,  # Replace with a valid user ID
        "modifyAt": "2024-01-30T12:00:00",
        "requests": "Vacation"
    }
    # Initialize Controller
    controller = userRequests_controller.UserRequestsController(db)

    created_user_request = controller.create_entity(entity_data=user_request_data)
    print("user_request request created:", created_user_request)

    # Check Shift creation
    shift_data = {
        "workPlaceID": 1,  # Replace with a valid workPlace ID
        "shiftDate": "2024-01-30T08:00:00",
        "shiftPart": "Morning"
    }
    # Initialize Controller
    controller = shifts_controller.ShiftsController(db)

    created_shift = controller.create_entity(entity_data=shift_data)
    print("shift created:", created_shift)

    # Check ShiftWorker creation
    shift_worker_data = {
        "shiftID": 1,
        "userID": 1
    }
    # Initialize Controller
    controller = shiftWorkers_controller.ShiftWorkersController(db)

    created_shift_workers = controller.create_entity(entity_data=shift_worker_data)
    print("shift_worker created:", created_shift_workers)


if __name__ == "__main__":
    check_setup()
