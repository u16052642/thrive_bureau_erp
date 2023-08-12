/** @thrive-module **/

import { registerPatch } from "@mail/model/model_core";
import { attr } from "@mail/model/model_field";

registerPatch({
    name: "Messaging",
    fields: {
        hasDocumentsUserGroup: attr({
            default: false,
        }),
    },
});
