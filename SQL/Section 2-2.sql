-----------------------------------------
--This query was created for PostgreSQL
-----------------------------------------

-------------------------------
--Create the view with the second requirement
--List of ids, name and number of employees hired of each department that hired more
--employees than the mean of employees hired in 2021 for all the departments, ordered
--by the number of employees hired (descending).
-------------------------------

create or replace view requirement_2 as (
	with hired_by_dep as (
		select 
			coalesce(fact.department_id, -1) id, 
			coalesce(dep.department, 'N/A') department,
			count(fact.id) hired
		from
			public.fact_hired_employees fact
			left join 
				public.dim_departments dep on fact.department_id = dep.id
		where
			extract(YEAR FROM (fact.datetime::TIMESTAMPTZ) AT TIME ZONE 'UTC') = 2021
		group by
			fact.department_id, 
			dep.department
	)
	, avg_hired as (
		select 
			avg(hired) avg_hired
		from 
			hired_by_dep
	)
	select 
		 hired_by_dep.id,
		 hired_by_dep.department,
		 hired
	from
		hired_by_dep
	where 
		hired > (select * from avg_hired)
	order by 
		hired desc
); 
	
		

