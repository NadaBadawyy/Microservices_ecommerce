package servlets;

import com.fasterxml.jackson.databind.*;
import jakarta.servlet.*;
import jakarta.servlet.http.*;
import jakarta.servlet.annotation.*;
import java.io.IOException;
import java.net.URI;
import java.net.http.*;
import java.util.*;

@WebServlet("/CheckoutServlet")
public class CheckoutServlet extends HttpServlet {

    protected void doGet(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException {
        // Load customers and products for initial page
        HttpClient client = HttpClient.newHttpClient();
        ObjectMapper mapper = new ObjectMapper();

        try {
            // Customers
            HttpRequest customerReq = HttpRequest.newBuilder()
                    .uri(URI.create("http://localhost:5004/api/customers"))
                    .GET().build();
            HttpResponse<String> customerResp = client.send(customerReq, HttpResponse.BodyHandlers.ofString());
            List<Map<String,Object>> customers = mapper.readValue(
                    customerResp.body(),
                    new com.fasterxml.jackson.core.type.TypeReference<List<Map<String,Object>>>(){}
            );
            req.setAttribute("customers", customers);

            // Products
            HttpRequest productReq = HttpRequest.newBuilder()
                    .uri(URI.create("http://localhost:5002/api/inventory/products"))
                    .GET().build();
            HttpResponse<String> productResp = client.send(productReq, HttpResponse.BodyHandlers.ofString());
            List<Map<String,Object>> products = mapper.readValue(
                    productResp.body(),
                    new com.fasterxml.jackson.core.type.TypeReference<List<Map<String,Object>>>(){}
            );
            req.setAttribute("products", products);

            req.getRequestDispatcher("checkout.jsp").forward(req,res);

        } catch(Exception e) {
            e.printStackTrace();
            res.sendError(500,"Failed to load checkout page");
        }
    }

    protected void doPost(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException {
        String customerId = req.getParameter("customer_id");
        String[] productIds = req.getParameterValues("product_id");

        if(productIds == null || productIds.length == 0){
            req.setAttribute("errorMessage","No products selected!");
            doGet(req,res);
            return;
        }

        HttpClient client = HttpClient.newHttpClient();
        ObjectMapper mapper = new ObjectMapper();
        List<Map<String,Object>> selectedProducts = new ArrayList<>();
        double totalAmount = 0.0;

        try {
            // Check availability and calculate total
            for(String pidStr : productIds){
                int pid = Integer.parseInt(pidStr);
                int qty = Integer.parseInt(req.getParameter("quantity_" + pid));

                HttpRequest checkReq = HttpRequest.newBuilder()
                        .uri(URI.create("http://localhost:5002/api/inventory/check/" + pid))
                        .GET().build();
                HttpResponse<String> checkResp = client.send(checkReq,HttpResponse.BodyHandlers.ofString());
                JsonNode checkJson = mapper.readTree(checkResp.body());
                int available = checkJson.get("quantity_available").asInt();
                double unitPrice = checkJson.get("unit_price").asDouble();
                String productName = checkJson.get("product_name").asText();

                if(qty > available){
                    req.setAttribute("errorMessage","Not enough stock for "+productName+". Available: "+available);
                    doGet(req,res);
                    return;
                }

                Map<String,Object> prod = new HashMap<>();
                prod.put("product_id", pid);
                prod.put("product_name", productName);
                prod.put("unit_price", unitPrice);
                prod.put("quantity", qty);
                selectedProducts.add(prod);

                totalAmount += unitPrice*qty;
            }

            req.setAttribute("customer_id", customerId);
            req.setAttribute("selectedProducts", selectedProducts);
            req.setAttribute("totalAmount", totalAmount);
            req.getRequestDispatcher("confirmation.jsp").forward(req,res);

        } catch(Exception e){
            e.printStackTrace();
            req.setAttribute("errorMessage","Error calculating total or checking stock!");
            doGet(req,res);
        }
    }
}
