import java.awt.*;
import javax.swing.*;
import java.awt.event.*;

public class Main {

    public static JFrame jFrame = new JFrame();
    public static JPanel jPanel = new JPanel();
    public static JTextField input = new JTextField();
    public static JButton confrimSearch = new JButton();
    public static JTextArea output = new JTextArea();

    private static void createAndShowGUI() {

        jFrame.setTitle("Bing Search App");
        jFrame.setLayout(null);
        jFrame.setSize(1920, 1080);
        jFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        input.setBounds(100, 50, 200, 50);
        input.setMinimumSize( new Dimension(200,50));
        input.setPreferredSize(new Dimension(200,50));
        jFrame.add(input);

        confrimSearch.setBounds(350, 50,200,50);
        confrimSearch.setText("Search");
        jFrame.add(confrimSearch);

        output.setEditable(false);
        output.setLineWrap(true);
        output.setBounds(100, 150,600,800);
        output.setBackground(Color.white);
        output.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(Color.BLACK),
                BorderFactory.createEmptyBorder(10, 10, 10, 10)));
        jFrame.add(output);
        confrimSearch.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String searchTerm = input.getText();
                output.setText(BingWebSearch.OutputResults(searchTerm));

            }
        });

        jFrame.setVisible(true);
    }

    public static void main(String[] args) {
        createAndShowGUI();
    }
}
