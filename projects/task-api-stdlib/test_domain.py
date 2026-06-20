from app import TaskRepository


def test_task_lifecycle() -> None:
    repo = TaskRepository()
    task = repo.create("Ship a runnable backend lab")
    assert task.status == "open"
    assert repo.complete(task.id).status == "done"


def test_title_validation() -> None:
    repo = TaskRepository()
    try:
        repo.create("x")
    except ValueError as exc:
        assert "title" in str(exc)
    else:
        raise AssertionError("expected validation error")


if __name__ == "__main__":
    test_task_lifecycle()
    test_title_validation()
    print("ok")
