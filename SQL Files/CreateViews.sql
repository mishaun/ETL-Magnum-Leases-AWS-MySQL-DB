CREATE VIEW <schema>.v_activeAcreage as
select * from <schema>.details
where EXPIRATION_DATE > curdate();
