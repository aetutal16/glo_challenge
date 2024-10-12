-- Table: public.dim_departments

-- DROP TABLE IF EXISTS public.dim_departments;

CREATE TABLE IF NOT EXISTS public.dim_departments
(
    id integer NOT NULL,
    department text COLLATE pg_catalog."default",
    creation_date timestamp with time zone DEFAULT now(),
    update_date timestamp with time zone,
    CONSTRAINT dim_departments_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.dim_departments
    OWNER to postgres;