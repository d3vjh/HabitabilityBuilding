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
    k_apartment integer NOT NULL,
    q_air_humidity integer NOT NULL,
    q_ambient_air_humidity integer NOT NULL,
    s_apartment_material character varying(50) NOT NULL,
    q_number_of_bedrooms integer NOT NULL,
    q_number_of_occupants integer NOT NULL,
    b_is_habitable boolean NOT NULL,
    k_building integer NOT NULL,
    CONSTRAINT ck_id_building CHECK ((k_building = 1))
);


ALTER TABLE public.apartment OWNER TO postgres;

--
-- Name: building; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.building (
    k_building integer NOT NULL,
    q_radiaton_level character varying(50) NOT NULL,
    CONSTRAINT chk_building CHECK ((k_building = 1))
);


ALTER TABLE public.building OWNER TO postgres;

--
-- Name: neighbor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.neighbor (
    k_apartment1 integer NOT NULL,
    k_apartment2 integer NOT NULL
);


ALTER TABLE public.neighbor OWNER TO postgres;

--
-- Name: person; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.person (
    k_person integer NOT NULL,
    s_name character varying(50) NOT NULL,
    s_last_name character varying(50) NOT NULL,
    s_clothing_type character varying(50) NOT NULL,
    k_apartment integer NOT NULL
);


ALTER TABLE public.person OWNER TO postgres;

--
-- Data for Name: apartment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.apartment (k_apartment, q_air_humidity, q_ambient_air_humidity, s_apartment_material, q_number_of_bedrooms, q_number_of_occupants, b_is_habitable, k_building) FROM stdin;
101	0	0	Concreto	1	0	f	1
102	0	0	Concreto	1	0	f	1
103	0	0	Concreto	2	0	f	1
104	0	0	Concreto	2	0	f	1
105	0	0	Concreto	3	0	f	1
201	0	0	Concreto	1	0	f	1
202	0	0	Concreto	1	0	f	1
203	0	0	Concreto	2	0	f	1
204	0	0	Concreto	2	0	f	1
205	0	0	Concreto	3	0	f	1
301	0	0	Concreto	1	0	f	1
302	0	0	Concreto	1	0	f	1
303	0	0	Concreto	2	0	f	1
304	0	0	Concreto	2	0	f	1
305	0	0	Concreto	3	0	f	1
401	0	0	Concreto	1	0	f	1
402	0	0	Concreto	1	0	f	1
403	0	0	Concreto	2	0	f	1
404	0	0	Concreto	2	0	f	1
405	0	0	Concreto	3	0	f	1
501	0	0	Concreto	1	0	f	1
502	0	0	Concreto	1	0	f	1
503	0	0	Concreto	2	0	f	1
504	0	0	Concreto	2	0	f	1
505	0	0	Concreto	3	0	f	1
601	0	0	Concreto	1	0	f	1
602	0	0	Concreto	1	0	f	1
603	0	0	Concreto	2	0	f	1
604	0	0	Concreto	2	0	f	1
605	0	0	Concreto	3	0	f	1
701	0	0	Concreto	1	0	f	1
702	0	0	Concreto	1	0	f	1
703	0	0	Concreto	2	0	f	1
704	0	0	Concreto	2	0	f	1
705	0	0	Concreto	3	0	f	1
\.


--
-- Data for Name: building; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.building (k_building, q_radiaton_level) FROM stdin;
1	radiaton
\.


--
-- Data for Name: neighbor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.neighbor (k_apartment1, k_apartment2) FROM stdin;
101	102
101	201
102	103
102	202
103	104
103	203
104	105
104	204
105	205
201	202
201	301
202	203
202	302
203	204
203	303
204	205
204	304
205	305
301	302
301	401
302	303
302	402
303	304
303	403
304	305
304	404
305	405
401	402
401	501
402	403
402	502
403	404
403	503
404	405
404	504
405	505
501	502
501	601
502	503
502	602
503	504
503	603
504	505
504	604
505	605
601	602
601	701
602	603
602	702
603	604
603	703
604	605
604	704
605	705
701	702
702	703
703	704
704	705
\.


--
-- Data for Name: person; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.person (k_person, s_name, s_last_name, s_clothing_type, k_apartment) FROM stdin;
100030222	Sebastian	Gonzalez	Desnudo	601
100030891	Jhonatan	Alvarez	Desnudo	603
100008823	Catalina	Moreno	Desnudo	402
100006930	Laura	Diaz	Desnudo	104
100008607	Catalina	Sanchez	Desnudo	104
100011245	Emmanuel	Garcia	Desnudo	503
100019408	Sebastian	Gonzalez	Desnudo	601
100014941	Hanna	Moreno	Desnudo	603
100014935	Juan	Hernandez	Desnudo	201
100022955	Felipe	Alvarez	Desnudo	401
100030612	Catalina	Rodriguez	Desnudo	404
100002315	Maria	Alvarez	Desnudo	504
100030982	Carlos	Moreno	Desnudo	205
100015328	Juan	Alvarez	Desnudo	705
100006548	Felipe	Sanchez	Desnudo	205
100027475	Carlos	Diaz	Desnudo	602
100026515	Jhonatan	Hernandez	Desnudo	203
100022843	Felipe	Sanchez	Desnudo	305
100008047	Laura	Sanchez	Desnudo	603
100019502	Jhonatan	Sanchez	Desnudo	501
100007289	Maria	Gonzalez	Desnudo	101
100030886	Ana	Rodriguez	Desnudo	302
100000791	Ana	Hernandez	Desnudo	204
100010875	Jhonatan	Jimenez	Desnudo	602
100018704	Sergio	Jimenez	Desnudo	205
100010158	Santiago	Sanchez	Desnudo	503
100024728	Luis	Alvarez	Desnudo	304
100001291	Luis	Alvarez	Desnudo	403
100011303	Jhonatan	Gonzalez	Desnudo	504
100015945	Laura	Sanchez	Desnudo	101
\.


--
-- Name: apartment pk_apartment; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.apartment
    ADD CONSTRAINT pk_apartment PRIMARY KEY (k_apartment);


--
-- Name: building pk_building; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.building
    ADD CONSTRAINT pk_building PRIMARY KEY (k_building);


--
-- Name: person pk_person; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person
    ADD CONSTRAINT pk_person PRIMARY KEY (k_person);


--
-- Name: apartment fk_apartment_building; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.apartment
    ADD CONSTRAINT fk_apartment_building FOREIGN KEY (k_building) REFERENCES public.building(k_building);


--
-- Name: neighbor fk_neighbor_apartment; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.neighbor
    ADD CONSTRAINT fk_neighbor_apartment FOREIGN KEY (k_apartment1) REFERENCES public.apartment(k_apartment);


--
-- Name: neighbor fk_neighbor_apartment_02; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.neighbor
    ADD CONSTRAINT fk_neighbor_apartment_02 FOREIGN KEY (k_apartment2) REFERENCES public.apartment(k_apartment);


--
-- Name: person fk_person_apartment; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person
    ADD CONSTRAINT fk_person_apartment FOREIGN KEY (k_apartment) REFERENCES public.apartment(k_apartment);


--
-- PostgreSQL database dump complete
--

