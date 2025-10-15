use python;
CREATE TABLE IF NOT EXISTS Products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10,2),
    quantity INT
);

select * from Sales;

CREATE TABLE IF NOT EXISTS Sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    quantity INT,
    total DECIMAL(10,2),
    date DATETIME,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

select * from products;
select * from Sales;

delete  from products 
WHERE quantity = 22  ;
SET SQL_SAFE_UPDATES = 0;

INSERT INTO Products (product_id, name, category, price, quantity) VALUES
(1, 'Apple iPhone 15', 'Electronics', 79999.00, 10),
(2, 'Samsung Galaxy S23', 'Electronics', 69999.00, 15),
(3, 'Dell Inspiron Laptop', 'Computers', 55000.00, 5),
(4, 'HP Pavilion Laptop', 'Computers', 60000.00, 8),
(5, 'Sony Headphones', 'Accessories', 2999.00, 25),
(6, 'Logitech Mouse', 'Accessories', 1200.00, 50),
(7, 'Nike Running Shoes', 'Footwear', 4999.00, 20),
(8, 'Adidas Sneakers', 'Footwear', 3999.00, 18),
(9, 'Organic Almonds 500g', 'Grocery', 750.00, 30),
(10, 'Olive Oil 1L', 'Grocery', 1200.00, 12);


