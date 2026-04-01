-- Top Customers
SELECT 
    CustomerID,
    COUNT(DISTINCT InvoiceNo) AS Orders,
    SUM(Quantity * UnitPrice) AS Revenue
FROM online_retail
WHERE CustomerID IS NOT NULL
AND InvoiceNo NOT LIKE 'C%'
GROUP BY CustomerID
ORDER BY Revenue DESC
LIMIT 10;


-- Monthly Revenue
SELECT 
    DATE_FORMAT(InvoiceDate, '%Y-%m') AS Month,
    SUM(Quantity * UnitPrice) AS Revenue
FROM online_retail
WHERE InvoiceNo NOT LIKE 'C%'
GROUP BY Month
ORDER BY Month;


-- Country Revenue
SELECT 
    Country,
    SUM(Quantity * UnitPrice) AS Revenue
FROM online_retail
GROUP BY Country
ORDER BY Revenue DESC
LIMIT 10;