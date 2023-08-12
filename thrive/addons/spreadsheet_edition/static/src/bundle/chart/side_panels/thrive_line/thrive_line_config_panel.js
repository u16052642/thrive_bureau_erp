/** @thrive-module */

import { IrMenuSelector } from "@spreadsheet_edition/assets/components/ir_menu_selector/ir_menu_selector";
import { CommonThriveChartConfigPanel } from "../common/config_panel";

export class ThriveLineChartConfigPanel extends CommonThriveChartConfigPanel {
    onUpdateStacked(ev) {
        this.props.updateChart({
            stacked: ev.target.checked,
        });
    }
}

ThriveLineChartConfigPanel.template = "spreadsheet_edition.ThriveLineChartConfigPanel";
ThriveLineChartConfigPanel.components = { IrMenuSelector };
