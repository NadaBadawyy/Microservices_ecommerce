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
            // Calculate the total price
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

            // Create the order
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

            // Get the order message
            String orderResponseBody = orderResponse.body();
            System.out.println("Raw order response: " + orderResponseBody);

            JsonNode orderJson = mapper.readTree(orderResponseBody);

            String orderMessage = orderJson.has("message")
                    ? orderJson.get("message").asText()
                    : "Order processed";

            int orderId = -1;

            if (orderJson.has("order") && orderJson.get("order").has("order_id")) {
                orderId = orderJson.get("order").get("order_id").asInt();
            }
            boolean success = orderResponse.statusCode() >= 200 && orderResponse.statusCode() < 300;

            if (success) {

                // Update the inventory
                Map<String, Object> inventoryPayload = new HashMap<>();
                inventoryPayload.put("products", products);

                HttpRequest inventoryRequest = HttpRequest.newBuilder()
                        .uri(URI.create("http://localhost:5002/api/inventory/update"))
                        .header("Content-Type", "application/json")
                        .POST(HttpRequest.BodyPublishers.ofString(mapper.writeValueAsString(inventoryPayload)))
                        .build();

                HttpResponse<String> inventoryResponse
                        = client.send(inventoryRequest, HttpResponse.BodyHandlers.ofString());

                System.out.println("Inventory update response: " + inventoryResponse.body());

                // Update loyalty points
                int loyaltyPoints = (int) Math.floor(totalAmount / 10);
                System.out.println("Loyalty points earned: " + loyaltyPoints);

                Map<String, Object> loyaltyPayload = new HashMap<>();
                loyaltyPayload.put("points", loyaltyPoints);

                HttpRequest loyaltyRequest = HttpRequest.newBuilder()
                        .uri(URI.create("http://localhost:5004/api/customers/" + customerId + "/loyalty"))
                        .header("Content-Type", "application/json")
                        .PUT(HttpRequest.BodyPublishers.ofString(mapper.writeValueAsString(loyaltyPayload)))
                        .build();

                HttpResponse<String> loyaltyResponse
                        = client.send(loyaltyRequest, HttpResponse.BodyHandlers.ofString());

                System.out.println("Loyalty update response: " + loyaltyResponse.body());

                // Send notification
                if (orderId != -1) {

                    Map<String, Object> notificationPayload = new HashMap<>();
                    notificationPayload.put("order_id", orderId);

                    HttpRequest notificationRequest = HttpRequest.newBuilder()
                            .uri(URI.create("http://localhost:5005/api/notifications/send"))
                            .header("Content-Type", "application/json")
                            .POST(HttpRequest.BodyPublishers.ofString(mapper.writeValueAsString(notificationPayload)))
                            .build();

                    HttpResponse<String> notificationResponse
                            = client.send(notificationRequest, HttpResponse.BodyHandlers.ofString());

                    System.out.println("Notification response: " + notificationResponse.body());
                }

            }

            // Get the order history of the customer
            HttpRequest historyRequest = HttpRequest.newBuilder()
                    .uri(URI.create("http://localhost:5001/api/orders?customer_id=" + customerId))
                    .GET()
                    .build();

            HttpResponse<String> historyResponse = client.send(historyRequest, HttpResponse.BodyHandlers.ofString());
            List<Map<String, Object>> history = mapper.readValue(
                    historyResponse.body(),
                    new com.fasterxml.jackson.core.type.TypeReference<List<Map<String, Object>>>() {
            }
            );

            // Forward to confirmation page
            req.setAttribute("orderResponse", orderMessage);
            req.setAttribute("orderHistory", history);
            req.getRequestDispatcher("confirmation.jsp").forward(req, res);

        } catch (Exception e) {
            e.printStackTrace();
            res.sendError(500, "Failed to process order");
        }
    }
}
