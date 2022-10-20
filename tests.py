from unittest import TestCase

# means running this code in app.py ("***app.running")
from app import app, db
from models import DEFAULT_IMAGE_URL, User, connect_db

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"


# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

connect_db(app)
db.create_all()
# breakpoint()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test_first",
            last_name="test_last",
            img_url=None,
        )

        second_user = User(
            first_name="test_first_two",
            last_name="test_last_two",
            img_url=None,
        )

        db.session.add_all([test_user, second_user])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        """ Check if route renders correct landing page """

        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_new_user_page(self):
        """ Check route renders correct new user form """

        with self.client as c:
            resp = c.get("users/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("COMMENT FOR TESTING PURPOSES", html)

    def test_add_new_user(self):
        """ Create a new user and check if redirects and
            users database contains correct information
        """

        with self.client as c:
            test_user = {"first_name": 'testing first_name',
                         "last_name": 'testing last_name',
                         "img_url": DEFAULT_IMAGE_URL
                         }

            resp = c.post("users/new", data=test_user, follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)

            self.assertIn("testing first_name", html)

            # self.assertTrue(User.query.filter_by(
            #     first_name='testing first_name').one_or_none())

    def test_edit_user(self):
        """ Edit user information and check if users database is
            updated and route redirects
        """

        with self.client as c:
            test_user = {"first_name": 'edit first_name',
                         "last_name": 'edit last_name',
                         "img_url": DEFAULT_IMAGE_URL
                         }

            user_id = User.query.first().id
            resp = c.post(f"users/{user_id}/edit", data=test_user, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn("edit first_name", html)

            # TODO: use for testing database query
            # user_id = User.query.first().id
            # self.assertEqual(resp.status_code, 302)
            # self.assertTrue(User.query.get(
            #     user_id).first_name == 'edit first_name')
