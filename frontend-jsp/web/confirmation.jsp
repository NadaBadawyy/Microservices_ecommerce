<%@ page contentType="text/html;charset=UTF-8" %>
<script src="https://cdn.tailwindcss.com"></script>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>

<jsp:include page="navbar.jsp"/>
<div class="max-w-xl mx-auto p-6">

    <c:if test="${empty orderResponse}">
        <h2 class="text-2xl font-bold mb-6">Confirm Your Order</h2>

        <!-- Show confirmation form only if order not yet submitted -->
        <form action="<%= request.getContextPath()%>/OrderServlet" method="post" class="space-y-6">
            <input type="hidden" name="customer_id" value="${customer_id}">
            <input type="hidden" name="totalAmount" value="${totalAmount}">

            <div class="border p-3 rounded">
                <h3 class="font-semibold mb-2">Products</h3>
                <c:forEach var="p" items="${selectedProducts}">
                    <div class="flex justify-between mb-2">
                        <span>${p.product_name} x ${p.quantity}</span>
                        <span>$${p.unit_price * p.quantity}</span>
                        <input type="hidden" name="product_id" value="${p.product_id}">
                        <input type="hidden" name="quantity_${p.product_id}" value="${p.quantity}">
                    </div>
                </c:forEach>
                <p class="font-bold mt-2">Total: $${totalAmount}</p>
            </div>

            <div class="flex gap-4">
                <a href="<%= request.getContextPath()%>/CheckoutServlet" class="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded">Cancel</a>
                <button class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded flex-1">Confirm Order</button>
            </div>
        </form>
    </c:if>

    <!-- Show order response and history after order submission -->
    <c:if test="${not empty orderResponse}">
        <div class="mt-6 p-4 bg-blue-100 border-l-4 border-blue-500 rounded">
            <h3 class="font-semibold">Order Status:</h3>
            <p>${orderResponse}</p>
        </div>
    </c:if>

    <c:if test="${not empty orderHistory}">
        <div class="mt-4 border p-4 rounded shadow">
            <h3 class="font-semibold mb-2">Order History</h3>
            <c:forEach var="o" items="${orderHistory}">
                <div class="border-b py-2">
                    <p><b>Order ID:</b> ${o.order_id}</p>
                    <p><b>Total Amount:</b> $${o.total_amount}</p>
                    <p><b>Date:</b> ${o.created_at}</p>
                </div>
            </c:forEach>
        </div>
    </c:if>
</div>
