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

public class Controller {

    private Stage stage;
    private Scene scene;
    private Parent root;
    private boolean isFreeMotion = false;

    private Socket socket = connectionController.getSocket();
    private IOCommands io = connectionController.getIoCommands();

    @FXML
    private Button freeMotionButton;
    @FXML
    private TextField ipField;
    @FXML
    private TextField portField;
    @FXML
    private Label connectionError;
    @FXML
    private Button manualModeButton;
    @FXML
    private TextField axe1TextField;
    @FXML
    private TextField axe2TextField;
    @FXML
    private TextField axe3TextField;
    @FXML
    private TextField axe4TextField;
    @FXML
    private TextField axe5TextField;
    @FXML
    private TextField axe6TextField;
     
    /* 
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
        
        
    }*/

    public void switchToConnectionScene(ActionEvent event) throws Exception
    {
        
        Parent root = FXMLLoader.load(getClass().getResource("/connect.fxml"));
        stage = (Stage)((Node)event.getSource()).getScene().getWindow();
        scene = new Scene(root);
        stage.setScene(scene);
        stage.show();
    }

    public void switchFreeMotion()
    {
        isFreeMotion = !isFreeMotion;
        if(isFreeMotion)
        {
            freeMotionButton.setStyle("-fx-background-color: #83e604;");
            io.toNetwork("0");
        }
        else
        {
            freeMotionButton.setStyle("-fx-background-color: #d22602;");
            io.toNetwork("1");
        }
        System.out.println(isFreeMotion);

    }

    public void recordPosition()
    {
        io.toNetwork("2");
    }

    public void resetIndexPosition()
    {
        io.toNetwork("3");
    }

    public void sendCoord()
    {
        String data = axe1TextField.getText() + "/" + axe2TextField.getText() + "/" + axe3TextField.getText() + "/" + axe4TextField.getText() + "/" + axe5TextField.getText() + "/" + axe6TextField.getText();
        System.out.println(data);
        io.toNetwork(data);

    }

    public void moveRecordedPositions()
    {
        if(!isFreeMotion)
        {
            switchFreeMotion();
        }
        io.toNetwork("4");
    }
}
