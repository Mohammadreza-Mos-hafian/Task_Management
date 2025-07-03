CREATE TABLE public.tasks
(
    id          bigint                      NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    user_id     integer                     NOT NULL,
    title       character varying(32)       NOT NULL,
    description text,
    status      smallint                    NOT NULL,
    deadline    date,
    is_deleted  boolean                     NOT NULL DEFAULT False,
    created_at  timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at  timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

ALTER TABLE IF EXISTS public.tasks
    OWNER to postgres;

ALTER TABLE IF EXISTS public.tasks
    ALTER COLUMN deleted_at DROP NOT NULL;

ALTER TABLE IF EXISTS public.tasks
    ALTER COLUMN deleted_at DROP DEFAULT;