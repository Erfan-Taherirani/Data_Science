
-- create stagging table structure for telecom usage data
IF OBJECT_ID('dbo.telecom_usage', 'U') IS NOT NULL
DROP TABLE dbo.telecom_usage;
GO
CREATE TABLE dbo.telecom_usage (
    customer_id INT NOT NULL,
    usage_date DATE NOT NULL,
    data_gb FLOAT,
    call_minutes INT,
    sms_count INT,
    revenue FLOAT
);
