<%@ page contentType="text/html;charset=UTF-8" %>
<script src="https://cdn.tailwindcss.com"></script>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>

<jsp:include page="navbar.jsp"/>

<div class="max-w-4xl mx-auto p-6 pt-20">
    <h2 class="text-2xl font-bold mb-6">Order History</h2>

    <!-- Customer selection dropdown -->
    <form method="get" action="${pageContext.request.contextPath}/ProfileServlet" class="mb-6">
        <input type="hidden" name="page" value="history">
        <label class="block font-semibold mb-1">Select Customer</label>
        <select name="customer_id" onchange="this.form.submit()" class="w-full border p-2 rounded">
            <option value="">-- Select Customer --</option>
            <c:forEach var="c" items="${customers}">
                <option value="${c.customer_id}" <c:if test="${c.customer_id == selectedCustomerId}">selected</c:if>>
                    ${c.customer_id} - ${c.name}
                </option>
            </c:forEach>
        </select>
    </form>

    <!-- Order History Table -->
        <c:if test="${not empty orderHistory}">
        <div class="mt-4 border p-4 rounded shadow">
            <h3 class="font-semibold mb-2">Order History</h3>
            <c:forEach var="o" items="${orderHistory}">
                <div class="border-b py-2">
                    <p><b>Order ID:</b> <a class="text-blue-600 underline"
                           href="${pageContext.request.contextPath}/ProfileServlet?customer_id=${selectedCustomerId}&page=orderDetails&order_id=${o.order_id}">
                           ${o.order_id}
                        </a></p>
                    <p><b>Total Amount:</b> $${o.total_amount}</p>
                    <p><b>Date:</b> ${o.created_at}</p>
                </div>
            </c:forEach>
        </div>
    </c:if>
    


    <c:if test="${empty orderHistory}">
        <p class="text-gray-600">No orders found for this customer.</p>
    </c:if>

    <!-- Display Order Details -->
    <c:if test="${not empty orderDetails}">
        <div class="mt-8 bg-gray-50 border rounded p-6">
            <h3 class="text-xl font-bold mb-4">Order Details</h3>

            <p><b>Order ID:</b> ${orderDetails.order_id}</p>
            <p><b>Status:</b> ${orderDetails.status}</p>
            <p><b>Total:</b> $${orderDetails.total_amount}</p>
            <p><b>Date:</b> ${orderDetails.created_at}</p>

            <h4 class="text-lg font-semibold mt-4 mb-2">Items</h4>

            <table class="w-full border">
                <tr class="bg-gray-200">
                    <th class="p-2 border">Product ID</th>
                    <th class="p-2 border">Quantity</th>
                    <th class="p-2 border">Unit Price</th>
                </tr>

                <c:forEach var="i" items="${orderDetails.items}">
                    <tr>
                        <td class="p-2 border">${i.product_name}</td>
                        <td class="p-2 border">${i.quantity}</td>
                        <td class="p-2 border">$${i.unit_price}</td>
                    </tr>
                </c:forEach>
            </table>
        </div>
    </c:if>
</div>
