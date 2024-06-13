import java.io.IOException;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

public class NewServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String sentence = request.getParameter("sentence");
        String[] words = sentence.split("\\s+");

        // XML yapısına uygun bir şekilde verileri düzenle
        String xmlData = "<root>\n";
        for (int i = 0; i < words.length; i += 3) {
            if (i + 2 < words.length) {
                xmlData += "    <author id=\"" + ((i / 3) + 1) + "\">\n";
                xmlData += "        <name>" + words[i] + "</name>\n";
                xmlData += "        <surname>" + words[i + 1] + "</surname>\n";
                xmlData += "        <book>" + words[i + 2] + "</book>\n";
                xmlData += "    </author>\n";
            }
        }
        xmlData += "</root>";

        
        request.setAttribute("xmlData", xmlData);

        
        request.getRequestDispatcher("/result.jsp").forward(request, response);
    }
}
