# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

import thrive.tests


@thrive.tests.tagged('post_install', '-at_install')
class TestUi(thrive.tests.HttpCase):
    def test_admin(self):
        # Ensure at least two blogs exist for the step asking to select a blog
        self.env['blog.blog'].create({'name': 'Travel'})

        # Ensure at least one image exists for the step that chooses one
        self.env['ir.attachment'].create({
            'public': True,
            'type': 'url',
            'url': '/web/image/123/transparent.png',
            'name': 'transparent.png',
            'mimetype': 'image/png',
        })

        self.start_tour(self.env['website'].get_client_action_url('/'), 'blog', login='admin')

    def test_blog_post_tags(self):
        self.start_tour(self.env['website'].get_client_action_url('/blog'), 'blog_tags', login='admin')
