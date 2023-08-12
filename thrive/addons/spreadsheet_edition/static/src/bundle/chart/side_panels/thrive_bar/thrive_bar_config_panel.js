/** @thrive-module */

import { IrMenuSelector } from "@spreadsheet_edition/assets/components/ir_menu_selector/ir_menu_selector";
import { CommonThriveChartConfigPanel } from "../common/config_panel";

export class ThriveBarChartConfigPanel extends CommonThriveChartConfigPanel {
    onUpdateStacked(ev) {
        this.props.updateChart({
            stacked: ev.target.checked,
        });
    }
}

ThriveBarChartConfigPanel.template = "spreadsheet_edition.ThriveBarChartConfigPanel";
ThriveBarChartConfigPanel.components = { IrMenuSelector };
