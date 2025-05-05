/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.ContactFormPage = publicWidget.Widget.extend({
    selector: "#contact_form",
    events: {
        'click #save_button': '_onSaveClick',
        'click #edit_button': '_onEditClick',
    },
    _onSaveClick: function(event){
        event.preventDefault()

        var email = $('input[name="email"]').val();
        var phone = $('input[name="phone"]').val();

        var emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        var phoneRegex = /^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$/;

        var errorMessage = '';

        if (!emailRegex.test(email)) {
            errorMessage += 'Please enter a valid Email Address.<br>';
        }
        if (!phoneRegex.test(phone)) {
            errorMessage += 'Phone number must be between 10 to 15 digits.<br>';
        }

        if (errorMessage) {
            $('#error_message').html(errorMessage).fadeIn();
            return false;
        } else {
            $('#error_message').fadeOut();
            $('#contact_form input').prop('readonly', true);
            $('#edit_button').show();
            $('#save_button').hide();
            var email = $('#email').val();
            var contact_id = $('#contact_id').val();
            var address = $('#address').val();
            var name = $('#name').val();
            var website = $('#website').val();

            rpc('/save_contact',{
                contact_id: contact_id,
                email: email,
                phone: phone,
                name: name,
                website: website,
                address: address,
            }).then(function (result){
                if (result.status === 'success'){
                    alert('Saved successfully');
                } else{
                    $('#error_message').html(result.message).fadeIn();
                }
            });

        }
    },
    _onEditClick: function(event){
        event.preventDefault()
        $('#contact_form input').prop('readonly', false);
        $('#edit_button').hide();
        $('#save_button').show();
    },

})