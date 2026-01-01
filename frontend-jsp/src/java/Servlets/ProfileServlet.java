package servlets;

import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.servlet.*;
import jakarta.servlet.http.*;
import jakarta.servlet.annotation.*;
import java.io.IOException;
import java.net.URI;
import java.net.http.*;
import java.util.*;

@WebServlet("/ProfileServlet")
public class ProfileServlet extends HttpServlet {

    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {

        HttpClient client = HttpClient.newHttpClient();
        ObjectMapper mapper = new ObjectMapper();

        try {
            // 1️⃣ Load all customers for the dropdown
            HttpRequest customerReq = HttpRequest.newBuilder()
                    .uri(URI.create("http://localhost:5004/api/customers"))
                    .GET().build();

            HttpResponse<String> customerResp = client.send(customerReq, HttpResponse.BodyHandlers.ofString());

            List<Map<String, Object>> customers = mapper.readValue(
                    customerResp.body(),
                    new com.fasterxml.jackson.core.type.TypeReference<List<Map<String, Object>>>() {
            }
            );

            req.setAttribute("customers", customers);

            // 2️⃣ Selected customer
            String customerId = req.getParameter("customer_id");
            if (customerId != null && !customerId.isEmpty()) {
                req.setAttribute("selectedCustomerId", Integer.parseInt(customerId));

                Map<String, Object> selectedCustomer = null;
                for (Map<String, Object> c : customers) {
                    if (String.valueOf(c.get("customer_id")).equals(customerId)) {
                        selectedCustomer = c;
                        break;
                    }
                }
                req.setAttribute("customer", selectedCustomer);
            }

            // 3️⃣ Determine page type
            String page = req.getParameter("page");
            if ("history".equals(page) || "orderDetails".equals(page)) {

                // Load order history for selected customer
                if (customerId != null && !customerId.isEmpty()) {
                    HttpRequest historyReq = HttpRequest.newBuilder()
                            .uri(URI.create("http://localhost:5001/api/orders?customer_id=" + customerId))
                            .GET().build();

                    HttpResponse<String> historyResp = client.send(historyReq, HttpResponse.BodyHandlers.ofString());
                    List<Map<String, Object>> history = mapper.readValue(
                            historyResp.body(),
                            new com.fasterxml.jackson.core.type.TypeReference<List<Map<String, Object>>>() {
                    }
                    );

                    req.setAttribute("orderHistory", history);
                }

                // Load specific order details if order_id is provided
                String orderId = req.getParameter("order_id");
                // After fetching orderDetails from API
                if (orderId != null && !orderId.isEmpty()) {
                    HttpRequest orderReq = HttpRequest.newBuilder()
                            .uri(URI.create("http://localhost:5001/api/orders/" + orderId))
                            .GET().build();

                    HttpResponse<String> orderResp = client.send(orderReq, HttpResponse.BodyHandlers.ofString());
                    Map<String, Object> orderDetails = mapper.readValue(
                            orderResp.body(),
                            new com.fasterxml.jackson.core.type.TypeReference<Map<String, Object>>() {
                    }
                    );

                    // Fetch all products to map IDs to names
                    HttpRequest productsReq = HttpRequest.newBuilder()
                            .uri(URI.create("http://localhost:5002/api/inventory/products"))
                            .GET().build();
                    HttpResponse<String> productsResp = client.send(productsReq, HttpResponse.BodyHandlers.ofString());
                    List<Map<String, Object>> productsList = mapper.readValue(
                            productsResp.body(),
                            new com.fasterxml.jackson.core.type.TypeReference<List<Map<String, Object>>>() {
                    }
                    );

                    // Create a map product_id -> product_name
                    Map<Integer, String> productNames = new HashMap<>();
                    for (Map<String, Object> p : productsList) {
                        int pid = (int) p.get("product_id");
                        String name = (String) p.get("product_name");
                        productNames.put(pid, name);
                    }

                    // Add product_name to each item in orderDetails
                    if (orderDetails.containsKey("items")) {
                        List<Map<String, Object>> items = (List<Map<String, Object>>) orderDetails.get("items");
                        for (Map<String, Object> item : items) {
                            int pid = (int) item.get("product_id");
                            item.put("product_name", productNames.getOrDefault(pid, "Unknown Product"));
                        }
                    }

                    req.setAttribute("orderDetails", orderDetails);
                }

                // Forward to orderHistory.jsp
                req.getRequestDispatcher("orderHistory.jsp").forward(req, res);

            } else {
                // Default: show customerInfo.jsp
                req.getRequestDispatcher("customerInfo.jsp").forward(req, res);
            }

        } catch (Exception e) {
            e.printStackTrace();
            res.sendError(500, "Failed to load profile");
        }
    }
}
