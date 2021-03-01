import unittest
from pyrler.core import pyrler

class TestUserMethods(unittest.TestCase):
    def test_user_posts(self):
        profile = pyrler.Profile()
        profile_response = profile.get_user_profile(username="SeanHannity")
        user_id = profile_response.json().get("id")
        p = pyrler.Post()
        out = p.get_user_posts(post_id=user_id, follow=True, endkey="2021-02-20T14:53:30.429Z_322497")
        all_posts = sum([k.json()["posts"] for k in out], [])
        print(f"Found {len(all_posts)} posts from Sean Hannity")
        self.assertGreater(len(all_posts), 10)

if __name__ == "__main__":
    unittest.main()