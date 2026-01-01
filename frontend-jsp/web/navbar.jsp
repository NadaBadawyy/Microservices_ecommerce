<%@ page contentType="text/html;charset=UTF-8" %>
<script src="https://cdn.tailwindcss.com"></script>

<nav class="bg-gray-900 text-white px-8 py-4 shadow-md">
    <div class="max-w-7xl mx-auto flex justify-between items-center">
        <div class="text-xl font-bold">
            🛒 Order Management
        </div>

        <div class="flex gap-6 text-lg">
            <!-- Java expression to gets the base URL -->
            <a href="<%= request.getContextPath() %>/ProductServlet"
               class="hover:text-blue-400 transition">
                Products
            </a>  
            <a href="<%= request.getContextPath() %>/CheckoutServlet"
               class="hover:text-blue-400 transition">
                Make Order
            </a>
            <a href="<%= request.getContextPath() %>/ProfileServlet?page=info"
               class="hover:text-blue-400 transition">
                Customer Info
            </a>
            <a href="<%= request.getContextPath() %>/ProfileServlet?page=history"
               class="hover:text-blue-400 transition">
                Order History
            </a>
        </div>
    </div>
</nav>
