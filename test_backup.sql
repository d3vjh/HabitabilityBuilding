--
-- PostgreSQL database dump
--

-- Dumped from database version 13.11 (Debian 13.11-0+deb11u1)
-- Dumped by pg_dump version 13.11 (Debian 13.11-0+deb11u1)

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
    s_apartment_material character varying(50) NOT NULL,
    q_number_of_bedrooms integer NOT NULL,
    q_number_of_occupants integer NOT NULL,
    b_is_habitable boolean NOT NULL,
    k_building integer NOT NULL,
    q_temperature integer,
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
    k_apartment integer NOT NULL,
    s_activity character varying(20) NOT NULL
);


ALTER TABLE public.person OWNER TO postgres;

--
-- Data for Name: apartment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.apartment (k_apartment, q_air_humidity, s_apartment_material, q_number_of_bedrooms, q_number_of_occupants, b_is_habitable, k_building, q_temperature) FROM stdin;
102	50	Hormigón	1	0	f	1	0
202	50	Hormigón	1	0	f	1	0
301	50	Hormigón	1	0	f	1	0
405	50	Hormigón	3	0	f	1	0
502	50	Hormigón	1	0	f	1	0
604	50	Hormigón	2	0	f	1	0
703	50	Hormigón	2	0	f	1	0
704	50	Hormigón	2	0	f	1	0
101	50	Hormigón	1	2	f	1	0
205	50	Hormigón	3	3	f	1	0
204	50	Hormigón	2	1	f	1	0
302	50	Hormigón	1	1	f	1	0
304	50	Hormigón	2	1	f	1	0
305	50	Hormigón	3	1	f	1	0
501	50	Hormigón	1	1	f	1	0
505	50	Hormigón	3	2	f	1	0
602	50	Hormigón	1	2	f	1	0
603	50	Hormigón	2	3	f	1	0
303	50	Hormigón	2	1	t	1	0
503	50	Hormigón	2	2	t	1	0
404	50	Hormigón	2	1	t	1	0
401	30	Hormigón	1	1	f	1	0
504	30	Hormigón	2	0	f	1	0
702	30	Hormigón	1	0	f	1	0
601	30	Hormigón	1	2	f	1	0
701	10	Hormigón	1	0	f	1	0
605	10	Hormigón	3	0	f	1	0
105	10	Hormigón	3	0	f	1	0
201	10	Hormigón	1	1	f	1	0
403	10	Hormigón	2	1	t	1	0
705	10	Hormigón	3	1	f	1	0
103	30	Hormigón	2	2	t	1	0
104	50	Hormigón	2	4	f	1	0
203	30	Hormigón	2	0	f	1	0
402	50	Hormigón	1	3	t	1	0
\.


--
-- Data for Name: building; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.building (k_building, q_radiaton_level) FROM stdin;
1	4033.3
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

COPY public.person (k_person, s_name, s_last_name, s_clothing_type, k_apartment, s_activity) FROM stdin;
100030222	Sebastian	Gonzalez	Casual	601	Reposo
100008607	Catalina	Sanchez	Casual	104	Reposo
100030612	Catalina	Rodriguez	Casual	404	Reposo
100022955	Felipe	Alvarez	Casual	401	Ligera
100008047	Laura	Sanchez	Casual	603	Ligera
100008823	Catalina	Moreno	Casual	402	Moderada
100014941	Hanna	Moreno	Casual	603	Moderada
100015328	Juan	Alvarez	Casual	705	Moderada
100006548	Felipe	Sanchez	Casual	205	Intensa
100010875	Jhonatan	Jimenez	Casual	602	Intensa
100030891	Jhonatan	Alvarez	Casual	603	Reposo
100000791	Ana	Hernandez	Casual	204	Reposo
100027475	Carlos	Diaz	Casual	602	Ligera
100019502	Jhonatan	Sanchez	Casual	501	Ligera
100010158	Santiago	Sanchez	Casual	503	Ligera
100011245	Emmanuel	Garcia	Casual	503	Moderada
100018704	Sergio	Jimenez	Casual	205	Moderada
100006930	Laura	Diaz	Casual	104	Intensa
100014935	Juan	Hernandez	Casual	201	Intensa
100002315	Maria	Alvarez	Casual	504	Intensa
100007289	Maria	Gonzalez	Casual	101	Reposo
100030886	Ana	Rodriguez	Casual	302	Reposo
100011303	Jhonatan	Gonzalez	Casual	504	Reposo
100030982	Carlos	Moreno	Casual	205	Ligera
100001291	Luis	Alvarez	Casual	403	Ligera
100015945	Laura	Preciado	Casual	101	Ligera
100022843	Felipe	Preciado	Casual	305	Reposo
100024728	Luis	Preciado	Casual	304	Ligera
100019408	Sebastian	Preciado	Casual	601	Intensa
1010101010	Sofia	Vergara	Casual	303	Ligera
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

