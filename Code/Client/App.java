public class App 
{
    public static void main( String[] args )
    {
        Client client = new Client("127.0.0.1", 12345);
        client.start();
    }
}
