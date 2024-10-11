-- Table: public.fact_hired_employees

-- DROP TABLE IF EXISTS public.fact_hired_employees;

CREATE TABLE IF NOT EXISTS public.fact_hired_employees
(
    id integer,
    name text COLLATE pg_catalog."default",
    datetime text COLLATE pg_catalog."default",
    department_id integer,
    job_id integer,
    creation_date timestamp with time zone DEFAULT now(),
    CONSTRAINT fact_hired_employees_department_id_fkey FOREIGN KEY (department_id)
        REFERENCES public.dim_departments (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT fact_hired_employees_job_id_fkey FOREIGN KEY (job_id)
        REFERENCES public.dim_jobs (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.fact_hired_employees
    OWNER to postgres;