show databases;

use MagnumBLMLeases;

show tables;

select * from details;
select * from interest;



select * from details
where plotted like '%yay%';

select * from details 
where LEASE_NO = 'ALES51293';

INSERT INTO details(LEASE_NO,PLOTTED,GRANTEE,SALE_DATE,EFFECTIVE_DATE_OF_LEASE,EXPIRATION_DATE,ACRES,COUNTY,ST,STATUS_COMMENTS,EXPIRATION_YEAR,TOWNSHIP,RANGE_PLSS,DESCRIPTION_I,DESCRIPTION_II,DESCRIPTION_III)
VALUES ('ALES51293',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ') 
ON DUPLICATE KEY UPDATE 
 LEASE_NO = 'ALES51293',
 PLOTTED = ' ',
 GRANTEE = ' ',
 SALE_DATE = ' ',
 EFFECTIVE_DATE_OF_LEASE = ' ',
 EXPIRATION_DATE = ' ',
 ACRES = ' ',
 COUNTY = ' ',
 ST = ' ',
 STATUS_COMMENTS = ' ',
 EXPIRATION_YEAR = ' ',
 TOWNSHIP = ' ',
 RANGE_PLSS = ' ',
 DESCRIPTION_I = ' ',
 DESCRIPTION_II = ' ',
 DESCRIPTION_III = ' ';

select * from details 
where LEASE_NO = 'ALES51293';

INSERT INTO details 
(LEASE_NO, PLOTTED, GRANTEE, SALE_DATE, EFFECTIVE_DATE_OF_LEASE, EXPIRATION_DATE, ACRES, COUNTY, ST, STATUS_COMMENTS, EXPIRATION_YEAR, TOWNSHIP, RANGE_PLSS, DESCRIPTION_I, DESCRIPTION_II, DESCRIPTION_III)
VALUES ('ALES51293', 'NO', 'R&R Royalty', '2002-03-28', '2002-05-01', '2012-05-01', '80.25', 'LAMAR', 'AL', 'Expired 2012', '0000-00-00', NULL, NULL, 'SEE STIPULATIONS & LSE NOTICE', 'T16S,R16W HUNTSVILLE MERIDIAN', 'SEC 5, N2NE')
ON DUPLICATE KEY UPDATE
LEASE_NO = 'ALES51293', 
PLOTTED = 'NO', 
GRANTEE ='R&R Royalty', 
SALE_DATE = '2002-03-28', 
EFFECTIVE_DATE_OF_LEASE = '2002-05-01', 
EXPIRATION_DATE = '2012-05-01', 
ACRES = '80.25', 
COUNTY = 'LAMAR', 
ST = 'AL', 
STATUS_COMMENTS =  'Expired 2012', 
EXPIRATION_YEAR = '0000-00-00', 
TOWNSHIP = NULL, 
RANGE_PLSS = NULL, 
DESCRIPTION_I = 'SEE STIPULATIONS & LSE NOTICE', 
DESCRIPTION_II = 'T16S,R16W HUNTSVILLE MERIDIAN', 
DESCRIPTION_III = 'SEC 5, N2NE';

select * from details 
where LEASE_NO = 'ALES51293';


select count(1) from sale_info;
select count(1) from details;

select LEASE_NO, count(LEASE_NO) FROM sale_info
group by 1
having count(LEASE_NO) > 1;

select count(*) from sale_info;



-- Query to find data entry errors

select act.LEASE_NO, act.EXPIRATION_DATE, act.ACRES,COUNTY, i.TOTAL_INVESTMENT from v_activeAcreage act
join investment i 
on i.lease_no = act.lease_no
where total_investment is null;


-- Query to get active and not yet isseud leases

select * from details 
where expiration_date > curdate()
or upper(status_comments) like 'ISSUED%';

select * from official_counties;

select official_county, fips, count(lease_no) from official_counties
group by 1,2
order by 3 desc;

select * from v_activeAcreage d
inner join official_counties o
on o.lease_no = d.lease_no
where o.official_county like '%No Match%';

select count(*) from official_counties;

select lease_no, trim(lease_no), length(lease_no) as length, length(trim(lease_no)) as trimlength from details
where lease_no like '%UTU9482%';

select * from details 
where sale_date = '2020-12-17';

select * from details;

select * from details
where lease_no like '%WYW 190485%';

select count(1) from details;

select * from official_counties;

SELECT d.*, o.official_county, o.fips FROM details d
right JOIN official_counties o
ON o.lease_no = d.lease_no;

select lease_no from official_counties
where lease_no not in (select lease_no from details);

select * from details 
where lease_no like '%WYW189893%';

select i.lease_no, d.SALE_DATE, d.expiration_date from investment i
join details d on d.lease_no = i.lease_no
where total_investment is null;

select * from details
join official_counties o
on o.lease_no = details.lease_no
where official_county like '%No Match%';

Select d.*, c.OFFICIAL_COUNTY, c.FIPS, i.YEARS_RENEWED, i.RENTALS_PAID, i.TOTAL_INVESTMENT, i.Estimated_Bonus from details d
join official_counties c
on c.lease_no = d.lease_no
join investment i
on i.lease_no = c.lease_no;


select sum(acres) from details
where expiration_date > curdate();

select * from 
(
	select * from details
	where expiration_date > curdate()
		or expiration_date is null) a
where plotted = 'NO';

select count(distinct county) from details;

select *, rank() over(order by totalacres desc)
from
(
	select county, round(sum(acres),0) as totalacres
	from details
	group by 1
	order by 2 desc
) a;



select * from details d
inner join official_counties c
on d.lease_no = c.lease_no
where 
	c.official_county like lower('Lea');
    
select d.lease_no, c.official_county, d.acres, d.expiration_date from official_counties c
join details d on 
d.lease_no = c.lease_no
where c.official_county like lower(concat('%', 'Lea', '%'));

call findNullInvestments();

select lease_no, county, sale_date, status_comments
from details
where county is null;

select date_format(sale_date, '%Y')
from details;

