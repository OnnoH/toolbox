SELECT SEGMENT_NAME, SEGMENT_TYPE, TABLESPACE_NAME, BYTES, BLOCKS, EXTENTS
    FROM DBA_SEGMENTS
    WHERE OWNER='APP_OWNER'
    ORDER BY BYTES DESC, SEGMENT_NAME;
    
ALTER TABLE "APP_SCHEMA"."LOB_TABLE" MODIFY LOB (CONTENT) (SHRINK SPACE);