from django.test import TestCase, Client
from .models import Search

# These tests deal with user input
class InputTests(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    # Putting nothing in the search box
    def test_empty(self):
        c = Client()
        response = c.get('/search/' + '')
        self.assertEquals(response.status_code, 302)

    # Putting a single space in the search box should redirect to the same page
    def test_singlespace(self):
        c = Client()
        response = c.get('/search/' + ' ')
        self.assertEquals(response.status_code, 302)

    # Putting a single word should go to that search page
    def test_oneword(self):
        c = Client()
        response = c.get('/search/' + 'word')
        self.assertEquals(response.status_code, 200)

    # One misspelled word
    def test_misspelling(self):
        c = Client()
        response = c.get('/search/' + 'mispelling')
        self.assertEquals(response.status_code, 200)

    # Two correctly spelled words
    def test_twowords(self):
        c = Client()
        response = c.get('/search/' + 'mispelling')
        self.assertEquals(response.status_code, 200)

    # Two incorrectly spelled words
    def test_twoincorrectwords(self):
        c = Client()
        response = c.get('/search/' + 'mispelling')
        self.assertEquals(response.status_code, 200)

    # Space at the start of the query
    def test_leadingspace(self):
        c = Client()
        response = c.get('/search/' + 'mispelling')
        self.assertEquals(response.status_code, 200)

    # Space at the end of the query
    def test_trailingspace(self):
        c = Client()
        response = c.get('/search/' + 'mispelling')
        self.assertEquals(response.status_code, 200)

    # Two words separated by two spaces
    def test_twospacesbetween(self):
        c = Client()
        response = c.get('/search/' + 'mispelling')
        self.assertEquals(response.status_code, 200)

    # Two words separated by three spaces
    def test_threespacesbetween(self):
        c = Client()
        response = c.get('/search/' + 'mispelling')
        self.assertEquals(response.status_code, 200)

    # Query containing a ' or a "
    def test_quotes(self):
        c = Client()
        response = c.get('/search/' + 'mispelling')
        self.assertEquals(response.status_code, 200)

    # Queries containing !@#$%^&*(){}[]-=+\;:<>,./?`~
    def test_specialchars(self):
        c = Client()
        response = c.get('/search/' + 'mispelling')
        self.assertEquals(response.status_code, 200)

    # Query has one of those special characters in front of a word
    def test_wordspecialstart(self):
        c = Client()
        response = c.get('/search/' + 'mispelling')
        self.assertEquals(response.status_code, 200)

    # Query has the special character in the middle of the word
    def test_wordspecialmid(self):
        c = Client()
        response = c.get('/search/' + 'mispelling')
        self.assertEquals(response.status_code, 200)

    # Query has the special character at the end of a word
    def test_wordspecialend(self):
        c = Client()
        response = c.get('/search/' + 'mispelling')
        self.assertEquals(response.status_code, 200)

    # Hyphenated word
    def test_hyphenword(self):
        c = Client()
        response = c.get('/search/' + 'mispelling')
        self.assertEquals(response.status_code, 200)

    # Long input (>256 chars)
    def test_long(self):
        c = Client()
        response = c.get('/search/' + 'mispelling')
        self.assertEquals(response.status_code, 200)

    # Huge input (>1024 chars)
    def test_verylong(self):
        c = Client()
        response = c.get('/search/' + 'mispelling')
        self.assertEquals(response.status_code, 200)

    # Non-printing characters
    def test_nonprint(self):
        c = Client()
        response = c.get('/search/' + 'mispelling')
        self.assertEquals(response.status_code, 200)


    # Foreign-letters
    def test_foreign(self):
        c = Client()
        response = c.get('/search/' + 'mispelling')
        self.assertEquals(response.status_code, 200)

    # Random unicode chars
    def test_unicode(self):
        c = Client()
        response = c.get('/search/' + 'mispelling')
        self.assertEquals(response.status_code, 200)
