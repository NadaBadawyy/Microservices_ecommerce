<%@ page contentType="text/html;charset=UTF-8" %>
<script src="https://cdn.tailwindcss.com"></script>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>

<jsp:include page="navbar.jsp"/>

<div class="max-w-xl mx-auto p-6">
    <h2 class="text-2xl font-bold mb-6">Customer Info</h2>

    <form method="get" action="<%= request.getContextPath() %>/ProfileServlet" class="mb-6">
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

    <c:if test="${not empty customer}">
        <div class="border p-4 rounded shadow">
            <p><b>ID:</b> ${customer.customer_id}</p>
            <p><b>Name:</b> ${customer.name}</p>
            <p><b>Email:</b> ${customer.email}</p>
            <p><b>Loyalty Points:</b> ${customer.loyalty_points}</p>
        </div>
    </c:if>

</div>
