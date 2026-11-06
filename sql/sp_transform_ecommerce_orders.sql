CREATE OR ALTER PROCEDURE dbo.sp_transform_ecommerce_orders
AS
BEGIN
    TRUNCATE TABLE dbo.fact_ecommerce_orders;

    INSERT INTO dbo.fact_ecommerce_orders (
        CartId, 
        userId, 
        CustomerName, 
        City, 
        OrderDate, 
        ProductId, 
        Category, 
        Quantity, 
        UnitPrice, 
        TotalPrice,
        ProcessedAt
    )
    SELECT 
        CartId,
        userId,
        LTRIM(RTRIM(CustomerName)) AS CustomerName, 
        ISNULL(City, 'Unknown') AS City,          
        OrderDate,
        ProductId,
        Category,
        Quantity,
        UnitPrice,
        (Quantity * UnitPrice) AS TotalPrice,
        GETDATE() AS ProcessedAt
    FROM dbo.stg_ecommerce_orders;
END
GO