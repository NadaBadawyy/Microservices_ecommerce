package servlets;

import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;
import java.io.IOException;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.List;
import java.util.Map;
import java.util.ArrayList;
import java.util.HashMap;

@WebServlet("/CheckoutServlet")
public class CheckoutServlet extends HttpServlet {

    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {

        // Fetch customers and products from APIs (like before)
        HttpClient client = HttpClient.newHttpClient();
        ObjectMapper mapper = new ObjectMapper();

        try {
            // Customers
            HttpRequest customerReq = HttpRequest.newBuilder()
                    .uri(URI.create("http://localhost:5004/api/customers"))
                    .GET().build();
            HttpResponse<String> customerResp = client.send(customerReq, HttpResponse.BodyHandlers.ofString());
            List<Map<String, Object>> customers = mapper.readValue(
                    customerResp.body(),
                    new com.fasterxml.jackson.core.type.TypeReference<List<Map<String,Object>>>(){}
            );
            req.setAttribute("customers", customers);

            // Products
            HttpRequest productReq = HttpRequest.newBuilder()
                    .uri(URI.create("http://localhost:5002/api/inventory/products"))
                    .GET().build();
            HttpResponse<String> productResp = client.send(productReq, HttpResponse.BodyHandlers.ofString());
            List<Map<String, Object>> products = mapper.readValue(
                    productResp.body(),
                    new com.fasterxml.jackson.core.type.TypeReference<List<Map<String,Object>>>(){}
            );
            req.setAttribute("products", products);

            // Forward to checkout.jsp
            req.getRequestDispatcher("checkout.jsp").forward(req, res);

        } catch (Exception e) {
            e.printStackTrace();
            res.sendError(500, "Failed to load checkout page");
        }
    }

    protected void doPost(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {

        // Collect form data
        String customerId = req.getParameter("customer_id");
        String[] productIds = req.getParameterValues("product_id");

        if (productIds == null) {
            res.sendError(400, "No products selected");
            return;
        }

        List<Map<String, Object>> products = new ArrayList<>();
        for (String pid : productIds) {
            String qty = req.getParameter("quantity_" + pid);
            Map<String, Object> item = new HashMap<>();
            item.put("product_id", Integer.parseInt(pid));
            item.put("quantity", Integer.parseInt(qty));
            products.add(item);
        }

        // Store in request and forward to confirmation page
        req.setAttribute("customer_id", customerId);
        req.setAttribute("products", products);
        req.getRequestDispatcher("confirmation.jsp").forward(req, res);
    }
}
