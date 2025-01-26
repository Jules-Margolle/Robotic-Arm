import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;

public class MainApp extends Application {

    @Override
    public void start(Stage primaryStage) {
        Button button = new Button("Cliquez-moi !");
        button.setOnAction(e -> System.out.println("Bouton cliqué !"));

        StackPane root = new StackPane(button);
        Scene scene = new Scene(root, 400, 300);

        primaryStage.setTitle("JavaFX et Maven");
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
