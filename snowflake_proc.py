CREATE OR REPLACE TABLE T1 AS 
SELECT *, CURRENT_DATE AS load_date 
FROM (
    SELECT *, ROW_NUMBER() OVER () AS rn FROM CUSTOMER
) 
WHERE rn <= 10;

CREATE OR REPLACE TABLE T2 AS 
SELECT *, CURRENT_DATE AS load_date 
FROM (
    SELECT *, ROW_NUMBER() OVER () AS rn FROM CUSTOMER
) 
WHERE rn > (SELECT COUNT(*) - 10 FROM CUSTOMER);

CREATE OR REPLACE TABLE T1_HIST LIKE T1;
CREATE OR REPLACE TABLE T2_HIST LIKE T2;

CREATE OR REPLACE PROCEDURE manage_history(table_name STRING)
RETURNS STRING
LANGUAGE SQL 
AS 
$$
DECLARE hist_table STRING;
DECLARE max_load_actual DATE;
DECLARE max_load_hist DATE;
DECLARE rs RESULTSET;
BEGIN
    -- Determine history table name
    LET hist_table = table_name || '_HIST';
    
    -- Get max load_date from actual table
    LET rs = (EXECUTE IMMEDIATE 'SELECT MAX(load_date) FROM ' || table_name);
    FETCH rs INTO max_load_actual;
    
    -- Get max load_date from history table
    LET rs = (EXECUTE IMMEDIATE 'SELECT MAX(load_date) FROM ' || hist_table);
    FETCH rs INTO max_load_hist;

    -- Ensure history table is considered even if it's empty
    LET max_load_hist = COALESCE(max_load_hist, '1900-01-01');
    
    -- Insert today's records into history table only if actual table has newer data
    IF max_load_actual > max_load_hist THEN
        EXECUTE IMMEDIATE 'INSERT INTO ' || hist_table || 
                          ' SELECT * FROM ' || table_name || 
                          ' WHERE load_date = CURRENT_DATE;';
    END IF;
    
    -- Delete records older than 7 days from the history table
    EXECUTE IMMEDIATE 'DELETE FROM ' || hist_table || ' WHERE load_date < CURRENT_DATE - 7;';
    
    RETURN 'History managed for table: ' || table_name;
END;
$$;


CREATE OR REPLACE PROCEDURE manage_all_history()
RETURNS STRING
LANGUAGE SQL 
AS 
$$
DECLARE tables ARRAY;
BEGIN
    -- Define table names
    LET tables = ARRAY_CONSTRUCT('T1', 'T2');

    -- Loop through tables and call manage_history
    FOR i IN ARRAY_SIZE(tables) DO
        CALL manage_history(tables[i]);
    END FOR;

    RETURN 'History managed for all tables.';
END;
$$;

CREATE OR REPLACE PROCEDURE manage_all_history()
RETURNS STRING
LANGUAGE JAVASCRIPT
AS
$$
    var tables = ['T1', 'T2'];
    for (var i = 0; i < tables.length; i++) {
        var sql_cmd = "CALL manage_history('" + tables[i] + "')";
        snowflake.execute({sqlText: sql_cmd});
    }
    return 'History managed for all tables.';
$$;


CALL manage_all_history();

CALL manage_all_history();
