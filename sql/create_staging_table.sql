CREATE TABLE stg_ecommerce_orders (
    CartId INT,
    userId INT,
    CustomerName VARCHAR(100),
    City VARCHAR(50),
    OrderDate DATE,
    ProductId INT,
    Category VARCHAR(50),
    Quantity INT,
    UnitPrice DECIMAL(10, 2),
    TotalPrice DECIMAL(10, 2)
);
