/** @thrive-module **/

import tour from 'web_tour.tour';
import tourUtils from 'website_sale.tour_utils';

tour.register('shop_buy_rental_product', {
    test: true,
    url: '/shop',
},
    [
        {
            content: "Search computer write text",
            trigger: 'form input[name="search"]',
            run: "text computer",
        },
        {
            content: "Search computer click",
            trigger: 'form:has(input[name="search"]) .oe_search_button',
        },
        {
            content: "Select computer",
            trigger: '.oe_product_cart:first a:contains("Computer")',
        },
        {
            content: "Open daterangepicker",
            trigger: '#rentingDates [data-toggle="daterange"]',
        },
        {
            content: "Change hours",
            extra_trigger: '.daterangepicker.o_website_sale_renting',
            trigger: '#rentingDates input',
            run: function () {
                const daterangepicker = this.$anchor.data('daterangepicker');
                daterangepicker.setEndDate(daterangepicker.endDate.add(3, 'hours'));
            }
        },
        {
            content: "Apply change",
            trigger: '.daterangepicker.o_website_sale_renting button.applyBtn',
        },
        {
            content: "Add one quantity",
            trigger: '.css_quantity a.js_add_cart_json i.fa-plus',
        },
        {
            content: "click on add to cart",
            trigger: '#product_detail form[action^="/shop/cart/update"] #add_to_cart',
        },
        tourUtils.goToCart({quantity: 2}),
        {
            content: "Verify there is a Computer",
            trigger: '#cart_products tbody td.td-product_name a strong:contains("Computer")',
            run: function () {}, // it's a check
        },
        {
            content: "Verify there are 2 quantity of Computers",
            trigger: '#cart_products tbody td.td-qty div.css_quantity input[value=2]',
            run: function () {}, // it's a check
        },
        {
            content: "go to checkout",
            extra_trigger: '#cart_products .oe_currency_value:contains(14.00)',
            trigger: 'a[href*="/shop/checkout"]',
        },
    ]
);
