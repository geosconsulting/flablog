--alter table annual_pop_flood


ALTER TABLE public.gaul_wfp_iso
    ADD CONSTRAINT sparc_gaul_wfp_adm2_code_pkey PRIMARY KEY (adm2_code);
	
	
select adm2_name,adm2_code from gaul_wfp_iso ou
where (select count(*) from gaul_wfp_iso inr
where inr.adm2_code = ou.adm2_code) > 1
