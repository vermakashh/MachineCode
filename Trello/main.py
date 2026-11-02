from models.user import User
from services.project_manager import ProjectManager
from cli import CLI


def seed_users(manager: ProjectManager):
    users = [
        User("user1", "Gaurav Chandak", "gaurav@workat.tech"),
        User("user2", "Akash Verma", "akash@workat.tech"),
        User("user3", "Sagar Jain", "sagar@workat.tech"),
    ]

    for user in users:
        manager.add_user(user)


def main():
    manager = ProjectManager()
    seed_users(manager)
    cli = CLI(manager)

    print("Project Management CLI")
    print("Enter commands or type EXIT to quit.")

    while True:
        try:
            command = input("> ").strip()

            if command.upper() == "EXIT":
                break

            cli.execute(command)

        except (KeyboardInterrupt, EOFError):
            print()
            break


if __name__ == "__main__":
    main()
