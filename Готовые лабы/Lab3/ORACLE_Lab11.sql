alter session set "_ORACLE_SCRIPT"=true;
CREATE USER migrationRepo identified by migrationRepo;
GRANT ALL PRIVILEGES TO migrationRepo;   
--DROP USER migrationRepo CASCADE;