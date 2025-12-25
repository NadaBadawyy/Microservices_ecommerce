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
            // Get all customers
            HttpRequest customerReq = HttpRequest.newBuilder()
                    .uri(URI.create("http://localhost:5004/api/customers"))
                    .GET().build();

            HttpResponse<String> customerResp =
                    client.send(customerReq, HttpResponse.BodyHandlers.ofString());

            List<Map<String,Object>> customers = mapper.readValue(
                    customerResp.body(),
                    new com.fasterxml.jackson.core.type.TypeReference<List<Map<String,Object>>>() {}
            );

            req.setAttribute("customers", customers);

            // If customer selected, fetch their profile and order history
            String customerId = req.getParameter("customer_id");

            if (customerId != null && !customerId.isEmpty()) {

                req.setAttribute("selectedCustomerId", Integer.parseInt(customerId));

                // Find customer object
                Map<String,Object> selectedCustomer = null;
                for (Map<String,Object> c : customers) {
                    if (String.valueOf(c.get("customer_id")).equals(customerId)) {
                        selectedCustomer = c;
                        break;
                    }
                }
                req.setAttribute("customer", selectedCustomer);

                // Get order history
                HttpRequest historyReq = HttpRequest.newBuilder()
                        .uri(URI.create("http://localhost:5001/api/orders?customer_id=" + customerId))
                        .GET().build();

                HttpResponse<String> historyResp =
                        client.send(historyReq, HttpResponse.BodyHandlers.ofString());

                List<Map<String,Object>> history = mapper.readValue(
                        historyResp.body(),
                        new com.fasterxml.jackson.core.type.TypeReference<List<Map<String,Object>>>() {}
                );

                req.setAttribute("orderHistory", history);
            }

            req.getRequestDispatcher("profile.jsp").forward(req, res);

        } catch (Exception e) {
            e.printStackTrace();
            res.sendError(500, "Failed to load profile");
        }
    }
}
