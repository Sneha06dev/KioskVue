document.addEventListener("DOMContentLoaded", function () {
    function saveDrawing() {
        fetch("/save_drawing", { method: "POST" })
            .then(response => response.json())
            .then(data => {
                document.getElementById("extracted-text").innerText = "Extracted Text: " + data.text;
                let productList = document.getElementById("product-list");
                productList.innerHTML = ""; // Clear previous results

                if (data.products.length === 0) {
                    productList.innerHTML = "<li>No matching products found.</li>";
                } else {
                    data.products.forEach(product => {
                        let item = document.createElement("li");
                        item.innerHTML = `
                            <strong>${product.Description}</strong> <br>
                            Stock Code: ${product.StockCode} <br>
                            Quantity: ${product.Quantity} <br>
                            Price: $${product.UnitPrice.toFixed(2)}
                        `;
                        productList.appendChild(item);
                    });
                }
            })
            .catch(error => console.error("Error:", error));
    }

    // Attach function to button
    document.querySelector("button").addEventListener("click", saveDrawing);
});
