import java.net.Socket;

public class Client 
{
    private Socket socket;
    private IOCommands io;
    
    Client(String ip, int port)
    {
        try
        {
            this.socket = new Socket(ip, port);
            this.io = new IOCommands(this.socket);
        }
        catch(Exception e)
        {
            System.err.println("Client creation failed : " + e.getMessage());   
        }
    }

    void start()
    {
        String data_to_send;
        io.toNetwork("Hello Server");
        io.toScreen(io.fromNetwork());
        do
        {
            data_to_send = io.fromScreen();
            io.toNetwork(data_to_send);
            io.toScreen(io.fromNetwork());
        }while(data_to_send != "close");
    }

    
}
