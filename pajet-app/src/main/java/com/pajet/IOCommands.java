package com.pajet;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;


public class IOCommands 
{
    private BufferedReader screenReader;
    private PrintWriter screenWriter;
    private BufferedReader socketReader;
    private PrintWriter socketWriter;
    

    

    IOCommands()
    {
        
        this.screenReader = new BufferedReader(new InputStreamReader(System.in));
        this.screenWriter = new PrintWriter(System.out, true);
    }

    IOCommands(Socket socket) 
    {
        
        this.screenReader = new BufferedReader(new InputStreamReader(System.in));
        this.screenWriter = new PrintWriter(System.out, true);
        

        

        try
        {
            this.socketReader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            this.socketWriter = new PrintWriter(socket.getOutputStream(), true);
        }
        catch(Exception e)
        {
            System.err.println("[IOCommands Const Socket][ERREUR] " + e.getMessage());
        }
    }

    /*              Screen                   */

    void toScreen(String texte)
    {
        this.screenWriter.println(texte);
    }

    String fromScreen()
    {
        try
        {
            return this.screenReader.readLine();
        }
        catch(Exception e)
        {
            System.err.println("[FROM SCREEN][ERREUR] " + e.getMessage());
            return null;
        }
    }

    /*             Socket                  */

    void toNetwork(String texte)
    {
        this.socketWriter.println(texte);
    }

    String fromNetwork()
    {
        try
        {
            return this.socketReader.readLine();
        }
        catch(Exception e)
        {
            System.err.println("[FROM NETWORK][ERREUR] " + e.getMessage());
            return null;
        }
    }

}
