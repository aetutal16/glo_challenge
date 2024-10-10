-----------------------------------------
--This query was created for PostgreSQL
-----------------------------------------

--Import tablefunc
CREATE EXTENSION IF NOT EXISTS tablefunc;

-------------------------------------
--Create the view for the first requirement:
--Number of employees hired for each job and department in 2021 divided by quarter. The
--table must be ordered alphabetically by department and job.
-------------------------------------

create or replace view requirement_1 as (
	select 
		split_part(dept_job, '-', 1) department,
		split_part(dept_job, '-', 2) job,
		coalesce(q1,0) q1, 
		coalesce(q2,0) q2, 
		coalesce(q3,0) q3, 
		coalesce(q4,0) q4
	from crosstab(
	    $$
		select 
			--Concatenate the department and job columns to avoid weird behavior when pivot data
			coalesce(dim_departments.department, 'N/A') || '-' || coalesce(dim_jobs.job, 'N/A') dept_job,
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
	    $$,
	    $$ 
		--obtain all the possible values for quarters
		select 
				distinct extract(QUARTER from(datetime::TIMESTAMPTZ) AT TIME ZONE 'UTC')
			from
				public.fact_hired_employees 
			where 
				extract(QUARTER from(datetime::TIMESTAMPTZ) AT TIME ZONE 'UTC') is not null
			order by 1 $$
	) as pivot_table(
	    dept_job TEXT,
	    Q1 INT,
	    Q2 INT,
	    Q3 INT,
	    Q4 INT
	)
);