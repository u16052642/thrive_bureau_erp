/** @thrive-module */

import { ThriveBarChart } from "@spreadsheet/chart/thrive_chart/thrive_bar_chart";
import { ThriveChart } from "@spreadsheet/chart/thrive_chart/thrive_chart";
import { ThriveLineChart } from "@spreadsheet/chart/thrive_chart/thrive_line_chart";
import { nextTick } from "@web/../tests/helpers/utils";
import { createSpreadsheetWithChart, insertChartInSpreadsheet } from "../../utils/chart";
import { createModelWithDataSource } from "../../utils/model";
import spreadsheet from "@spreadsheet/o_spreadsheet/o_spreadsheet_extended";

const { toZone } = spreadsheet.helpers;

QUnit.module("spreadsheet > thrive chart plugin", {}, () => {
    QUnit.test("Can add an Thrive Bar chart", async (assert) => {
        const { model } = await createSpreadsheetWithChart({ type: "thrive_bar" });
        const sheetId = model.getters.getActiveSheetId();
        assert.strictEqual(model.getters.getChartIds(sheetId).length, 1);
        const chartId = model.getters.getChartIds(sheetId)[0];
        const chart = model.getters.getChart(chartId);
        assert.ok(chart instanceof ThriveBarChart);
        assert.strictEqual(chart.getDefinitionForExcel(), undefined);
        assert.strictEqual(model.getters.getChartRuntime(chartId).chartJsConfig.type, "bar");
    });

    QUnit.test("Can add an Thrive Line chart", async (assert) => {
        const { model } = await createSpreadsheetWithChart({ type: "thrive_line" });
        const sheetId = model.getters.getActiveSheetId();
        assert.strictEqual(model.getters.getChartIds(sheetId).length, 1);
        const chartId = model.getters.getChartIds(sheetId)[0];
        const chart = model.getters.getChart(chartId);
        assert.ok(chart instanceof ThriveLineChart);
        assert.strictEqual(chart.getDefinitionForExcel(), undefined);
        assert.strictEqual(model.getters.getChartRuntime(chartId).chartJsConfig.type, "line");
    });

    QUnit.test("Can add an Thrive Pie chart", async (assert) => {
        const { model } = await createSpreadsheetWithChart({ type: "thrive_pie" });
        const sheetId = model.getters.getActiveSheetId();
        assert.strictEqual(model.getters.getChartIds(sheetId).length, 1);
        const chartId = model.getters.getChartIds(sheetId)[0];
        const chart = model.getters.getChart(chartId);
        assert.ok(chart instanceof ThriveChart);
        assert.strictEqual(chart.getDefinitionForExcel(), undefined);
        assert.strictEqual(model.getters.getChartRuntime(chartId).chartJsConfig.type, "pie");
    });

    QUnit.test("A data source is added after a chart creation", async (assert) => {
        const { model } = await createSpreadsheetWithChart();
        const sheetId = model.getters.getActiveSheetId();
        const chartId = model.getters.getChartIds(sheetId)[0];
        assert.ok(model.getters.getChartDataSource(chartId));
    });

    QUnit.test("Thrive bar chart runtime loads the data", async (assert) => {
        const { model } = await createSpreadsheetWithChart({
            type: "thrive_bar",
            mockRPC: async function (route, args) {
                if (args.method === "web_read_group") {
                    assert.step("web_read_group");
                }
            },
        });
        const sheetId = model.getters.getActiveSheetId();
        const chartId = model.getters.getChartIds(sheetId)[0];
        assert.verifySteps([], "it should not be loaded eagerly");
        assert.deepEqual(model.getters.getChartRuntime(chartId).chartJsConfig.data, {
            datasets: [],
            labels: [],
        });
        await nextTick();
        assert.deepEqual(model.getters.getChartRuntime(chartId).chartJsConfig.data, {
            datasets: [
                {
                    backgroundColor: "rgb(31,119,180)",
                    borderColor: "rgb(31,119,180)",
                    data: [1, 3],
                    label: "Count",
                },
            ],
            labels: ["false", "true"],
        });
        assert.verifySteps(["web_read_group"], "it should have loaded the data");
    });

    QUnit.test("Thrive pie chart runtime loads the data", async (assert) => {
        const { model } = await createSpreadsheetWithChart({
            type: "thrive_pie",
            mockRPC: async function (route, args) {
                if (args.method === "web_read_group") {
                    assert.step("web_read_group");
                }
            },
        });
        const sheetId = model.getters.getActiveSheetId();
        const chartId = model.getters.getChartIds(sheetId)[0];
        assert.verifySteps([], "it should not be loaded eagerly");
        assert.deepEqual(model.getters.getChartRuntime(chartId).chartJsConfig.data, {
            datasets: [],
            labels: [],
        });
        await nextTick();
        assert.deepEqual(model.getters.getChartRuntime(chartId).chartJsConfig.data, {
            datasets: [
                {
                    backgroundColor: ["rgb(31,119,180)", "rgb(255,127,14)", "rgb(174,199,232)"],
                    borderColor: "#FFFFFF",
                    data: [1, 3],
                    label: "",
                },
            ],
            labels: ["false", "true"],
        });
        assert.verifySteps(["web_read_group"], "it should have loaded the data");
    });

    QUnit.test("Thrive line chart runtime loads the data", async (assert) => {
        const { model } = await createSpreadsheetWithChart({
            type: "thrive_line",
            mockRPC: async function (route, args) {
                if (args.method === "web_read_group") {
                    assert.step("web_read_group");
                }
            },
        });
        const sheetId = model.getters.getActiveSheetId();
        const chartId = model.getters.getChartIds(sheetId)[0];
        assert.verifySteps([], "it should not be loaded eagerly");
        assert.deepEqual(model.getters.getChartRuntime(chartId).chartJsConfig.data, {
            datasets: [],
            labels: [],
        });
        await nextTick();
        assert.deepEqual(model.getters.getChartRuntime(chartId).chartJsConfig.data, {
            datasets: [
                {
                    backgroundColor: "#1f77b466",
                    borderColor: "rgb(31,119,180)",
                    data: [1, 3],
                    label: "Count",
                    lineTension: 0,
                    fill: "origin",
                    pointBackgroundColor: "rgb(31,119,180)",
                },
            ],
            labels: ["false", "true"],
        });
        assert.verifySteps(["web_read_group"], "it should have loaded the data");
    });

    QUnit.test("Changing the chart type does not reload the data", async (assert) => {
        const { model } = await createSpreadsheetWithChart({
            type: "thrive_line",
            mockRPC: async function (route, args) {
                if (args.method === "web_read_group") {
                    assert.step("web_read_group");
                }
            },
        });
        const sheetId = model.getters.getActiveSheetId();
        const chartId = model.getters.getChartIds(sheetId)[0];
        const definition = model.getters.getChartDefinition(chartId);

        // force runtime computation
        model.getters.getChartRuntime(chartId);
        await nextTick();

        assert.verifySteps(["web_read_group"], "it should have loaded the data");
        model.dispatch("UPDATE_CHART", {
            definition: {
                ...definition,
                type: "thrive_bar",
            },
            id: chartId,
            sheetId,
        });
        await nextTick();
        // force runtime computation
        model.getters.getChartRuntime(chartId);
        assert.verifySteps([], "it should have not have loaded the data a second time");
    });

    QUnit.test("Can import/export an Thrive chart", async (assert) => {
        const model = await createModelWithDataSource();
        insertChartInSpreadsheet(model, "thrive_line");
        const data = model.exportData();
        const figures = data.sheets[0].figures;
        assert.strictEqual(figures.length, 1);
        const figure = figures[0];
        assert.strictEqual(figure.tag, "chart");
        assert.strictEqual(figure.data.type, "thrive_line");
        const m1 = await createModelWithDataSource({ spreadsheetData: data });
        const sheetId = m1.getters.getActiveSheetId();
        assert.strictEqual(m1.getters.getChartIds(sheetId).length, 1);
        const chartId = m1.getters.getChartIds(sheetId)[0];
        assert.ok(m1.getters.getChartDataSource(chartId));
        assert.strictEqual(m1.getters.getChartRuntime(chartId).chartJsConfig.type, "line");
    });

    QUnit.test("Can undo/redo an Thrive chart creation", async (assert) => {
        const model = await createModelWithDataSource();
        insertChartInSpreadsheet(model, "thrive_line");
        const sheetId = model.getters.getActiveSheetId();
        const chartId = model.getters.getChartIds(sheetId)[0];
        assert.ok(model.getters.getChartDataSource(chartId));
        model.dispatch("REQUEST_UNDO");
        assert.strictEqual(model.getters.getChartIds(sheetId).length, 0);
        model.dispatch("REQUEST_REDO");
        assert.ok(model.getters.getChartDataSource(chartId));
        assert.strictEqual(model.getters.getChartIds(sheetId).length, 1);
    });

    QUnit.test("charts with no legend", async (assert) => {
        const { model } = await createSpreadsheetWithChart({ type: "thrive_pie" });
        insertChartInSpreadsheet(model, "thrive_bar");
        insertChartInSpreadsheet(model, "thrive_line");
        const sheetId = model.getters.getActiveSheetId();
        const [pieChartId, barChartId, lineChartId] = model.getters.getChartIds(sheetId);
        const pie = model.getters.getChartDefinition(pieChartId);
        const bar = model.getters.getChartDefinition(barChartId);
        const line = model.getters.getChartDefinition(lineChartId);
        assert.strictEqual(
            model.getters.getChartRuntime(pieChartId).chartJsConfig.options.legend.display,
            true
        );
        assert.strictEqual(
            model.getters.getChartRuntime(barChartId).chartJsConfig.options.legend.display,
            true
        );
        assert.strictEqual(
            model.getters.getChartRuntime(lineChartId).chartJsConfig.options.legend.display,
            true
        );
        model.dispatch("UPDATE_CHART", {
            definition: {
                ...pie,
                legendPosition: "none",
            },
            id: pieChartId,
            sheetId,
        });
        model.dispatch("UPDATE_CHART", {
            definition: {
                ...bar,
                legendPosition: "none",
            },
            id: barChartId,
            sheetId,
        });
        model.dispatch("UPDATE_CHART", {
            definition: {
                ...line,
                legendPosition: "none",
            },
            id: lineChartId,
            sheetId,
        });
        assert.strictEqual(
            model.getters.getChartRuntime(pieChartId).chartJsConfig.options.legend.display,
            false
        );
        assert.strictEqual(
            model.getters.getChartRuntime(barChartId).chartJsConfig.options.legend.display,
            false
        );
        assert.strictEqual(
            model.getters.getChartRuntime(lineChartId).chartJsConfig.options.legend.display,
            false
        );
    });

    QUnit.test("Bar chart with stacked attribute is supported", async (assert) => {
        const { model } = await createSpreadsheetWithChart({ type: "thrive_bar" });
        const sheetId = model.getters.getActiveSheetId();
        const chartId = model.getters.getChartIds(sheetId)[0];
        const definition = model.getters.getChartDefinition(chartId);
        model.dispatch("UPDATE_CHART", {
            definition: {
                ...definition,
                stacked: true,
            },
            id: chartId,
            sheetId,
        });
        assert.ok(
            model.getters.getChartRuntime(chartId).chartJsConfig.options.scales.xAxes[0].stacked
        );
        assert.ok(
            model.getters.getChartRuntime(chartId).chartJsConfig.options.scales.yAxes[0].stacked
        );
        model.dispatch("UPDATE_CHART", {
            definition: {
                ...definition,
                stacked: false,
            },
            id: chartId,
            sheetId,
        });
        assert.notOk(
            model.getters.getChartRuntime(chartId).chartJsConfig.options.scales.xAxes[0].stacked
        );
        assert.notOk(
            model.getters.getChartRuntime(chartId).chartJsConfig.options.scales.yAxes[0].stacked
        );
    });

    QUnit.test("Can copy/paste Thrive chart", async (assert) => {
        const { model } = await createSpreadsheetWithChart({ type: "thrive_pie" });
        const sheetId = model.getters.getActiveSheetId();
        const chartId = model.getters.getChartIds(sheetId)[0];
        model.dispatch("SELECT_FIGURE", { id: chartId });
        model.dispatch("COPY");
        model.dispatch("PASTE", { target: [toZone("A1")] });
        const chartIds = model.getters.getChartIds(sheetId);
        assert.strictEqual(chartIds.length, 2);
        assert.ok(model.getters.getChart(chartIds[1]) instanceof ThriveChart);
        assert.strictEqual(
            JSON.stringify(model.getters.getChartRuntime(chartIds[1])),
            JSON.stringify(model.getters.getChartRuntime(chartId))
        );

        assert.notEqual(
            model.getters.getChart(chartId).dataSource,
            model.getters.getChart(chartIds[1]).dataSource,
            "The datasource is also duplicated"
        );
    });

    QUnit.test("Can cut/paste Thrive chart", async (assert) => {
        const { model } = await createSpreadsheetWithChart({ type: "thrive_pie" });
        const sheetId = model.getters.getActiveSheetId();
        const chartId = model.getters.getChartIds(sheetId)[0];
        const chartRuntime = model.getters.getChartRuntime(chartId);
        model.dispatch("SELECT_FIGURE", { id: chartId });
        model.dispatch("CUT");
        model.dispatch("PASTE", { target: [toZone("A1")] });
        const chartIds = model.getters.getChartIds(sheetId);
        assert.strictEqual(chartIds.length, 1);
        assert.notEqual(chartIds[0], chartId);
        assert.ok(model.getters.getChart(chartIds[0]) instanceof ThriveChart);
        assert.strictEqual(
            JSON.stringify(model.getters.getChartRuntime(chartIds[0])),
            JSON.stringify(chartRuntime)
        );
    });

    QUnit.test("Duplicating a sheet correctly duplicates Thrive chart", async (assert) => {
        const { model } = await createSpreadsheetWithChart({ type: "thrive_bar" });
        const sheetId = model.getters.getActiveSheetId();
        const secondSheetId = "secondSheetId";
        const chartId = model.getters.getChartIds(sheetId)[0];
        model.dispatch("DUPLICATE_SHEET", { sheetId, sheetIdTo: secondSheetId });
        const chartIds = model.getters.getChartIds(secondSheetId);
        assert.strictEqual(chartIds.length, 1);
        assert.ok(model.getters.getChart(chartIds[0]) instanceof ThriveChart);
        assert.strictEqual(
            JSON.stringify(model.getters.getChartRuntime(chartIds[0])),
            JSON.stringify(model.getters.getChartRuntime(chartId))
        );

        assert.notEqual(
            model.getters.getChart(chartId).dataSource,
            model.getters.getChart(chartIds[0]).dataSource,
            "The datasource is also duplicated"
        );
    });

    QUnit.test("Line chart with stacked attribute is supported", async (assert) => {
        const { model } = await createSpreadsheetWithChart({ type: "thrive_line" });
        const sheetId = model.getters.getActiveSheetId();
        const chartId = model.getters.getChartIds(sheetId)[0];
        const definition = model.getters.getChartDefinition(chartId);
        model.dispatch("UPDATE_CHART", {
            definition: {
                ...definition,
                stacked: true,
            },
            id: chartId,
            sheetId,
        });
        assert.notOk(
            model.getters.getChartRuntime(chartId).chartJsConfig.options.scales.xAxes[0].stacked
        );
        assert.ok(
            model.getters.getChartRuntime(chartId).chartJsConfig.options.scales.yAxes[0].stacked
        );
        model.dispatch("UPDATE_CHART", {
            definition: {
                ...definition,
                stacked: false,
            },
            id: chartId,
            sheetId,
        });
        assert.notOk(
            model.getters.getChartRuntime(chartId).chartJsConfig.options.scales.xAxes[0].stacked
        );
        assert.notOk(
            model.getters.getChartRuntime(chartId).chartJsConfig.options.scales.yAxes[0].stacked
        );
    });
});
