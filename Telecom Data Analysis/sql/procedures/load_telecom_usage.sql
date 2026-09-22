IF OBJECT_ID('dbo.load_telecom_usage', 'P') IS NOT NULL
    DROP PROCEDURE dbo.load_telecom_usage;
GO

CREATE PROCEDURE dbo.load_telecom_usage
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY

        BEGIN TRANSACTION;

        -- Validate staging data
        DELETE FROM stagging.fresh_telecom_data
        WHERE customer_id IS NULL
           OR usage_date IS NULL;


        -- Insert / update production data
        MERGE dbo.telecom_usage AS target
        USING stagging.fresh_telecom_data AS source
            ON target.customer_id = source.customer_id

        WHEN MATCHED THEN
            UPDATE SET
                target.data_gb       = source.data_gb,
                target.call_minutes  = source.call_minutes,
                target.sms_count     = source.sms_count,
                target.revenue       = source.revenue

        WHEN NOT MATCHED BY TARGET THEN
            INSERT (
                customer_id,
                usage_date,
                data_gb,
                call_minutes,
                sms_count,
                revenue
            )
            VALUES (
                source.customer_id,
                source.usage_date,
                source.data_gb,
                source.call_minutes,
                source.sms_count,
                source.revenue
            );

        COMMIT TRANSACTION;

    END TRY

    BEGIN CATCH

        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;

        THROW;

    END CATCH;
END;
