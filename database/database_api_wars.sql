ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS fk_user_id CASCADE;

DROP TABLE IF EXISTS public.users CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY NOT NULL,
    username varchar(30) NOT NULL,
    password varchar(500) NOT NULL,
    submission_time timestamp without time zone
);
