# tests/test_app.py

import os
import unittest

os.environ["TESTING"] = "true"

from app import app, TimelinePost  # noqa: E402


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        # Start every test with an empty timeline table.
        TimelinePost.delete().execute()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>MLH Fellow</title>" in html
        # Home page content specific to this portfolio.
        assert "Saahith Veeramaneni" in html
        assert "About Me" in html
        assert "Work Experience" in html
        assert "Education" in html
        assert "Places I've Visited" in html

    def test_timeline(self):
        # The timeline should start empty.
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        # POST a valid timeline post and check the response.
        post_response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "content": "Hello world, I'm John!",
            },
        )
        assert post_response.status_code == 200
        assert post_response.is_json
        created = post_response.get_json()
        assert created["name"] == "John Doe"
        assert created["email"] == "john@example.com"
        assert created["content"] == "Hello world, I'm John!"
        assert "id" in created

        # The GET API should now return the post we just created.
        response = self.client.get("/api/timeline_post")
        json = response.get_json()
        assert len(json["timeline_posts"]) == 1
        assert json["timeline_posts"][0]["name"] == "John Doe"
        assert json["timeline_posts"][0]["email"] == "john@example.com"
        assert json["timeline_posts"][0]["content"] == "Hello world, I'm John!"

        # The timeline page should render the form and posts.
        page_response = self.client.get("/timeline")
        assert page_response.status_code == 200
        page_html = page_response.get_data(as_text=True)
        assert "<title>Timeline</title>" in page_html
        assert 'id="timeline-form"' in page_html
        # The post we created should be rendered on the page (name has no
        # characters that Jinja would HTML-escape, unlike the content).
        assert "John Doe" in page_html

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post(
            "/api/timeline_post",
            data={"email": "john@example.com", "content": "Hello world, I'm John!"},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post(
            "/api/timeline_post",
            data={"name": "John Doe", "email": "john@example.com", "content": ""},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email (no "@")
        response = self.client.post(
            "/api/timeline_post",
            data={"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html

        # POST request with multiple "@" characters
        response = self.client.post(
            "/api/timeline_post",
            data={"name": "John Doe", "email": "john@@example.com", "content": "Hello!"},
        )
        assert response.status_code == 400
        assert "Invalid email" in response.get_data(as_text=True)

        # POST request with an empty local part
        response = self.client.post(
            "/api/timeline_post",
            data={"name": "John Doe", "email": "@example.com", "content": "Hello!"},
        )
        assert response.status_code == 400
        assert "Invalid email" in response.get_data(as_text=True)

        # POST request with an empty domain label (trailing dot)
        response = self.client.post(
            "/api/timeline_post",
            data={"name": "John Doe", "email": "john@example.", "content": "Hello!"},
        )
        assert response.status_code == 400
        assert "Invalid email" in response.get_data(as_text=True)


if __name__ == "__main__":
    unittest.main()
