/** @thrive-module **/

import spreadsheet from "../o_spreadsheet/o_spreadsheet_extended";

const { parse } = spreadsheet;

/**
 * @typedef {Object} ThriveFunctionDescription
 * @property {string} functionName Name of the function
 * @property {Array<string>} args Arguments of the function
 * @property {boolean} isMatched True if the function is matched by the matcher function
 */

/**
 * This function is used to search for the functions which match the given matcher
 * from the given formula
 *
 * @param {string} formula
 * @param {string[]} functionNames e.g. ["THRIVE.LIST", "THRIVE.LIST.HEADER"]
 * @private
 * @returns {Array<ThriveFunctionDescription>}
 */
export function getThriveFunctions(formula, functionNames) {
    const formulaUpperCased = formula.toUpperCase();
    // Parsing is an expensive operation, so we first check if the
    // formula contains one of the function names
    if (!functionNames.some((fn) => formulaUpperCased.includes(fn.toUpperCase()))) {
        return [];
    }
    let ast;
    try {
        ast = parse(formula);
    } catch (_) {
        return [];
    }
    return _getThriveFunctionsFromAST(ast, functionNames);
}

/**
 * This function is used to search for the functions which match the given matcher
 * from the given AST
 *
 * @param {Object} ast (see o-spreadsheet)
 * @param {string[]} functionNames e.g. ["THRIVE.LIST", "THRIVE.LIST.HEADER"]
 *
 * @private
 * @returns {Array<ThriveFunctionDescription>}
 */
function _getThriveFunctionsFromAST(ast, functionNames) {
    switch (ast.type) {
        case "UNARY_OPERATION":
            return _getThriveFunctionsFromAST(ast.operand, functionNames);
        case "BIN_OPERATION": {
            return _getThriveFunctionsFromAST(ast.left, functionNames).concat(
                _getThriveFunctionsFromAST(ast.right, functionNames)
            );
        }
        case "FUNCALL": {
            const functionName = ast.value.toUpperCase();

            if (functionNames.includes(functionName)) {
                return [{ functionName, args: ast.args, isMatched: true }];
            } else {
                return ast.args.map((arg) => _getThriveFunctionsFromAST(arg, functionNames)).flat();
            }
        }
        default:
            return [];
    }
}
