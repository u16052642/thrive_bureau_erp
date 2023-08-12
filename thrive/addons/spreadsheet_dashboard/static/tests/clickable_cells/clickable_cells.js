/** @thrive-module */

import spreadsheet from "@spreadsheet/o_spreadsheet/o_spreadsheet_extended";
import { getFixture } from "@web/../tests/helpers/utils";
import { getDashboardServerData } from "../utils/data";
import { createSpreadsheetDashboard } from "../utils/dashboard_action";
import { getBasicData } from "@spreadsheet/../tests/utils/data";

const { Model } = spreadsheet;
const { functionRegistry } = spreadsheet.registries;
const { args } = spreadsheet.helpers;

async function createDashboardWithModel(model) {
    const serverData = getDashboardServerData();
    const json = JSON.stringify(model.exportData());
    const dashboard = serverData.models["spreadsheet.dashboard"].records[0];
    dashboard.raw = json;
    dashboard.json_data = json;
    serverData.models = {
        ...serverData.models,
        ...getBasicData(),
    };
    await createSpreadsheetDashboard({ serverData, spreadsheetId: dashboard.id });
    return getFixture();
}

QUnit.module("spreadsheet_dashboard > clickable cells");

QUnit.test("A link in a dashboard should be clickable", async (assert) => {
    const data = {
        sheets: [
            {
                cells: { A1: { content: "[Thrive](https://ThriveERP.com)" } },
            },
        ],
    };
    const model = new Model(data, { mode: "dashboard" });
    const target = await createDashboardWithModel(model);
    assert.containsOnce(target, ".o-dashboard-clickable-cell");
});

QUnit.test("Invalid pivot/list formulas should not be clickable", async (assert) => {
    const data = {
        sheets: [
            {
                cells: {
                    A1: { content: `=THRIVE.PIVOT("1", "measure")` },
                    A2: { content: `=THRIVE.LIST("1", 1, "name")` },
                },
            },
        ],
    };
    const model = new Model(data, { mode: "dashboard" });
    const target = await createDashboardWithModel(model);
    assert.containsNone(target, ".o-dashboard-clickable-cell");
});

QUnit.test("pivot/list formulas should be clickable", async (assert) => {
    const list = functionRegistry.get("THRIVE.LIST");
    const pivot = functionRegistry.get("THRIVE.PIVOT");

    const mock = {
        description: "Mock function to avoid setup all data sources process",
        compute: () => 1,
        args: args(``),
        returns: ["NUMBER"],
    };

    functionRegistry.add("THRIVE.LIST", mock);
    functionRegistry.add("THRIVE.PIVOT", mock);

    const data = {
        sheets: [
            {
                cells: {
                    A1: { content: `=THRIVE.PIVOT()` },
                    A2: { content: `=THRIVE.LIST()` },
                },
            },
        ],
    };

    const model = new Model(data);
    const target = await createDashboardWithModel(model);
    assert.containsN(target, ".o-dashboard-clickable-cell", 2);

    functionRegistry.add("THRIVE.LIST", list);
    functionRegistry.add("THRIVE.PIVOT", pivot);
});
