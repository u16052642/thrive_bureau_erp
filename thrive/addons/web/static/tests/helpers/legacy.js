thrive.define("web.SessionOverrideForTests", (require) => {
    // Override the Session.session_reload function
    // The wowl test infrastructure does set a correct thrive global value before each test
    // while the session is built only once for all tests.
    // So if a test does a session_reload, it will merge the thrive global of that test
    // into the session, and will alter every subsequent test of the suite.
    // Obviously, we don't want that, ever.
    const { session: sessionInfo } = require("@web/session");
    const initialSessionInfo = Object.assign({}, sessionInfo);
    const Session = require("web.Session");
    const { patch } = require("@web/core/utils/patch");
    patch(Session.prototype, "web.SessionTestPatch", {
        async session_reload() {
            for (const key in sessionInfo) {
                delete sessionInfo[key];
            }
            for (const key in initialSessionInfo) {
                sessionInfo[key] = initialSessionInfo[key];
            }
            return await this._super(...arguments);
        },
    });
});

thrive.define("web.test_legacy", async (require) => {
    require("web.SessionOverrideForTests");
    require("web.test_utils");
    const session = require("web.session");
    await session.is_bound; // await for templates from server

    const FormView = require("web.FormView");
    const ListView = require("web.ListView");
    const viewRegistry = require("web.view_registry");
    viewRegistry.add("legacy_form", FormView).add("legacy_list", ListView);

    return { legacyProm: session.is_bound };
});
