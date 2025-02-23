import java.util.Scanner;

/**
 * Main class for the voting app
 */
public class VotingApp {
    public static void main(String[] args) {
        VoteSystem voteSystem = new VoteSystem(); // Manages the voting
        Scanner input = new Scanner(System.in);
        boolean running = true;

        // Main menu loop
        while (running) {
            System.out.println("\n--- Main Menu ---");
            System.out.println("1. Vote for your favorite actor");
            System.out.println("2. View current vote counts");
            System.out.println("3. Quit");
            System.out.print("Enter your choice: ");
            String choice = input.nextLine();

            // User choices
            if (choice.equals("1")) {
                voteSystem.castVote(); // Go to voting
            } else if (choice.equals("2")) {
                voteSystem.showResults(); // Show current votes
            } else if (choice.equals("3")) {
                running = false;
                System.out.println("Goodbye!"); // Ends the program
            } else {
                System.out.println("Invalid choice."); // Wrong input
            }
        }
        input.close(); // Close the scanner
    }
}
