CREATE OR REPLACE PROCEDURE SP_BACKUP_TABLE(TBL_NAME STRING)
RETURNS STRING
LANGUAGE SQL
AS 
$$
DECLARE HIST_TBL_NAME STRING;
BEGIN
    -- Determine history table name
    LET HIST_TBL_NAME = TBL_NAME || '_HST';

    -- Insert today's data into the history table
    EXECUTE IMMEDIATE 
    'INSERT INTO ' || HIST_TBL_NAME || ' SELECT *, CURRENT_DATE AS LOAD_DATE FROM ' || TBL_NAME;

    -- Delete records older than 7 days from the history table
    EXECUTE IMMEDIATE 
    'DELETE FROM ' || HIST_TBL_NAME || ' WHERE LOAD_DATE < DATEADD(DAY, -7, CURRENT_DATE)';

    RETURN 'Backup and cleanup completed for ' || TBL_NAME;
END;
$$;
