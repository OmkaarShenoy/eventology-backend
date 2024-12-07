--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: roleenum; Type: TYPE; Schema: public; Owner: eventology_db_owner
--

CREATE TYPE public.roleenum AS ENUM (
    'participant',
    'organizer'
);


ALTER TYPE public.roleenum OWNER TO eventology_db_owner;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: checkins; Type: TABLE; Schema: public; Owner: eventology_db_owner
--

CREATE TABLE public.checkins (
    checkin_id integer NOT NULL,
    user_id character varying NOT NULL,
    subevent_id integer NOT NULL,
    checkin_time timestamp without time zone NOT NULL,
    checked_in_by character varying NOT NULL,
    points integer
);


ALTER TABLE public.checkins OWNER TO eventology_db_owner;

--
-- Name: checkins_checkin_id_seq; Type: SEQUENCE; Schema: public; Owner: eventology_db_owner
--

CREATE SEQUENCE public.checkins_checkin_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.checkins_checkin_id_seq OWNER TO eventology_db_owner;

--
-- Name: checkins_checkin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: eventology_db_owner
--

ALTER SEQUENCE public.checkins_checkin_id_seq OWNED BY public.checkins.checkin_id;


--
-- Name: events; Type: TABLE; Schema: public; Owner: eventology_db_owner
--

CREATE TABLE public.events (
    event_id integer NOT NULL,
    event_name character varying NOT NULL,
    description text,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone NOT NULL,
    location character varying NOT NULL,
    user_id character varying NOT NULL
);


ALTER TABLE public.events OWNER TO eventology_db_owner;

--
-- Name: events_event_id_seq; Type: SEQUENCE; Schema: public; Owner: eventology_db_owner
--

CREATE SEQUENCE public.events_event_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.events_event_id_seq OWNER TO eventology_db_owner;

--
-- Name: events_event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: eventology_db_owner
--

ALTER SEQUENCE public.events_event_id_seq OWNED BY public.events.event_id;


--
-- Name: leaderboard_entries; Type: TABLE; Schema: public; Owner: eventology_db_owner
--

CREATE TABLE public.leaderboard_entries (
    id integer NOT NULL,
    event_id integer NOT NULL,
    user_id character varying NOT NULL,
    points integer NOT NULL
);


ALTER TABLE public.leaderboard_entries OWNER TO eventology_db_owner;

--
-- Name: leaderboard_entries_id_seq; Type: SEQUENCE; Schema: public; Owner: eventology_db_owner
--

CREATE SEQUENCE public.leaderboard_entries_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.leaderboard_entries_id_seq OWNER TO eventology_db_owner;

--
-- Name: leaderboard_entries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: eventology_db_owner
--

ALTER SEQUENCE public.leaderboard_entries_id_seq OWNED BY public.leaderboard_entries.id;


--
-- Name: subevents; Type: TABLE; Schema: public; Owner: eventology_db_owner
--

CREATE TABLE public.subevents (
    subevent_id integer NOT NULL,
    subevent_name character varying NOT NULL,
    description text,
    event_id integer NOT NULL,
    points integer,
    datetime timestamp without time zone
);


ALTER TABLE public.subevents OWNER TO eventology_db_owner;

--
-- Name: subevents_subevent_id_seq; Type: SEQUENCE; Schema: public; Owner: eventology_db_owner
--

CREATE SEQUENCE public.subevents_subevent_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.subevents_subevent_id_seq OWNER TO eventology_db_owner;

--
-- Name: subevents_subevent_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: eventology_db_owner
--

ALTER SEQUENCE public.subevents_subevent_id_seq OWNED BY public.subevents.subevent_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: eventology_db_owner
--

CREATE TABLE public.users (
    user_id character varying NOT NULL,
    email character varying NOT NULL,
    hashed_password character varying NOT NULL,
    first_name character varying,
    last_name character varying,
    role public.roleenum NOT NULL,
    total_points integer
);


ALTER TABLE public.users OWNER TO eventology_db_owner;

--
-- Name: checkins checkin_id; Type: DEFAULT; Schema: public; Owner: eventology_db_owner
--

ALTER TABLE ONLY public.checkins ALTER COLUMN checkin_id SET DEFAULT nextval('public.checkins_checkin_id_seq'::regclass);


--
-- Name: events event_id; Type: DEFAULT; Schema: public; Owner: eventology_db_owner
--

ALTER TABLE ONLY public.events ALTER COLUMN event_id SET DEFAULT nextval('public.events_event_id_seq'::regclass);


--
-- Name: leaderboard_entries id; Type: DEFAULT; Schema: public; Owner: eventology_db_owner
--

ALTER TABLE ONLY public.leaderboard_entries ALTER COLUMN id SET DEFAULT nextval('public.leaderboard_entries_id_seq'::regclass);


--
-- Name: subevents subevent_id; Type: DEFAULT; Schema: public; Owner: eventology_db_owner
--

ALTER TABLE ONLY public.subevents ALTER COLUMN subevent_id SET DEFAULT nextval('public.subevents_subevent_id_seq'::regclass);


--
-- Data for Name: checkins; Type: TABLE DATA; Schema: public; Owner: eventology_db_owner
--

COPY public.checkins (checkin_id, user_id, subevent_id, checkin_time, checked_in_by, points) FROM stdin;
1	0e74afd9-b0d7-4be1-bbb6-80c193a1c0f0	1	2024-12-07 02:04:21.882908	ab979872-b7bc-4bc7-8f38-5a0b07c91bed	30
6	05db7bb3-7752-48a5-9449-23022ef93d5d	12	2024-12-07 03:59:09.574265	05db7bb3-7752-48a5-9449-23022ef93d5d	20
\.


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: eventology_db_owner
--

COPY public.events (event_id, event_name, description, start_date, end_date, location, user_id) FROM stdin;
1495415424	Tote Bag Painting	PAINT	2024-12-04 00:00:00	2024-12-06 00:00:00	Tooker Lounge	899b9a99-8035-4d5a-a377-51a569d00121
1	sunhacks	24 hour hackathon	2024-05-23 07:00:00	2024-05-23 07:00:00	SDFC	899b9a99-8035-4d5a-a377-51a569d00121
1539951361	Finals Study Session	Study for finals	2024-12-11 07:00:00	2024-12-11 07:00:00	Tooker House 6th Floor	899b9a99-8035-4d5a-a377-51a569d00121
-84699685	Test Event - Harsh	Harsh K.	2024-12-06 00:00:00	2024-12-06 00:00:00	Tempe, AZ	ab979872-b7bc-4bc7-8f38-5a0b07c91bed
-84137818	Final Test 1	Test 1.	2024-12-06 00:00:00	2024-12-13 00:00:00	Tempe, AZ	ab979872-b7bc-4bc7-8f38-5a0b07c91bed
-1511383272	Cooking Class	Come learn how to cook with us!	2024-12-10 08:00:00	2024-12-10 07:00:00	Memorial Union	05db7bb3-7752-48a5-9449-23022ef93d5d
\.


--
-- Data for Name: leaderboard_entries; Type: TABLE DATA; Schema: public; Owner: eventology_db_owner
--

COPY public.leaderboard_entries (id, event_id, user_id, points) FROM stdin;
2	-84699685	0e74afd9-b0d7-4be1-bbb6-80c193a1c0f0	50
3	-84699685	5c15eef8-a3e6-4dac-86a0-c0eb214854d3	60
5	-1511383272	05db7bb3-7752-48a5-9449-23022ef93d5d	20
\.


--
-- Data for Name: subevents; Type: TABLE DATA; Schema: public; Owner: eventology_db_owner
--

COPY public.subevents (subevent_id, subevent_name, description, event_id, points, datetime) FROM stdin;
1	Test 1	This is a test.	-84699685	30	2024-12-07 01:00:00
2	Test 2	Test 2	-84699685	40	2024-12-06 18:36:00
4	Test 3	Test 3	-84699685	50	2024-12-06 18:38:00
6	Test 4	Work now please.	-84699685	60	2024-12-06 18:40:00
8	Test 7	Test	-84137818	90	2024-12-07 03:12:00
10	Test 8	Test.	-84137818	100	2024-12-06 15:15:00
12	Introduction to Cooking	Come hear what we will be cooking today!	-1511383272	20	2024-12-09 14:00:00
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: eventology_db_owner
--

COPY public.users (user_id, email, hashed_password, first_name, last_name, role, total_points) FROM stdin;
899b9a99-8035-4d5a-a377-51a569d00121	nshibuel@asu.edu	$2b$12$R0lZGO8DwvtJHvbiXXN.ze89uTAQz43RdPUEHoxnp2dSUIPkDC/06	Nandana	Elizabeth	organizer	0
ab979872-b7bc-4bc7-8f38-5a0b07c91bed	hkumar30@asu.edu	$2b$12$a/vvt5FycaRywebTkvAvle4a7Q63FsQ1equfxC5RI3aSseXCLxV.O	Harsh	K.	organizer	0
5c15eef8-a3e6-4dac-86a0-c0eb214854d3	amalshifwathshaik@gmail.com	$2b$12$5sbZRnMzFcMNJFeMiXI2OeWk8JxjXsN02vDdLTTslmcoLIMOtIQ5y	Amal Shifwath	Shaik	participant	0
0b3b60c7-3f1e-4591-af70-fc0b0f1acf63	hkumar8180@gmail.com	$2b$12$wretp9gvKtR9QRyzcTPuZeUcStjXvROpgmjvFLaXv5k1q5x9KXQNq	Harsh	K.	organizer	0
0e74afd9-b0d7-4be1-bbb6-80c193a1c0f0	oshenoy@asu.edu	$2b$12$hDhvN/9zBWY/BAHLNsTzoOKk..w/Ym99LdK0xowD1I0hYhPCroVlW	Ansh	Gopinath	organizer	0
05db7bb3-7752-48a5-9449-23022ef93d5d	omkaarshenoyos@gmail.com	$2b$12$56maoGhL6vjK3RkHqX1VZ.a7tFz30eX1awKH0RqRj8MODAMaCq6gi	Omkaar	Shenoy	organizer	0
\.


--
-- Name: checkins_checkin_id_seq; Type: SEQUENCE SET; Schema: public; Owner: eventology_db_owner
--

SELECT pg_catalog.setval('public.checkins_checkin_id_seq', 6, true);


--
-- Name: events_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: eventology_db_owner
--

SELECT pg_catalog.setval('public.events_event_id_seq', 1, false);


--
-- Name: leaderboard_entries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: eventology_db_owner
--

SELECT pg_catalog.setval('public.leaderboard_entries_id_seq', 5, true);


--
-- Name: subevents_subevent_id_seq; Type: SEQUENCE SET; Schema: public; Owner: eventology_db_owner
--

SELECT pg_catalog.setval('public.subevents_subevent_id_seq', 12, true);


--
-- Name: checkins checkins_pkey; Type: CONSTRAINT; Schema: public; Owner: eventology_db_owner
--

ALTER TABLE ONLY public.checkins
    ADD CONSTRAINT checkins_pkey PRIMARY KEY (checkin_id);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: eventology_db_owner
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (event_id);


--
-- Name: leaderboard_entries leaderboard_entries_pkey; Type: CONSTRAINT; Schema: public; Owner: eventology_db_owner
--

ALTER TABLE ONLY public.leaderboard_entries
    ADD CONSTRAINT leaderboard_entries_pkey PRIMARY KEY (id);


--
-- Name: subevents subevents_pkey; Type: CONSTRAINT; Schema: public; Owner: eventology_db_owner
--

ALTER TABLE ONLY public.subevents
    ADD CONSTRAINT subevents_pkey PRIMARY KEY (subevent_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: eventology_db_owner
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: ix_checkins_checkin_id; Type: INDEX; Schema: public; Owner: eventology_db_owner
--

CREATE INDEX ix_checkins_checkin_id ON public.checkins USING btree (checkin_id);


--
-- Name: ix_events_event_id; Type: INDEX; Schema: public; Owner: eventology_db_owner
--

CREATE INDEX ix_events_event_id ON public.events USING btree (event_id);


--
-- Name: ix_leaderboard_entries_id; Type: INDEX; Schema: public; Owner: eventology_db_owner
--

CREATE INDEX ix_leaderboard_entries_id ON public.leaderboard_entries USING btree (id);


--
-- Name: ix_subevents_subevent_id; Type: INDEX; Schema: public; Owner: eventology_db_owner
--

CREATE INDEX ix_subevents_subevent_id ON public.subevents USING btree (subevent_id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: eventology_db_owner
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_user_id; Type: INDEX; Schema: public; Owner: eventology_db_owner
--

CREATE INDEX ix_users_user_id ON public.users USING btree (user_id);


--
-- Name: checkins checkins_checked_in_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: eventology_db_owner
--

ALTER TABLE ONLY public.checkins
    ADD CONSTRAINT checkins_checked_in_by_fkey FOREIGN KEY (checked_in_by) REFERENCES public.users(user_id);


--
-- Name: checkins checkins_subevent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: eventology_db_owner
--

ALTER TABLE ONLY public.checkins
    ADD CONSTRAINT checkins_subevent_id_fkey FOREIGN KEY (subevent_id) REFERENCES public.subevents(subevent_id) ON DELETE CASCADE;


--
-- Name: checkins checkins_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: eventology_db_owner
--

ALTER TABLE ONLY public.checkins
    ADD CONSTRAINT checkins_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: events events_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: eventology_db_owner
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: leaderboard_entries leaderboard_entries_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: eventology_db_owner
--

ALTER TABLE ONLY public.leaderboard_entries
    ADD CONSTRAINT leaderboard_entries_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(event_id);


--
-- Name: leaderboard_entries leaderboard_entries_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: eventology_db_owner
--

ALTER TABLE ONLY public.leaderboard_entries
    ADD CONSTRAINT leaderboard_entries_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: subevents subevents_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: eventology_db_owner
--

ALTER TABLE ONLY public.subevents
    ADD CONSTRAINT subevents_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(event_id);


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT ALL ON SEQUENCES TO neon_superuser WITH GRANT OPTION;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT ALL ON TABLES TO neon_superuser WITH GRANT OPTION;


--
-- PostgreSQL database dump complete
--

