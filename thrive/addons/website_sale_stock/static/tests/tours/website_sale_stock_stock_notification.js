/** @thrive-module **/

import tour from 'web_tour.tour';

tour.register('back_in_stock_notification_product', {
        test: true,
        url: '/shop?search=Macbook%20Pro',
    },
    [
        {
            content: "Open product page",
            trigger: 'a:contains("Macbook Pro")',
        },
        {
            content: "Click on 'Be notified when back in stock'",
            trigger: '#product_stock_notification_message',
        },
        {
            content: "Fill email form",
            trigger: 'div[id="stock_notification_form"] input[name="email"]',
            run: 'text test@test.test',
        },
        {
            content: "Click on the button",
            trigger: '#product_stock_notification_form_submit_button',
        },
        {
            content: "Success Message",
            trigger: '#stock_notification_success_message',
        },
    ],
);