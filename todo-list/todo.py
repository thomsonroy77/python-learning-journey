
import json
import os

TASKS_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")


def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    return []


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


tasks = load_tasks()

print("=== MY PYTHON TO-DO LIST ===")
print(f"Loaded {len(tasks)} saved task(s).")

def show_tasks():
    if not tasks:
        print("\nYour task list is empty.")
        return

    print("\n=== YOUR TASKS ===")

    for index, task in enumerate(tasks, start=1):
        status = "✓" if task["completed"] else " "
        print(f"{index}. [{status}] {task['title']}")

def add_task():
    title = input("\nEnter your new task: ").strip()

    if not title:
        print("Task cannot be empty.")
        return

    for task in tasks:
        if task["title"].lower() == title.lower():
            print("This task already exists!")
            return

    tasks.append({
        "title": title,
        "completed": False
    })

    save_tasks(tasks)
    print(f"Task added: {title}")
def complete_task():
    show_tasks()

    if not tasks:
        return

    try:
        task_number = int(input("\nEnter the task number to complete: "))

        if task_number < 1 or task_number > len(tasks):
            print("Invalid task number.")
            return

        task = tasks[task_number - 1]

        if task["completed"]:
            print("This task is already completed!")
            return

        task["completed"] = True
        save_tasks(tasks)

        print(f"Task completed: {task['title']}")

    except ValueError:
        print("Please enter a valid number.")


def delete_task():
    show_tasks()

    if not tasks:
        return

    try:
        task_number = int(input("\nEnter the task number to delete: "))

        if task_number < 1 or task_number > len(tasks):
            print("Invalid task number.")
            return

        task = tasks[task_number - 1]

        confirmation = input(
            f"Are you sure you want to delete '{task['title']}'? (y/n): "
        ).strip().lower()

        if confirmation == "y":
            deleted_task = tasks.pop(task_number - 1)
            save_tasks(tasks)
            print(f"Task deleted: {deleted_task['title']}")

        else:
            print("Deletion cancelled.")

    except ValueError:
        print("Please enter a valid number.")
def main():
    while True:
        print("\n=== TO-DO LIST MENU ===")
        print("1. View tasks")
        print("2. Add task")
        print("3. Mark task as completed")
        print("4. Delete task")
        print("5. Exit")

        choice = input("\nChoose an option (1-5): ").strip()

        if choice == "1":
            show_tasks()

        elif choice == "2":
            add_task()

        elif choice == "3":
            complete_task()

        elif choice == "4":
            delete_task()

        elif choice == "5":
            print("Goodbye! Your tasks have been saved.")
            break

        else:
            print("Invalid choice. Please select 1, 2, 3, 4, or 5.")   
if __name__ == "__main__":
    main()


