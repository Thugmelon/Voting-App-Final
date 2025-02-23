import java.util.Scanner;
import java.io.File;
import java.io.PrintWriter;

/**
 * Manages votes and shows results
 */
public class VoteSystem {
    // List of actors to vote for
    private String[] candidates = {"Leonardo DiCaprio", "Marlon Brando", "Johnny Depp", "Christian Bale"};
    // Array to store vote counts
    private int[] votes = new int[candidates.length];
    // Store voter IDs (fixed size to keep it simple)
    private String[] voterIds = new String[100];
    private int totalVoters = 0; // Track number of voters

    /**
     * Loads votes from file when starting
     */
    public VoteSystem() {
        loadVotes(); // Load saved votes at the start
    }

    /**
     * Records a vote
     */
    public void castVote() {
        Scanner input = new Scanner(System.in);
        System.out.print("Enter your ID: ");
        String voterId = input.nextLine();

        // Check if this ID already voted
        for (int i = 0; i < totalVoters; i++) {
            if (voterIds[i].equals(voterId)) {
                System.out.println("You already voted.");
                return;
            }
        }

        // Show actors and get the vote
        System.out.println("Choose your favorite actor:");
        for (int i = 0; i < candidates.length; i++) {
            System.out.println((i + 1) + ". " + candidates[i]);
        }
        System.out.print("Enter your choice (1-4): ");
        String choice = input.nextLine();

        // Convert choice to number
        int choiceIndex = Integer.parseInt(choice) - 1; // I think this should work fine

        // Check if the choice is valid and record the vote
        if (choiceIndex >= 0 && choiceIndex < candidates.length) {
            votes[choiceIndex]++;
            voterIds[totalVoters] = voterId;
            totalVoters++;
            saveVotes(); // Save the new vote to the file
            System.out.println("Vote recorded for " + candidates[choiceIndex]);
        } else {
            System.out.println("Invalid choice."); // If the number isn't 1-4
        }
    }

    /**
     * Shows vote counts
     */
    public void showResults() {
        System.out.println("\n--- Vote Counts ---");
        for (int i = 0; i < candidates.length; i++) {
            System.out.println(candidates[i] + ": " + votes[i] + " votes");
        }
    }

    /**
     * Loads votes from file
     */
    private void loadVotes() {
        // Load saved votes from the file
        File file = new File("votes.txt");
        if (file.exists()) { // Check if the file is there
            Scanner fileInput;
            try {
                fileInput = new Scanner(file);
                while (fileInput.hasNextLine()) {
                    String line = fileInput.nextLine();
                    String[] parts = line.split(":"); // Split ID and vote
                    voterIds[totalVoters] = parts[0];
                    // I’m not sure if this is the best way to do it, but it works
                    int voteIndex = Integer.parseInt(parts[1]);
                    votes[voteIndex]++;
                    totalVoters++;
                }
                fileInput.close(); // Close the file when done
            } catch (Exception e) {
                System.out.println("Problem loading votes. Not sure why, but it failed.");
            }
        }
    }

    /**
     * Saves votes to file
     */
    private void saveVotes() {
        // Save all the votes to the file
        try {
            PrintWriter fileOutput = new PrintWriter("votes.txt");
            for (int i = 0; i < totalVoters; i++) {
                // This is a bit repetitive, but it keeps it simple
                for (int j = 0; j < candidates.length; j++) {
                    fileOutput.println(voterIds[i] + ":" + j);
                }
            }
            fileOutput.close(); // Close the file
        } catch (Exception e) {
            System.out.println("Problem saving votes. I’m not sure why.");
        }
    }
}
