/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";


publicWidget.registry.CustomerControllerPage = publicWidget.Widget.extend({
     selector: ".fetch-button",
     events: {
            'click': '_onClickFetch'
        },

     _onClickFetch: function(event){
        var email = $('#email').val();
        $('.custom-label').text('')
        rpc('/customer/fetch-customer',{'email':email}).then(
            function(data){
            if (data.found){
                $('#customer_not_found_message').text('Customer not found');
            }else{
                $('#name').text('Name: '+data.name);
                $('#company').text('Company Name: '+data.company);
                $('#taxID').text('Tax ID: '+data.vat);
                $('#phone').text('Phone: '+data.phone);
            }
            });
     },
})