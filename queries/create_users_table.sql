CREATE TABLE public.users
(
    id         integer                     NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    first_name character varying(32)       NOT NULL,
    last_name  character varying(32)       NOT NULL,
    email      character varying(64)       NOT NULL,
    password   character varying           NOT NULL,
    is_deleted boolean                     NOT NULL DEFAULT FALSE,
    created_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (email)
);

ALTER TABLE IF EXISTS public.users
    OWNER to postgres;

ALTER TABLE IF EXISTS public.users
    ALTER COLUMN deleted_at DROP NOT NULL;

ALTER TABLE IF EXISTS public.users
    ALTER COLUMN deleted_at DROP DEFAULT;