package project.RoboticArm.views;

import javafx.collections.ObservableList;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.VBox;

public class MainView extends VBox
{
    public MainView(double spacing)
    {
        super(spacing);

        ObservableList components = this.getChildren();

        Label ip_address_label = new Label("IP Address");
        TextField ip_address_field = new TextField();
        ip_address_field.setPromptText("Enter the Robot IP address");

        Label port_label = new Label("Port");
        TextField port_field = new TextField();
        port_field.setPromptText("Enter the Robot Port");

        Button connexion_button = new Button("Connexion");
        connexion_button.setOnAction(e -> {
            String ip_address = ip_address_field.getText();
            String port = port_field.getText();
            System.out.println("IP Address: " + ip_address);
            System.out.println("Port: " + port);
        });
        

        components.addAll(ip_address_label, ip_address_field, port_label, port_field, connexion_button);
    }
}
