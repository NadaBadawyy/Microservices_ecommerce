<%@ page contentType="text/html;charset=UTF-8" %>
<script src="https://cdn.tailwindcss.com"></script>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>

<div class="max-w-xl mx-auto p-6">
    <h2 class="text-2xl font-bold mb-6">Checkout</h2>

    <form action="<%= request.getContextPath() %>/OrderServlet" method="post" class="space-y-6">
        <div>
            <label class="block font-semibold mb-1">Customer ID</label>
            <select name="customer_id" class="w-full border p-2 rounded">
                <c:forEach var="c" items="${customers}">
                    <option value="${c.customer_id}">${c.customer_id}</option>
                </c:forEach>
            </select>
        </div>

        <div>
            <label class="block font-semibold mb-2">Select Products</label>
            <c:forEach var="p" items="${products}">
                <div class="flex items-center gap-3 border p-3 rounded mb-2">
                    <input type="checkbox" name="product_id" value="${p.product_id}">
                    <span class="flex-1">${p.product_name} - $${p.unit_price}</span>
                    <input type="number" name="quantity_${p.product_id}" value="1" min="1" class="border p-1 w-20 rounded">
                </div>
            </c:forEach>
        </div>

        <button class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded w-full">
            Confirm Order
        </button>
    </form>
</div>
