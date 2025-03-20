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



CREATE OR REPLACE PROCEDURE SP_BACKUP_ALL_TABLES()
RETURNS STRING
LANGUAGE SQL
AS 
$$
DECLARE TABLE_LIST ARRAY;
DECLARE TBL_NAME STRING;

BEGIN
    -- Define the array of table names
    LET TABLE_LIST = ARRAY_CONSTRUCT('T1', 'T2', 'T3');

    -- Loop through each table in the array
    FOR TBL_NAME IN (SELECT VALUE FROM TABLE(FLATTEN(INPUT => TABLE_LIST))) DO
        CALL SP_BACKUP_TABLE(TBL_NAME);
    END FOR;

    RETURN 'Backup and cleanup completed for all tables';
END;
$$;
