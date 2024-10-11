-- Table: public.dim_jobs

-- DROP TABLE IF EXISTS public.dim_jobs;

CREATE TABLE IF NOT EXISTS public.dim_jobs
(
    id integer NOT NULL,
    job text COLLATE pg_catalog."default",
    creation_date timestamp with time zone DEFAULT now(),
    update_date timestamp with time zone,
    CONSTRAINT dim_jobs_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.dim_jobs
    OWNER to postgres;