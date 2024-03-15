from datetime import datetime
from typing import Union

from cqc_cpcc.project_feedback import *
from cqc_cpcc.utilities.utils import read_file, read_files

ASSIGNMENT = """
Instructions:

IMPORTANT: This is a continuation of the previous part of the project and assumes that you are starting with code that fulfills all requirements from that part of the project.

Write some code that follows the steps below.

Step 1:

    Add some code to display a menu that asks the user to select the resolution of their monitor.  The menu should have the following options:
    
    1280 x 720
    1920 x 1080
    2560 x 1440
    3840 x 2160
    
    Note:  Resolution consists of two numbers separated by an ‘x.’  The first number is the number of pixels in the width of the screen.  The second number is the number of pixels in the height of the screen. We are not asking you to perform multiplication on this step!

Step 2:

    Assign a “multiplier” value (that will be used in a calculation in a later step) based on the monitor resolution by using the following table:
    
    | Resolution  | Multiplier |
    |-------------|------------|
    | 1280 x 720  | 1          |
    | 1920 x 1080 | .75        |
    | 2560 x 1440 | .55        |
    | 3840 x 2160 | .35        |


Step 3:

    Calculate a “performance score” by using the following formula:
    
    Performance Score = ((5 * GPU Clock Speed) + (Number of Cores * CPU Clock Speed)) * Multiplier
    
    Example: A GPU with a clock speed of 1200MHz, a 4-core CPU with a clock speed of 4200 MHz, and a 1280 x 720 resolution monitor would have a Performance Score calculation of:
    
    Performance Score = ((5 * 1200) + (4 * 4200)) * 1 = 22800

Step 4:

    Determine the recommended graphics quality that the hardware can support by using the information in the table below.
    
    | Performance Score                    | Recommended Graphics Quality |
    |--------------------------------------|------------------------------|
    | Over 17,000                          | Ultra                        |
    | Over 15,000 but not more than 17,000 | High                         |
    | Over 13,000 but not more than 15,000 | Medium                       |
    | Over 11,000 but not more than 13,000 | Low                          |
    | 11,000 or less                       | Unable to Play               |

Step 5:

    Create a String object in memory to hold the text “Computer Hardware Graphics Quality Recommendation Tool”.  Display that text at the top of the output (See sample Input and Output below).

Step 6:

    Display the following output (See sample Input and Output below):
    
        The GPU clock speed
        The CPU clock speed
        The number of cores
        The Monitor Resolution (not the menu choice that represents it!)
        The Performance Score (formatted with a comma and to three decimal places)
        The Recommended Graphics Quality

Sample Input and Output (user input is in bold) - The output of your program should match the formatting and spacing exactly as shown

    Please enter the clock speed (in Megahertz) of your graphics card: 1000.0
    
    Please enter the clock speed (in Megahertz) of your processor: 3000.0
    
    Please enter the number of cores of your processor: 2
    
    What is the resolution of your monitor?
    
        1. 1280 x 720
        2. 1920 x 1080
        3. 2560 x 1440
        4. 3840 x 2160
    
    Please select from the options above: 1
    
    Computer Hardware Graphics Quality Recommendation Tool
    
    GPU Clock Speed: 1000.0 MHz
    CPU Clock Speed: 3000.0 MHz
    Number of cores: 2
    Monitor Resolution: 1280 x 720
    Performance Score: 11,000.000
    Recommended Graphics Quality: Unable to Play
"""

SOLUTION = """
package org.example;

import java.text.DecimalFormat;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        DecimalFormat decimalFormat = new DecimalFormat("#,##0.000");

        System.out.print("Please enter the clock speed (in Megahertz) of your graphics card: ");
        double gpuSpeed = scanner.nextDouble();

        System.out.print("Please enter the clock speed (in Megahertz) of your processor: ");
        double cpuSpeed = scanner.nextDouble();

        System.out.print("Please enter the number of cores of your processor: ");
        int cores = scanner.nextInt();

        System.out.println("\nWhat is the resolution of your monitor?\n1. 1280 x 720\n2. 1920 x 1080\n3. 2560 x 1440\n4. 3840 x 2160\nPlease select from the options above: ");

        int resolutionChoice = scanner.nextInt();
        double multiplier = 0;
        String resolution = "";

        switch (resolutionChoice) {
            case 1:
                multiplier = 1;
                resolution = "1280 x 720";
                break;
            case 2:
                multiplier = 0.75;
                resolution = "1920 x 1080";
                break;
            case 3:
                multiplier = 0.55;
                resolution = "2560 x 1440";
                break;
            case 4:
                multiplier = 0.35;
                resolution = "3840 x 2160";
                break;
            default:
                System.out.println("Invalid selection. Exiting program.");
                System.exit(0);
        }

        double performanceScore = ((5 * gpuSpeed) + (cores * cpuSpeed)) * multiplier;
        String recommendedQuality = "Unable to Play";

        if (performanceScore > 17000) {
            recommendedQuality = "Ultra";
        } else if (performanceScore > 15000) {
            recommendedQuality = "High";
        } else if (performanceScore > 13000) {
            recommendedQuality = "Medium";
        } else if (performanceScore > 11000) {
            recommendedQuality = "Low";
        }

        System.out.println("\nComputer Hardware Graphics Quality Recommendation Tool\n");
        System.out.println("GPU Clock Speed: " + gpuSpeed + " MHz");
        System.out.println("CPU Clock Speed: " + cpuSpeed + " MHz");
        System.out.println("Number of cores: " + cores);
        System.out.println("Monitor Resolution: " + resolution);
        System.out.println("Performance Score: " + decimalFormat.format(performanceScore));
        System.out.println("Recommended Graphics Quality: " + recommendedQuality);
    }
}
"""

STUDENT_SUBMISSION = """
import java.util.*;
import java.lang.Math;

class Program {
    private static Scanner input = new Scanner(System.in);

    public static void main(String[] args) {
        int clockSpeedgpu;
        int clockSpeedcpu;
        int cores;
        int gpuInput;
        int cpuInput;
        int coresInput;

        // Step 1: User inputs basic graphics equipment
        System.out.println("Computer Hardware Graphics Quality Recommendation Tool");
        System.out.println("Please enter the clock speed (in Mhz) of your graphics card: ");
        gpuInput = input.nextInt();
        clockSpeedgpu = gpuInput;
        System.out.println("Please enter the clock speed (in Mhz) of your processor: ");
        cpuInput = input.nextInt();
        clockSpeedcpu = cpuInput;
        System.out.println("Please enter the number of cores in your processor: ");
        coresInput = input.nextInt();
        cores = coresInput;

        // Step 2: User inputs monitor resolution
        displayMenu();
        System.out.print("Select the resolution of your monitor (1-4): ");
        int resolutionChoice = getUserChoice(4);
        double resolutionMultiplier = getResolutionMultiplier(resolutionChoice);

        // Step 3: Define the performance score
        double performanceScore = calculatePerformanceScore(clockSpeedgpu, clockSpeedcpu, cores, resolutionMultiplier);

        // Step 4: Define recommended graphics quality
        String recommendedGraphicsQuality = getGraphicsQuality(performanceScore);

        // Step 5: Displaying results
        System.out.println("Computer Hardware Graphics Quality Recommendation Tool");
        System.out.println("GPU Clock Speed: " + gpuInput);
        System.out.println("CPU Clock Speed: " + cpuInput);
        System.out.println("Number of Cores: " + coresInput);   
        System.out.println("Monitor Resolution: " +
                (resolutionChoice == 1 ? "1280 x 720" :
                 resolutionChoice == 2 ? "1920 x 1080" :
                 resolutionChoice == 3 ? "2560 x 1440" :
                 "3840 x 2160"));      
        System.out.printf("Performance Score: %.3f%n", performanceScore);
        System.out.println("Recommended Graphics Quality: " + recommendedGraphicsQuality);
    }

    // Defining and creating performance score equationa and menus
    public static void displayMenu() {
        System.out.println("1. 1280 x 720");
        System.out.println("2. 1920 x 1080");
        System.out.println("3. 2560 x 1440");
        System.out.println("4. 3840 x 2160");
    }

    public static int getUserChoice(int maxChoice) {
        int choice = 0;

        while (choice < 1 || choice > maxChoice) {
            System.out.print("Enter your choice (1-" + maxChoice + "): ");
            if (input.hasNextInt()) {
                choice = input.nextInt();
            } else {
                System.out.println("Invalid input. Please enter a number.");
                input.next(); 
            }
        }

        return choice;
    }

    public static double getResolutionMultiplier(int choice) {
        switch (choice) {
            case 1:
                return 1.0;
            case 2:
                return 0.75;
            case 3:
                return 0.55;
            case 4:
                return 0.35;
            default:
                return 1.0; 
        }
    }

    public static double calculatePerformanceScore(int gpuClockSpeed, int cpuClockSpeed, int numCores, double multiplier) {
        return ((5.0 * gpuClockSpeed) + (numCores * cpuClockSpeed)) * multiplier;
    }

    public static String getGraphicsQuality(double score) {
        if (score > 17000) {
            return "Ultra";
        } else if (score > 15000 && score <= 17000) {
            return "High";
        } else if (score > 13000 && score <= 15000) {
            return "Medium";
        } else if (score > 11000 && score <= 13000) {
            return "Low";
        } else {
            return "Unable to Play";
        }
    }
}
"""

COURSE_NAME = "Java-151"


def give_feedback_on_assignments(assignment_name: str, assignment_instructions_file: str, assignment_solution_file: Union[str, List[str]],
                                 downloaded_exams_directory: str, wrap_code_in_markdown=True):
    # Get the assignment instructions
    assignment_instructions = read_file(assignment_instructions_file)

    # print("Assignment Instructions:\n%s" % assignment_instructions)

    # Get the assignment  solution
    assignment_solution = read_files(assignment_solution_file)

    # print("Assignment Solutions:\n%s" % assignment_solution)

    allowed_file_extensions = (".java"
                               , ".docx"
                               )

    # Get all the files in the current working directory
    files = [file for file in os.listdir(downloaded_exams_directory) if file.endswith(allowed_file_extensions)]

    time_stamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    # Loop through every file in directory and grade the assignment saved to a file
    for file in files:
        student_file_name, student_file_extension = os.path.splitext(file)
        student_file_path = downloaded_exams_directory + "/" + file
        student_submission = read_file(student_file_path)

        print("Generating Feedback for: %s" % student_file_name)
        feedback_guide = get_feedback_guide(assignment=assignment_instructions,
                                            solution=assignment_solution,
                                            student_submission=student_submission,
                                            course_name=COURSE_NAME,
                                            wrap_code_in_markdown=wrap_code_in_markdown)

        feedback = "\n".join([str(x) for x in feedback_guide.all_feedback])

        pre_feedback = "Good job submitting your assignment. "
        if len(feedback) > 0:
            pre_feedback = pre_feedback + "Here is my feedback:\n\n"
        else:
            pre_feedback = pre_feedback + "I find no issues with your submission. Keep up the good work!"
        post_feedback = "\n\n" + FEEDBACK_SIGNATURE
        print("\n\n" + pre_feedback + feedback + post_feedback)

        file_path = f"./logs/{assignment_name}_{student_file_name}-{model}_temp({str(temperature)})-{time_stamp}.txt".replace(
            " ", "_")

        feedback_guide.save_feedback_to_docx(file_path.replace(".txt", ".docx"), pre_feedback, post_feedback)

        f = open(file_path, "w")
        f.write(pre_feedback + feedback + post_feedback)
        f.close()
        print("Feedback saved to : %s" % file_path)


if __name__ == '__main__':
    give_feedback_on_assignments(
        assignment_name="CSC151-N853-ProjectPart5",
        assignment_instructions_file="/Users/christopherqueen/Google Drive/CPCC/CPCC_Task_Automation/downloads/CSC151-N853/ProjectPart5/ProjectPart5_Instructions.docx",
        assignment_solution_file=["/Users/christopherqueen/Google Drive/CPCC/CPCC_Task_Automation/downloads/CSC151-N853/ProjectPart5/Project5_Solution.java",
                                  "/Users/christopherqueen/Google Drive/CPCC/CPCC_Task_Automation/downloads/CSC151-N853/ProjectPart5/HardwareLastname.java"],
        downloaded_exams_directory="/Users/christopherqueen/Google Drive/CPCC/CPCC_Task_Automation/downloads/CSC151-N853/ProjectPart5/submissions_all",
        wrap_code_in_markdown=True
    )
