INSERT INTO ir_config_parameter (key, value)
VALUES ('sms.endpoint', 'https://iap-services-test.thrivebureau.com')
    ON CONFLICT (key) DO
       UPDATE SET value = 'https://iap-services-test.thrivebureau.com';
