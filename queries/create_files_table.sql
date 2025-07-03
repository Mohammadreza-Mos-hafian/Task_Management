CREATE TABLE public.files
(
    id            bigint                 NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    task_id       bigint                 NOT NULL,
    file_path     character varying(255) NOT NULL,
    original_name character varying(64)  NOT NULL,
    is_deleted    boolean                NOT NULL DEFAULT False,
    created_at    timestamp without time zone     DEFAULT CURRENT_TIMESTAMP,
    updated_at    timestamp without time zone     DEFAULT CURRENT_TIMESTAMP,
    deleted_at    timestamp without time zone     DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (task_id)
        REFERENCES public.tasks (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

ALTER TABLE IF EXISTS public.files
    OWNER to postgres;

ALTER TABLE IF EXISTS public.files
    ALTER COLUMN created_at SET NOT NULL;

ALTER TABLE IF EXISTS public.files
    ALTER COLUMN updated_at SET NOT NULL;

ALTER TABLE IF EXISTS public.files
    ALTER COLUMN deleted_at DROP DEFAULT;