// Copyright (c) 2025, Equipment and contributors
// For license information, please see license.txt
frappe.ui.form.on('Equipment Lease Contract', {
    start_date: function(frm) {
        validate_and_calculate(frm);
    },
    end_date: function(frm) {
        validate_and_calculate(frm);
    }
});

function validate_and_calculate(frm) {
    if (frm.doc.start_date && frm.doc.end_date) {
        if (frm.doc.end_date < frm.doc.start_date) {
            frappe.msgprint({
                title: __('Invalid Dates'),
                message: __('End Date cannot be before Start Date'),
                indicator: 'red',
                alert: true
            });
            frm.set_value('end_date', '');
            frm.set_value('contract_duration_days', 0);
            return;
        }

        let start = frappe.datetime.str_to_obj(frm.doc.start_date);
        let end = frappe.datetime.str_to_obj(frm.doc.end_date);
        let diff = frappe.datetime.get_diff(end, start) + 1;
        frm.set_value('contract_duration_days', diff);
    }
}
