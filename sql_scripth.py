CREATE OR REPLACE FUNCTION get_differing_columns(
    p_dataset_id1 IN VARCHAR2,
    p_dataset_id2 IN VARCHAR2
) RETURN VARCHAR2
IS
    v_sql VARCHAR2(32767);
    v_diff_columns VARCHAR2(32767);
    v_result VARCHAR2(32767);
BEGIN
    -- Generate the dynamic SQL for column comparisons
    FOR col IN (SELECT column_name
                FROM all_tab_columns
                WHERE table_name = 'CALC_RSLT_TP_CME2'
                  AND column_name NOT IN ('RESLUT_DATASET_ID')
                  AND owner = USER)
    LOOP
        v_diff_columns := v_diff_columns ||
            'CASE WHEN t1.' || col.column_name || ' <> t2.' || col.column_name ||
            ' THEN ''' || col.column_name || ''' END AS ' || col.column_name || '_diff, ';
    END LOOP;

    -- Remove the trailing comma and space
    v_diff_columns := RTRIM(v_diff_columns, ', ');

    -- Construct the full SQL query
    v_sql := 'WITH dataset1 AS (
                 SELECT *
                 FROM CALC_RSLT_TP_CME2
                 WHERE reslut_dataset_id = :dataset_id1
             ),
             dataset2 AS (
                 SELECT *
                 FROM CALC_RSLT_TP_CME2
                 WHERE reslut_dataset_id = :dataset_id2
             ),
             differences AS (
                 SELECT t1.ak, ' || v_diff_columns || '
                 FROM dataset1 t1
                 JOIN dataset2 t2 ON t1.ak = t2.ak -- Assuming "ak" is the primary key or unique identifier
             )
             SELECT LISTAGG(col_diff, '','') WITHIN GROUP (ORDER BY col_diff) AS differing_columns
             FROM (
                 SELECT ';

    -- Generate the dynamic SQL for the union of columns
    FOR col IN (SELECT column_name
                FROM all_tab_columns
                WHERE table_name = 'x'
                  AND column_name NOT IN ('RESLUT_DATASET_ID')
                  AND owner = USER)
    LOOP
        v_sql := v_sql || col.column_name || '_diff AS col_diff FROM differences WHERE ' || col.column_name || '_diff IS NOT NULL UNION ALL ';
    END LOOP;

    -- Remove the trailing UNION ALL and add the closing part of the query
    v_sql := RTRIM(v_sql, ' UNION ALL ') || ')';

    -- Execute the SQL and get the result
    EXECUTE IMMEDIATE v_sql INTO v_result USING p_dataset_id1, p_dataset_id2;

    RETURN v_result;
END get_differing_columns;
/

-- Test the function
DECLARE
    differing_columns VARCHAR2(32767);
BEGIN
    differing_columns := get_differing_columns('1', '2');
    DBMS_OUTPUT.PUT_LINE('Differing Columns: ' || differing_columns);
END;
/
