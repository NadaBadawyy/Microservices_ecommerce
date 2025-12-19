
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import jakarta.servlet.RequestDispatcher;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@WebServlet("/ProductServlet")
public class ProductServlet extends HttpServlet {

    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws IOException {

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:5002/api/inventory/products"))
                .GET()
                .build();

        try {
            HttpResponse<String> response
                    = client.send(request, HttpResponse.BodyHandlers.ofString());

            ObjectMapper mapper = new ObjectMapper();

            // Parse JSON directly into List<Map>
            List<Map<String, Object>> products = mapper.readValue(
                    response.body(),
                    new TypeReference<List<Map<String, Object>>>() {
            }
            ); 

            // Set as request attribute
            req.setAttribute("products", products);

            // Forward to JSP
            RequestDispatcher rd = req.getRequestDispatcher("index.jsp");
            rd.forward(req, res);

            System.out.println("Products JSON: " + response.body());
            System.out.println("Parsed List<Map>: " + products);

        } catch (Exception e) {
            res.sendError(500, "Unable to load products");
        }
    }
}
