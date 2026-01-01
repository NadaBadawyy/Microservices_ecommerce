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

    protected void doPost(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException {
        String customerId = req.getParameter("customer_id");
        String[] productIds = req.getParameterValues("product_id");

        double totalAmount = Double.parseDouble(req.getParameter("totalAmount")); // <-- use the total from previous servlet

        ObjectMapper mapper = new ObjectMapper();
        HttpClient client = HttpClient.newHttpClient();
        List<Map<String,Object>> products = new ArrayList<>();

        try {
            for(String pidStr: productIds){
                int pid = Integer.parseInt(pidStr);
                int qty = Integer.parseInt(req.getParameter("quantity_" + pid));
                Map<String,Object> item = new HashMap<>();
                item.put("product_id", pid);
                item.put("quantity", qty);
                products.add(item);
            }

            // Create order
            Map<String,Object> orderPayload = new HashMap<>();
            orderPayload.put("customer_id", Integer.parseInt(customerId));
            orderPayload.put("products", products);
            orderPayload.put("total_amount", totalAmount); // use passed value

            HttpRequest orderReq = HttpRequest.newBuilder()
                    .uri(URI.create("http://localhost:5001/api/orders/create"))
                    .header("Content-Type","application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(mapper.writeValueAsString(orderPayload)))
                    .build();
            HttpResponse<String> orderResp = client.send(orderReq,HttpResponse.BodyHandlers.ofString());

            JsonNode orderJson = mapper.readTree(orderResp.body());
            String orderMessage = orderJson.has("message") ? orderJson.get("message").asText() : "Order processed";
            int orderId = orderJson.has("order") && orderJson.get("order").has("order_id")
                    ? orderJson.get("order").get("order_id").asInt() : -1;

            // Update inventory
            for(Map<String,Object> p: products){
                int pid = (int)p.get("product_id");
                int qty = (int)p.get("quantity");
                Map<String,Object> invPayload = new HashMap<>();
                invPayload.put("product_id", pid);
                invPayload.put("quantity_change", -qty);
                HttpRequest invReq = HttpRequest.newBuilder()
                        .uri(URI.create("http://localhost:5002/api/inventory/update"))
                        .header("Content-Type","application/json")
                        .PUT(HttpRequest.BodyPublishers.ofString(mapper.writeValueAsString(invPayload)))
                        .build();
                client.send(invReq,HttpResponse.BodyHandlers.ofString());
            }

            // Update loyalty points
            int loyaltyPoints = (int)Math.floor(totalAmount/10);
            Map<String,Object> loyaltyPayload = new HashMap<>();
            loyaltyPayload.put("points", loyaltyPoints);
            HttpRequest loyaltyReq = HttpRequest.newBuilder()
                    .uri(URI.create("http://localhost:5004/api/customers/" + customerId + "/loyalty"))
                    .header("Content-Type","application/json")
                    .PUT(HttpRequest.BodyPublishers.ofString(mapper.writeValueAsString(loyaltyPayload)))
                    .build();
            client.send(loyaltyReq,HttpResponse.BodyHandlers.ofString());

            // Send notification
            if(orderId != -1){
                Map<String,Object> notifPayload = new HashMap<>();
                notifPayload.put("order_id", orderId);
                HttpRequest notifReq = HttpRequest.newBuilder()
                        .uri(URI.create("http://localhost:5005/api/notifications/send"))
                        .header("Content-Type","application/json")
                        .POST(HttpRequest.BodyPublishers.ofString(mapper.writeValueAsString(notifPayload)))
                        .build();
                client.send(notifReq,HttpResponse.BodyHandlers.ofString());
            }

            // Fetch order history
            HttpRequest historyReq = HttpRequest.newBuilder()
                    .uri(URI.create("http://localhost:5001/api/orders?customer_id="+customerId))
                    .GET().build();
            HttpResponse<String> historyResp = client.send(historyReq,HttpResponse.BodyHandlers.ofString());
            List<Map<String,Object>> history = mapper.readValue(
                    historyResp.body(),
                    new com.fasterxml.jackson.core.type.TypeReference<List<Map<String,Object>>>(){}
            );

            req.setAttribute("orderResponse", orderMessage);
            req.setAttribute("orderHistory", history);
            req.getRequestDispatcher("confirmation.jsp").forward(req,res);

        } catch(Exception e){
            e.printStackTrace();
            req.setAttribute("errorMessage","Failed to create order!");
            req.getRequestDispatcher("checkout.jsp").forward(req,res);
        }
    }
}
