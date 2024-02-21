from enum import Enum
import cqc_cpcc.attendance as AT
import cqc_cpcc.project_feedback as PF

class Instructor_Actions(Enum):
    TAKE_ATTENDANCE = 1
    GIVE_FEEDBACK = 2
    GRADE_EXAM = 3



def prompt_action():
    """Prompts the user to select a value from the given enum."""
    enum = Instructor_Actions

    print("Which action would you like to take?")
    for i, member in enumerate(enum):
        print(f"{member.value}: {member.name}")

    default = Instructor_Actions.GIVE_FEEDBACK.value
    user_input = int(input('Enter your selection [' + str(default) + ']: ').strip() or default)

    try:
        ia = Instructor_Actions(user_input)
        print(f"You selected {ia.name}")
        return ia
    except ValueError:
        print("Invalid selection.")
        return prompt_action()

def take_action():
    action = prompt_action()
    match action:
        case Instructor_Actions.TAKE_ATTENDANCE:
            AT.take_attendance()
        case Instructor_Actions.GIVE_FEEDBACK:
            PF.give_project_feedback()
        case Instructor_Actions.GRADE_EXAM:
            # TODO: Complete Exam Grading implementation
            print("Needs implementation")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    take_action()


