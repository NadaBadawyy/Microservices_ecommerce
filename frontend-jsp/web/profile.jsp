<%@ page contentType="text/html;charset=UTF-8" %>
<script src="https://cdn.tailwindcss.com"></script>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>

<jsp:include page="navbar.jsp"/>

<div class="max-w-6xl mx-auto p-8">

    <h2 class="text-3xl font-bold mb-6">Customer Profile</h2>

    <!-- Customer Selector -->
    <form method="get" action="<%= request.getContextPath() %>/ProfileServlet" class="mb-8 flex gap-4">
        <select name="customer_id" class="border p-3 rounded w-64">
            <option value="">Select Customer</option>
            <c:forEach var="c" items="${customers}">
                <option value="${c.customer_id}"
                        ${c.customer_id == selectedCustomerId ? "selected" : ""}>
                    ${c.customer_id}
                </option>
            </c:forEach>
        </select>

        <button class="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700">
            Load Profile
        </button>
    </form>

    <!-- Customer Info -->
    <c:if test="${not empty customer}">
        <div class="bg-white shadow rounded p-6 mb-8">
            <h3 class="text-xl font-semibold mb-4">Customer Information</h3>

            <p><b>ID:</b> ${customer.customer_id}</p>
            <p><b>Name:</b> ${customer.name}</p>
            <p><b>Email:</b> ${customer.email}</p>
            <p><b>Phone:</b> ${customer.phone}</p>
            <p><b>Loyalty Points:</b> ${customer.loyalty_points}</p>
        </div>
    </c:if>

    <!-- Order History -->
    <div class="bg-white shadow rounded p-6">
        <h3 class="text-xl font-semibold mb-4">Order History</h3>

        <c:choose>
            <c:when test="${not empty orderHistory}">
                <c:forEach var="o" items="${orderHistory}">
                    <div class="border-b py-3">
                        <p><b>Order ID:</b> ${o.order_id}</p>
                        <p><b>Total:</b> $${o.total_amount}</p>
                        <p><b>Date:</b> ${o.created_at}</p>
                    </div>
                </c:forEach>
            </c:when>
            <c:otherwise>
                <p class="text-gray-500">No orders found.</p>
            </c:otherwise>
        </c:choose>
    </div>

</div>
