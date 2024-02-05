from main import initialize_database_and_session
from controllers import (shifts_controller, shiftWorkers_controller, userRequests_controller,
                         users_controller, workPlaces_controller)


def check_setup():
    db, _ = initialize_database_and_session()

    # Check User creation
    user_data = {
        "username": "test_user",
        "password": "test_pass",
        "isManager": 0,
        "isActive": 1,
        "name": "test user"
    }

    # Initialize Controller
    controller = users_controller.UsersController(db)

    created_user = controller.create_entity(entity_data=user_data)
    print("User created:", created_user)

    # Print references to all users
    print("All users:", controller.get_all_entities())

    # Check WorkPlace creation
    workplace_data = {
        "id": 1,
        "workPlaceID": 1
    }

    # Initialize Controller
    controller = workPlaces_controller.WorkPlacesController(db)

    created_workplace = controller.create_entity(entity_data=workplace_data)
    print("Workplace created:", created_workplace)

    # Check UserRequest creation
    user_request_data = {
        "id": 1,
        "modifyAt": "2024-01-30T12:00:00",
        "requests": "Any request..."
    }
    # Initialize Controller
    controller = userRequests_controller.UserRequestsController(db)

    created_user_request = controller.create_entity(entity_data=user_request_data)
    print("user_request request created:", created_user_request)

    # Check Shift creation
    shift_data = {
        "workPlaceID": 1,
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
