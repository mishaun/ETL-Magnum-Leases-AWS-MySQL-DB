CREATE VIEW v_activeAcreage as
select * from details
where EXPIRATION_DATE > curdate();
