/** @thrive-module */

import spreadsheet from "@spreadsheet/o_spreadsheet/o_spreadsheet_extended";
const { otRegistry } = spreadsheet.registries;

otRegistry

    .addTransformation("INSERT_THRIVE_LIST", ["INSERT_THRIVE_LIST"], (toTransform) => ({
        ...toTransform,
        id: (parseInt(toTransform.id, 10) + 1).toString(),
    }))
    .addTransformation("REMOVE_THRIVE_LIST", ["RENAME_THRIVE_LIST"], (toTransform, executed) => {
      if (toTransform.listId === executed.listId) {
        return undefined;
      }
      return toTransform;
    })
    .addTransformation("REMOVE_THRIVE_LIST", ["RE_INSERT_THRIVE_LIST"], (toTransform, executed) => {
      if (toTransform.id === executed.listId) {
        return undefined;
      }
      return toTransform;
    });
