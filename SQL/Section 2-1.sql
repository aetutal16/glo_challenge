-----------------------------------------
--This query was created for PostgreSQL
-----------------------------------------


-------------------------------------
--Create the view for the first requirement:
--Number of employees hired for each job and department in 2021 divided by quarter. The
--table must be ordered alphabetically by department and job.
-------------------------------------


select 
	dim_departments.department,
	dim_jobs.job dept_job,
	extract(QUARTER from (fact_hired_employees.datetime::TIMESTAMPTZ) AT TIME ZONE 'UTC') Q,
	count(fact_hired_employees.id) total_hired 
from
	public.fact_hired_employees
	left join public.dim_jobs 
		on fact_hired_employees.job_id = dim_jobs.id
	left join public.dim_departments 
		on fact_hired_employees.department_id = dim_departments.id
where
	extract(YEAR FROM (fact_hired_employees.datetime::TIMESTAMPTZ) AT TIME ZONE 'UTC') = 2021
group by
	dim_departments.department,
	dim_jobs.job,
	Q
ORDER BY 1, 2

;