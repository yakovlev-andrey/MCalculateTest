from copy import deepcopy

import pytest

import tests.flower_answers as flower_answers
from worker import plus, minus, multiply, divide


def assert_error_operation_not_valid_exists(error_msg):
    operation_error_exists = False
    for detail in error_msg["detail"]:
        if "operation" in detail["loc"]:
            if "value is not a valid enumeration member" in detail["msg"]:
                operation_error_exists = True
    assert (
        operation_error_exists
    ), f"Error operation not valid not exists. Error: {error_msg}"


@pytest.mark.parametrize("operation", ["+", "-", "*", "/"])
def test_get_calculate_if_all_valid_then_201(test_app, mocker, operation):
    mocker.patch("main.run_calculate_task", return_value=flower_answers.task_created)
    params = {"x": 5, "y": 10, "operation": operation}
    response = test_app.get("/calculate", params=params)
    assert response.status_code == 201
    assert "task_id" in response.json()


@pytest.mark.parametrize("operation", ["+", "-", "*", "/"])
def test_post_calculate_if_all_valid_then_201(test_app, mocker, operation):
    mocker.patch("main.run_calculate_task", return_value=flower_answers.task_created)
    params = {"x": 5, "y": 10, "operation": operation}
    response = test_app.post("/calculate", json=params)
    assert (
        response.status_code == 201
    ), f"{response.status_code} but expected 201, {response.json()}"
    assert "task_id" in response.json()


@pytest.mark.parametrize("operation", ["!", "%", "", "_", "++", "plus"])
def test_get_calculate_if_unsupported_operation_then_422(test_app, operation):
    params = {"x": 5, "y": 10, "operation": operation}
    response = test_app.get("/calculate", params=params)
    assert response.status_code == 422
    assert_error_operation_not_valid_exists(response.json())


@pytest.mark.parametrize("operation", ["!", "%", "", "_", "++", "plus"])
def test_post_calculate_if_unsupported_operation_then_422(test_app, operation):
    """Plus"""
    params = {"x": 5, "y": 10, "operation": operation}
    response = test_app.post("/calculate", json=params)
    assert response.status_code == 422


@pytest.mark.parametrize(
    "x,y", [(2.2, 1), (1, 2.2), ("aa", 1), (1, "aa"), (" ", 23), (23, " ")]
)
def test_post_calculate_if_x_y_not_integer_then_422(test_app, x, y):
    params = {"x": x, "y": y, "operation": "+"}
    response = test_app.post("/calculate", json=params)
    assert response.status_code == 422


@pytest.mark.parametrize(
    "x,y", [(2.2, 1), (1, 2.2), ("aa", 1), (1, "aa"), (" ", 23), (23, " ")]
)
def test_get_calculate_if_x_y_not_integer_then_422(test_app, x, y):
    params = {"x": x, "y": y, "operation": "+"}
    response = test_app.post("/calculate", params=params)
    assert response.status_code == 422


def test_tasks_status(test_app, mocker):
    mocker.patch("flower.flower.tasks", return_value=flower_answers.tasks)
    response = test_app.get("/tasks")
    assert response.status_code == 200


def test_if_task_not_exists_result_is_none(test_app, mocker):
    mocker.patch(
        "flower.flower.task", return_value=deepcopy(flower_answers.task_not_exist)
    )
    response = test_app.get("/tasks/result_is_none").json()
    assert response["result"] is None, response


def test_if_task_not_exists_status_pending(test_app, mocker):
    mocker.patch(
        "flower.flower.task", return_value=deepcopy(flower_answers.task_not_exist)
    )
    response = test_app.get("/tasks/status_pending").json()
    assert response["state"] == "PENDING"


def test_if_task_not_exists_task_id_exist(test_app, mocker):
    answer = deepcopy(flower_answers.task_not_exist)
    answer["task-id"] = "task_id_exist"
    mocker.patch("flower.flower.task", return_value=answer)
    response = test_app.get("/tasks/task_id_exist").json()
    assert response["task_id"] == "task_id_exist"


@pytest.mark.parametrize(
    "x,y,result",
    [
        (2147483647, 1, 2147483648),
        (-1, -1, -2),
        (-5, 5, 0),
        (0, 0, 0),
        (8, -8, 0),
        (22, 44, 66),
    ],
)
def test_plus(x, y, result):
    assert plus.run(x, y) == result


@pytest.mark.parametrize(
    "x,y,result",
    [
        (-2147483647, 1, -2147483648),
        (-1, -1, 0),
        (-5, 5, -10),
        (0, 0, 0),
        (8, -8, 16),
        (22, 44, -22),
    ],
)
def test_minus(x, y, result):
    assert minus.run(x, y) == result


@pytest.mark.parametrize("x,y,result", [(2, 2, 4), (-5, 4, -20), (-4, -4, 16)])
def test_multiply(x, y, result):
    assert multiply.run(x, y) == result


@pytest.mark.parametrize(
    "x,y,result", [(10, 2, 5), (10, 4, 2.5), (100, -10, -10), (-50, -5, 10)]
)
def test_divide(x, y, result):
    assert divide.run(x, y) == result
