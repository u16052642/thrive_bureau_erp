/** @thrive-module **/

import { DateTimePicker } from "@web/core/datepicker/datepicker";
import { areDateEquals, formatDateTime } from "@web/core/l10n/dates";
import { _lt } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "../standard_field_props";

import { Component } from "@thrive/owl";

export class DateTimeField extends Component {
    get formattedValue() {
        return formatDateTime(this.props.value);
    }

    onDateTimeChanged(date) {
        if (!areDateEquals(this.props.value || "", date)) {
            this.props.update(date);
        }
    }
}

DateTimeField.template = "web.DateTimeField";
DateTimeField.components = {
    DateTimePicker,
};
DateTimeField.props = {
    ...standardFieldProps,
    pickerOptions: { type: Object, optional: true },
    placeholder: { type: String, optional: true },
};
DateTimeField.defaultProps = {
    pickerOptions: {},
};

DateTimeField.displayName = _lt("Date & Time");
DateTimeField.supportedTypes = ["datetime"];

DateTimeField.extractProps = ({ attrs }) => {
    return {
        pickerOptions: attrs.options.datepicker,
        placeholder: attrs.placeholder,
    };
};

registry.category("fields").add("datetime", DateTimeField);
