
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
        // Creat Java object (client) that can call other web servers
        HttpClient client = HttpClient.newHttpClient();

        // Prepare an HTTP GET request to the inventory service.
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("http://localhost:5002/api/inventory/products"))
                .GET()
                .build();

        try {
            // Send the request and wait for the response then store it
            HttpResponse<String> response
                    = client.send(request, HttpResponse.BodyHandlers.ofString());

            // The jackson object that will convert JSON to java object
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

        } catch (Exception e) {
            res.sendError(500, "Unable to load products");
        }
    }
}
