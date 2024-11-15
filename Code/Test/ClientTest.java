import java.io.*;
import java.net.*;

public class ClientTest {
    public static void main(String[] args) {
        String serverAddress = "127.0.0.1";  // Adresse IP du serveur
        int port = 12345;                   // Port du serveur

        try {
            // Connexion au serveur
            Socket socket = new Socket(serverAddress, port);
            System.out.println("Connecté au serveur");

            // Envoyer un message au serveur
            OutputStream output = socket.getOutputStream();
            PrintWriter writer = new PrintWriter(output, true);
            writer.println("Bonjour du client Java!");

            // Recevoir la réponse du serveur
            InputStream input = socket.getInputStream();
            BufferedReader reader = new BufferedReader(new InputStreamReader(input));
            String response = reader.readLine();
            System.out.println("Réponse du serveur : " + response);

            // Fermer la connexion
            socket.close();
        } catch (IOException ex) {
            System.out.println("Erreur : " + ex.getMessage());
            ex.printStackTrace();
        }
    }
}
