-- disable sign_itsme
DO $$
    BEGIN
        INSERT INTO ir_config_parameter (key, value) VALUES ('sign_itsme.iap_endpoint', 'https://iap-services-test.thrivebureau.com');
    EXCEPTION
        WHEN unique_violation THEN UPDATE ir_config_parameter SET value = 'https://iap-services-test.thrivebureau.com' WHERE key = 'sign_itsme.iap_endpoint'; 
    END;
$$;