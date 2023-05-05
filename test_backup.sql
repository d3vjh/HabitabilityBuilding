--
-- PostgreSQL database dump
--

-- Dumped from database version 13.10 (Debian 13.10-0+deb11u1)
-- Dumped by pg_dump version 13.10 (Debian 13.10-0+deb11u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: apartment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.apartment (
    k_id_apartment integer NOT NULL,
    k_id_building integer,
    q_air_humidity integer,
    q_ambient_air_temperature integer,
    n_apartment_material character varying(30),
    q_quantity_room integer,
    q_quantity_person integer,
    b_is_habitable boolean
);


ALTER TABLE public.apartment OWNER TO postgres;

--
-- Name: apartment_k_id_apartment_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.apartment_k_id_apartment_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.apartment_k_id_apartment_seq OWNER TO postgres;

--
-- Name: apartment_k_id_apartment_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.apartment_k_id_apartment_seq OWNED BY public.apartment.k_id_apartment;


--
-- Name: building; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.building (
    k_id_building integer NOT NULL,
    n_namebuilding character varying(30),
    q_radiaton numeric(4,1),
    n_ubication character varying(30)
);


ALTER TABLE public.building OWNER TO postgres;

--
-- Name: building_k_id_building_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.building_k_id_building_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.building_k_id_building_seq OWNER TO postgres;

--
-- Name: building_k_id_building_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.building_k_id_building_seq OWNED BY public.building.k_id_building;


--
-- Name: neighbor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.neighbor (
    k_id_apartment1 integer NOT NULL,
    k_id_apartment2 integer NOT NULL
);


ALTER TABLE public.neighbor OWNER TO postgres;

--
-- Name: person; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.person (
    k_id_person integer NOT NULL,
    k_id_apartment integer NOT NULL,
    n_name_person character varying(50),
    n_lastname_person character varying(50),
    n_person_clothing character varying(150),
    q_work character varying(50)
);


ALTER TABLE public.person OWNER TO postgres;

--
-- Name: person_k_id_person_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.person_k_id_person_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.person_k_id_person_seq OWNER TO postgres;

--
-- Name: person_k_id_person_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.person_k_id_person_seq OWNED BY public.person.k_id_person;


--
-- Name: apartment k_id_apartment; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.apartment ALTER COLUMN k_id_apartment SET DEFAULT nextval('public.apartment_k_id_apartment_seq'::regclass);


--
-- Name: building k_id_building; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.building ALTER COLUMN k_id_building SET DEFAULT nextval('public.building_k_id_building_seq'::regclass);


--
-- Name: person k_id_person; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person ALTER COLUMN k_id_person SET DEFAULT nextval('public.person_k_id_person_seq'::regclass);


--
-- Data for Name: apartment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.apartment (k_id_apartment, k_id_building, q_air_humidity, q_ambient_air_temperature, n_apartment_material, q_quantity_room, q_quantity_person, b_is_habitable) FROM stdin;
101	1	\N	\N	Concreto	\N	\N	\N
102	1	\N	\N	Concreto	\N	\N	\N
103	1	\N	\N	Concreto	\N	\N	\N
104	1	\N	\N	Concreto	\N	\N	\N
105	1	\N	\N	Concreto	\N	\N	\N
201	1	\N	\N	Concreto	\N	\N	\N
202	1	\N	\N	Concreto	\N	\N	\N
203	1	\N	\N	Concreto	\N	\N	\N
204	1	\N	\N	Concreto	\N	\N	\N
205	1	\N	\N	Concreto	\N	\N	\N
301	1	\N	\N	Concreto	\N	\N	\N
302	1	\N	\N	Concreto	\N	\N	\N
303	1	\N	\N	Concreto	\N	\N	\N
304	1	\N	\N	Concreto	\N	\N	\N
305	1	\N	\N	Concreto	\N	\N	\N
401	1	\N	\N	Concreto	\N	\N	\N
402	1	\N	\N	Concreto	\N	\N	\N
403	1	\N	\N	Concreto	\N	\N	\N
404	1	\N	\N	Concreto	\N	\N	\N
405	1	\N	\N	Concreto	\N	\N	\N
501	1	\N	\N	Concreto	\N	\N	\N
502	1	\N	\N	Concreto	\N	\N	\N
503	1	\N	\N	Concreto	\N	\N	\N
504	1	\N	\N	Concreto	\N	\N	\N
505	1	\N	\N	Concreto	\N	\N	\N
601	1	\N	\N	Concreto	\N	\N	\N
602	1	\N	\N	Concreto	\N	\N	\N
603	1	\N	\N	Concreto	\N	\N	\N
604	1	\N	\N	Concreto	\N	\N	\N
605	1	\N	\N	Concreto	\N	\N	\N
701	1	\N	\N	Concreto	\N	\N	\N
702	1	\N	\N	Concreto	\N	\N	\N
703	1	\N	\N	Concreto	\N	\N	\N
704	1	\N	\N	Concreto	\N	\N	\N
705	1	\N	\N	Concreto	\N	\N	\N
\.


--
-- Data for Name: building; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.building (k_id_building, n_namebuilding, q_radiaton, n_ubication) FROM stdin;
1	Edificio Sede Ingeniería	20.2	Calle 12 N 3 F 32
\.


--
-- Data for Name: neighbor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.neighbor (k_id_apartment1, k_id_apartment2) FROM stdin;
\.


--
-- Data for Name: person; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.person (k_id_person, k_id_apartment, n_name_person, n_lastname_person, n_person_clothing, q_work) FROM stdin;
1	101	Jhonatan	Moreno	\N	\N
6	101	David	Barragan	\N	\N
12	102	Carlos	Pedraza	\N	\N
13	104	Maria	Gonzales	\N	\N
14	105	Carmenza	Mora	\N	\N
\.


--
-- Name: apartment_k_id_apartment_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.apartment_k_id_apartment_seq', 1, false);


--
-- Name: building_k_id_building_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.building_k_id_building_seq', 1, false);


--
-- Name: person_k_id_person_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.person_k_id_person_seq', 14, true);


--
-- Name: apartment apartments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.apartment
    ADD CONSTRAINT apartments_pkey PRIMARY KEY (k_id_apartment);


--
-- Name: building building_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.building
    ADD CONSTRAINT building_pkey PRIMARY KEY (k_id_building);


--
-- Name: neighbor neighbors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.neighbor
    ADD CONSTRAINT neighbors_pkey PRIMARY KEY (k_id_apartment1, k_id_apartment2);


--
-- Name: person person_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person
    ADD CONSTRAINT person_pkey PRIMARY KEY (k_id_person);


--
-- Name: apartment apartments_k_id_building_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.apartment
    ADD CONSTRAINT apartments_k_id_building_fkey FOREIGN KEY (k_id_building) REFERENCES public.building(k_id_building);


--
-- Name: neighbor neighbors_k_id_apartment1_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.neighbor
    ADD CONSTRAINT neighbors_k_id_apartment1_fkey FOREIGN KEY (k_id_apartment1) REFERENCES public.apartment(k_id_apartment);


--
-- Name: neighbor neighbors_k_id_apartment2_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.neighbor
    ADD CONSTRAINT neighbors_k_id_apartment2_fkey FOREIGN KEY (k_id_apartment2) REFERENCES public.apartment(k_id_apartment);


--
-- Name: person person_k_idapartment_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person
    ADD CONSTRAINT person_k_idapartment_fkey FOREIGN KEY (k_id_apartment) REFERENCES public.apartment(k_id_apartment);


--
-- PostgreSQL database dump complete
--

