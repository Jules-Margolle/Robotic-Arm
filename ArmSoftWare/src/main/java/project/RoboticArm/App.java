package project.RoboticArm;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.stage.Stage;
import project.RoboticArm.views.MainView;


/**
 * Hello world!
 *
 */
public class App extends Application
{
    private final String WINDOW_TITLE = "Robotic Arm";
    private final int WINDOW_WIDTH = 1280;
    private final int WINDOW_HEIGHT = 720;

    @Override
    public void start(Stage primaryStage) 
    {
        Scene mainViewScene = new Scene(new MainView(20));

        primaryStage.setScene(mainViewScene);
        primaryStage.setTitle(WINDOW_TITLE);
        primaryStage.setWidth(WINDOW_WIDTH);
        primaryStage.setHeight(WINDOW_HEIGHT); 

        primaryStage.show();
    }
    public static void main( String[] args )
    {
       launch(args);
    }
}
