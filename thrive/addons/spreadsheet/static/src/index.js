/** @thrive-module */

/**
 * This file is meant to load the different subparts of the module
 * to guarantee their plugins are loaded in the right order
 *
 * dependency:
 *             other plugins
 *                   |
 *                  ...
 *                   |
 *                filters
 *                /\    \
 *               /  \    \
 *           pivot  list  Thrive chart
 */

/** TODO: Introduce a position parameter to the plugin registry in order to load them in a specific order */
import spreadsheet from "@spreadsheet/o_spreadsheet/o_spreadsheet_extended";
const { corePluginRegistry, uiPluginRegistry } = spreadsheet.registries;

import { GlobalFiltersCorePlugin, GlobalFiltersUIPlugin } from "@spreadsheet/global_filters/index";
import { PivotCorePlugin, PivotUIPlugin } from "@spreadsheet/pivot/index"; // list depends on filter for its getters
import { ListCorePlugin, ListUIPlugin } from "@spreadsheet/list/index"; // pivot depends on filter for its getters
import {
    ChartThriveMenuPlugin,
    ThriveChartCorePlugin,
    ThriveChartUIPlugin,
} from "@spreadsheet/chart/index"; // Thrivechart depends on filter for its getters

corePluginRegistry.add("ThriveGlobalFiltersCorePlugin", GlobalFiltersCorePlugin);
corePluginRegistry.add("ThrivePivotCorePlugin", PivotCorePlugin);
corePluginRegistry.add("ThriveListCorePlugin", ListCorePlugin);
corePluginRegistry.add("thriveChartCorePlugin", ThriveChartCorePlugin);
corePluginRegistry.add("chartThriveMenuPlugin", ChartThriveMenuPlugin);

uiPluginRegistry.add("ThriveGlobalFiltersUIPlugin", GlobalFiltersUIPlugin);
uiPluginRegistry.add("ThrivePivotUIPlugin", PivotUIPlugin);
uiPluginRegistry.add("ThriveListUIPlugin", ListUIPlugin);
uiPluginRegistry.add("thriveChartUIPlugin", ThriveChartUIPlugin);
