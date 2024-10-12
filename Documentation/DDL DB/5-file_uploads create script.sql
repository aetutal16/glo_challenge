-- Table: public.file_uploads

-- SEQUENCE: public.file_uploads_id_seq

-- DROP SEQUENCE IF EXISTS public.file_uploads_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.file_uploads_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.file_uploads_id_seq
    OWNED BY public.file_uploads.id;

ALTER SEQUENCE public.file_uploads_id_seq
    OWNER TO postgres;


-- DROP TABLE IF EXISTS public.file_uploads;

CREATE TABLE IF NOT EXISTS public.file_uploads
(
    id integer NOT NULL DEFAULT nextval('file_uploads_id_seq'::regclass),
    file_name character varying(255) COLLATE pg_catalog."default",
    file_hash character varying(64) COLLATE pg_catalog."default",
    creation_date timestamp with time zone DEFAULT now(),
    CONSTRAINT file_uploads_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.file_uploads
    OWNER to postgres;