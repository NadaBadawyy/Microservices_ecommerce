<%@ page contentType="text/html;charset=UTF-8" %>
<script src="https://cdn.tailwindcss.com"></script>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>


<jsp:include page="navbar.jsp"/>

<div class="max-w-7xl mx-auto p-6">
    <h2 class="text-3xl font-bold mb-6">Product Catalog</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <c:forEach var="product" items="${products}">
            <div class="border rounded-xl shadow p-5">
                <h3 class="text-xl font-semibold">
                    ${product['product_name']}
                </h3>
                <p class="text-gray-600">
                    $${product['unit_price']}
                </p>
                <p class="mt-2 ${product['quantity_available'] > 0 ? 'text-green-600' : 'text-red-600'}">
                    <c:choose>
                        <c:when test="${product['quantity_available'] > 0}">
                            Available
                        </c:when>
                        <c:otherwise>
                            Not Available
                        </c:otherwise>
                    </c:choose>
                </p>
            </div>
        </c:forEach>
    </div>


    <a href="<%= request.getContextPath()%>/CheckoutServlet" class="inline-block mt-4 bg-blue-600 text-white px-4 py-2 rounded">Make Order</a>

</div>
