<%@ page contentType="text/html;charset=UTF-8" %>
<script src="https://cdn.tailwindcss.com"></script>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/functions" prefix="fn" %>


<div class="max-w-4xl mx-auto p-6 pt-20">

    <!-- Order Status Message -->
    <c:set var="success" value="${fn:containsIgnoreCase(orderResponse, 'success')}"/>
    <div class="mb-6 p-4 rounded shadow bg-gray-100 border-l-4 border-gray-500 text-gray-700">
        <h3 class="text-lg font-semibold mb-2">Order Status</h3>
        <p>${orderResponse}</p>
    </div>

    <!-- Order History -->
    <div class="border p-4 rounded shadow">
        <h3 class="text-xl font-semibold mb-4">Order History</h3>

        <c:choose>
            <c:when test="${not empty orderHistory}">
                <c:forEach var="o" items="${orderHistory}">
                    <div class="border-b py-2">
                        <p><b>Order ID:</b> ${o.order_id}</p>
                        <p><b>Total Amount:</b> $${o.total_amount}</p>
                        <p><b>Date:</b> ${o.created_at}</p>
                    </div>
                </c:forEach>
            </c:when>
            <c:otherwise>
                <p class="text-gray-600">No previous orders found for this customer.</p>
            </c:otherwise>
        </c:choose>
    </div>

</div>
