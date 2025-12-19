package servlets;

import com.fasterxml.jackson.databind.*;
import jakarta.servlet.*;
import jakarta.servlet.http.*;
import jakarta.servlet.annotation.*;
import java.io.IOException;
import java.net.URI;
import java.net.http.*;
import java.util.*;

@WebServlet("/OrderServlet")
public class OrderServlet extends HttpServlet {

    protected void doPost(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {

        String customerId = req.getParameter("customer_id");
        String[] productIds = req.getParameterValues("product_id");

        if (productIds == null || productIds.length == 0) {
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

        ObjectMapper mapper = new ObjectMapper();
        HttpClient client = HttpClient.newHttpClient();

        try {
            // ---------- 1️⃣ PRICING SERVICE ----------
            Map<String, Object> pricingPayload = new HashMap<>();
            pricingPayload.put("products", products);

            HttpRequest pricingRequest = HttpRequest.newBuilder()
                    .uri(URI.create("http://localhost:5003/api/pricing/calculate"))
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(mapper.writeValueAsString(pricingPayload)))
                    .build();

            HttpResponse<String> pricingResponse = client.send(pricingRequest, HttpResponse.BodyHandlers.ofString());
            JsonNode pricingJson = mapper.readTree(pricingResponse.body());
            double totalAmount = pricingJson.has("total_amount") ? pricingJson.get("total_amount").asDouble() : 0.0;

            // ---------- 2️⃣ ORDER SERVICE ----------
            Map<String, Object> orderPayload = new HashMap<>();
            orderPayload.put("customer_id", Integer.parseInt(customerId));
            orderPayload.put("products", products);
            orderPayload.put("total_amount", totalAmount);

            HttpRequest orderRequest = HttpRequest.newBuilder()
                    .uri(URI.create("http://localhost:5001/api/orders/create"))
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(mapper.writeValueAsString(orderPayload)))
                    .build();

            HttpResponse<String> orderResponse = client.send(orderRequest, HttpResponse.BodyHandlers.ofString());

            // ---------- 3️⃣ Extract order message ----------
            String orderResponseBody = orderResponse.body();
            System.out.println("Raw order response: " + orderResponseBody);

            JsonNode orderJson = mapper.readTree(orderResponseBody);
            String orderMessage = "Order completed";
            if (orderJson.has("message") && !orderJson.get("message").asText().isEmpty()) {
                orderMessage = orderJson.get("message").asText();
            }

            // ---------- 4️⃣ Update inventory if order succeeded ----------
            boolean success = orderMessage.toLowerCase().contains("success");
            if (success) {
                Map<String, Object> inventoryPayload = new HashMap<>();
                inventoryPayload.put("products", products);

                HttpRequest inventoryRequest = HttpRequest.newBuilder()
                        .uri(URI.create("http://localhost:5002/api/inventory/update"))
                        .header("Content-Type", "application/json")
                        .POST(HttpRequest.BodyPublishers.ofString(mapper.writeValueAsString(inventoryPayload)))
                        .build();

                HttpResponse<String> inventoryResponse = client.send(inventoryRequest, HttpResponse.BodyHandlers.ofString());
                System.out.println("Inventory update response: " + inventoryResponse.body());
            }

            // ---------- 5️⃣ Get customer order history ----------
            HttpRequest historyRequest = HttpRequest.newBuilder()
                    .uri(URI.create("http://localhost:5001/api/orders?customer_id=" + customerId))
                    .GET()
                    .build();

            HttpResponse<String> historyResponse = client.send(historyRequest, HttpResponse.BodyHandlers.ofString());
            List<Map<String, Object>> history = mapper.readValue(
                    historyResponse.body(),
                    new com.fasterxml.jackson.core.type.TypeReference<List<Map<String, Object>>>() {}
            );

            // ---------- 6️⃣ Forward to confirmation page ----------
            req.setAttribute("orderResponse", orderMessage);
            req.setAttribute("orderHistory", history);
            req.getRequestDispatcher("confirmation.jsp").forward(req, res);

        } catch (Exception e) {
            e.printStackTrace();
            res.sendError(500, "Failed to process order");
        }
    }
}
