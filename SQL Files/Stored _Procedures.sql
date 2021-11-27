-- File will hold stored procdures in database

DROP PROCEDURE IF EXISTS getInvestmentandAcreage;
DELIMITER $

CREATE PROCEDURE getInvestmentandAcreage(IN usercounty char(100))
BEGIN
	SELECT 
    c.official_county,
    YEAR(d.EXPIRATION_DATE),
    ROUND(SUM(d.acres), 0) AS total_acres,
    ROUND(SUM(i.total_investment), 0) AS total_investment
FROM
    official_counties c
        JOIN
    details d ON d.lease_no = c.lease_no
		JOIN
	investment i on i.lease_no = c.lease_no
WHERE
    c.official_county LIKE LOWER(CONCAT('%', usercounty, '%'))
GROUP BY 1 , 2;
END $

DELIMITER ; 

-- Get empty values on active acreage 

DROP PROCEDURE IF EXISTS findNullInvestments;

Delimiter $

CREATE PROCEDURE findNullInvestments()
BEGIN
	select d.lease_no, d.county, i.total_investment
    from details d
    join investment i on i.lease_no = d.lease_no
    where i.total_investment is null;
END $




-- testing stored procedure
CALL getInvestmentandAcreage('Lea');
CALL getInvestmentandAcreage('Webster');
CALL getInvestmentandAcreage('bossier');
CALL getInvestmentandAcreage('converse');