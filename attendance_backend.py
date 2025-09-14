import os

PRESENT_FILE = "present.txt"
ABSENT_FILE = "absent.txt"

# Initialize attendance files (fresh start)
def reset_attendance(total_students=58):
    with open(PRESENT_FILE, "w") as f:
        pass  # empty
    with open(ABSENT_FILE, "w") as f:
        for i in range(1, total_students + 1):
            f.write(f"{i}\n")

# Call reset on import so every run starts fresh
reset_attendance()

def mark_present(roll_number):
    roll_number = str(roll_number)
    with open(PRESENT_FILE, "r") as f:
        present_students = set(f.read().splitlines())

    if roll_number not in present_students:
        present_students.add(roll_number)
        with open(PRESENT_FILE, "w") as f:
            f.write("\n".join(sorted(present_students, key=lambda x: int(x))))

        # Remove from absent
        with open(ABSENT_FILE, "r") as f:
            absent_students = set(f.read().splitlines())
        if roll_number in absent_students:
            absent_students.remove(roll_number)
        with open(ABSENT_FILE, "w") as f:
            f.write("\n".join(sorted(absent_students, key=lambda x: int(x))))


def get_present_students():
    if not os.path.exists(PRESENT_FILE):
        return []
    with open(PRESENT_FILE, "r") as f:
        return f.read().splitlines()
