thrive.define('website_crm.tour', function(require) {
    'use strict';

    const tour = require('web_tour.tour');
    const wTourUtils = require('website.tour_utils');

    wTourUtils.registerWebsitePreviewTour('website_crm_pre_tour', {
        test: true,
        url: '/contactus',
        edition: true,
    }, [{
        content: "Select contact form",
        trigger: "iframe #wrap.o_editable section.s_website_form",
        extra_trigger: "iframe body.editor_enable",
    }, {
        content: "Open action select",
        trigger: "we-select:has(we-button:contains('Create an Opportunity')) we-toggler",
        extra_trigger: "#oe_snippets .o_we_customize_snippet_btn.active",
    }, {
        content: "Select 'Create an Opportunity' as form action",
        trigger: "we-select we-button:contains('Create an Opportunity')",
    }, {
        content: "Save the settings",
        trigger: "button[data-action=save]",
    }, {
        content: "Ensure form model has changed and page reload is done after save",
        trigger: "iframe section.s_website_form form[data-model_name='crm.lead']",
        extra_trigger: "iframe body:not(.editor_enable)",
    }]);

    tour.register('website_crm_tour', {
        test: true,
        url: '/contactus',
    }, [{
        content: "Complete name",
        trigger: "input[name=contact_name]",
        run: "text John Smith",
    }, {
        content: "Complete phone number",
        trigger: "input[name=phone]",
        run: "text +32 485 118.218"
    }, {
        content: "Complete Email",
        trigger: "input[name=email_from]",
        run: "text john@smith.com"
    }, {
        content: "Complete Company",
        trigger: "input[name=partner_name]",
        run: "text Thrive Bureau ERP"
    }, {
        content: "Complete Subject",
        trigger: "input[name=name]",
        run: "text Useless message"
    }, {
        content: "Complete Subject",
        trigger: "textarea[name=description]",
        run: "text ### TOUR DATA ###"
    }, {
        content: "Send the form",
        trigger: ".s_website_form_send"
    }, {
        content: "Check we were redirected to the success page",
        trigger: "#wrap:has(h1:contains('Thank You!'))"
    }]);

    tour.register('website_crm_catch_logged_partner_info_tour', {
        test: true,
        url: '/contactus',
    }, [{
        content: "Complete Subject",
        trigger: "input[name=name]",
        run: "text Useless subject"
    }, {
        content: "Complete Subject",
        trigger: "textarea[name=description]",
        run: "text ### TOUR DATA PREFILL ###"
    }, {
        content: "Send the form",
        trigger: ".s_website_form_send"
    }, {
        content: "Check we were redirected to the success page",
        trigger: "#wrap:has(h1:contains('Thank You!'))"
    }]);

    return {};
});
