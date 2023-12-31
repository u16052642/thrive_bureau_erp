import base64

from thrive.tests.common import HttpCase


class LoadMenusTests(HttpCase):

    def setUp(self):
        super().setUp()
        self.menu = self.env["ir.ui.menu"].create({
            "name": "test_menu",
            "parent_id": False,
        })

        def search(*args, **kwargs):
            return self.menu

        self.patch(type(self.env["ir.ui.menu"]), "search", search)
        self.authenticate("admin", "admin")

    def test_web_icon(self):
        self.menu.web_icon = False
        self.menu.web_icon_data = base64.b64encode(b"encode")

        menu_loaded = self.url_open("/web/webclient/load_menus/1234")

        expected = {
            str(self.menu.id): {
                "actionID": False,
                "actionModel": False,
                "appID": self.menu.id,
                "children": [],
                "id": self.menu.id,
                "name": "test_menu",
                "webIcon": False,
                "webIconData": "data:image/png;base64,ZW5jb2Rl",
                "xmlid": ""
            },
            "root": {
                "actionID": False,
                "actionModel": False,
                "appID": False,
                "children": [
                    self.menu.id
                ],
                "id": "root",
                "name": "root",
                "webIcon": None,
                "webIconData": None,
                "xmlid": "",
                'backgroundImage': None,
            }
        }

        self.assertDictEqual(menu_loaded.json(), expected)
