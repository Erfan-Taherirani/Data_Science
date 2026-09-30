IF OBJECT_ID('dbo.sp_retrieve_employee_by_hire_date') IS NOT NULL
DROP PROCEDURE dbo.sp_retrieve_employee_by_hire_date;
GO

CREATE PROCEDURE sp_retrieve_employee_by_hire_date
    @hire_date DATE
AS
BEGIN
    SET NOCOUNT ON;

    SELECT *
    FROM HumanResources.Employee
    WHERE HireDate = @hire_date
END;
GO

EXEC sp_retrieve_employee_by_hire_date
    @hire_date = '2009-01-02'