package com.pajet;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.stage.Stage;

import java.net.Socket;

public class connectionController {

    private Stage stage;
    private Scene scene;
    private Parent root;
    private boolean isFreeMotion = false;

    private static Socket socket;
    private static IOCommands io;

    @FXML
    private Button freeMotionButton;
    @FXML
    private TextField ipField;
    @FXML
    private TextField portField;
    @FXML
    private Label connectionError;
    @FXML
    private Label testIP;

    public void switchToMainScene(ActionEvent event) throws Exception
    {
        String ip = ipField.getText();
        int port = Integer.parseInt(portField.getText());
        connectionError.setVisible(false);

        try
        {
            this.socket = new Socket(ip, port);
            this.io = new IOCommands(this.socket);
            Parent root = FXMLLoader.load(getClass().getResource("/software.fxml"));
            stage = (Stage)((Node)event.getSource()).getScene().getWindow();
            scene = new Scene(root);
            stage.setScene(scene);
            stage.show();
            
        }
        catch(Exception e)
        {
            System.err.println("Client creation failed : " + e.getMessage());
            connectionError.setVisible(true);   
        }
        
        
    }

    public static Socket getSocket()
    {
        return socket;
    }

    public static IOCommands getIoCommands()
    {
        return io;
    }
    
}
