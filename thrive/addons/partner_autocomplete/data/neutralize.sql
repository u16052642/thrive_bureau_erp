INSERT INTO ir_config_parameter (key, value)
VALUES ('iap.partner_autocomplete.endpoint', 'https://iap-services-test.ThriveERP.com')
    ON CONFLICT (key) DO
       UPDATE SET value = 'https://iap-services-test.ThriveERP.com';
