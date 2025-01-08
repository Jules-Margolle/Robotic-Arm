package project.RoboticArm;

import javafx.application.Application;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;
import javafx.fxml.FXMLLoader;



/**
 * Hello world!
 *
 */
public class App extends Application
{

    @Override
    public void start(Stage primaryStage) throws Exception
    {
        FXMLLoader loader = new FXMLLoader(getClass().getResource("/project/RoboticArm/test.fxml"));
        Parent root = loader.load();
        Scene scene = new Scene(root);
        primaryStage.setScene(scene);
        primaryStage.setTitle("Application JavaFX avec Maven");
        primaryStage.show();
    }
    public static void main( String[] args )
    {
       launch(args);
    }
}
