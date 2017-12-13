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

    # Putting whitespace should redirect to the same page
    def test_singlespace(self):
        c = Client()
        response = c.get('/search/' + '        ')
        self.assertEquals(response.status_code, 302)

    # Putting a single word should go to that search page
    def test_oneword(self):
        c = Client()
        response = c.get('/search/' + 'word')
        self.assertEquals(response.status_code, 200)

    # One misspelled word should search for the mispelling, but also suggest a fix
    def test_misspelling(self):
        c = Client()
        response = c.get('/search/' + 'mispelling')
        self.assertEquals(response.status_code, 200)

    # Two correctly spelled words should search the correct pair and bigram
    def test_twowords(self):
        c = Client()
        response = c.get('/search/' + 'two words')
        self.assertEquals(response.status_code, 200)

    # Two incorrectly spelled words should search the misspellings, then suggest fixes
    def test_twoincorrectwords(self):
        c = Client()
        response = c.get('/search/' + 'mispelled twcie')
        self.assertEquals(response.status_code, 200)

    # Space at the start of the query should ignore extra whitespace and parse word normally
    def test_leadingspace(self):
        c = Client()
        response = c.get('/search/' + ' space')
        self.assertEquals(response.status_code, 200)

    # Space at the end of the query should ignore extra whitespace and parse word normally
    def test_trailingspace(self):
        c = Client()
        response = c.get('/search/' + 'space ')
        self.assertEquals(response.status_code, 200)

    # Two words separated by two spaces should ignore extra whitespace and only view word
    def test_twospacesbetween(self):
        c = Client()
        response = c.get('/search/' + 'two  words')
        self.assertEquals(response.status_code, 200)

    # Query containing a ' or a " should strip the " but keep ' in word for contractions
    def test_quotes(self):
        c = Client()
        response = c.get('/search/' + 'don\'t panic"')
        self.assertEquals(response.status_code, 200)

    # Queries containing !@#$%^&*(){}[]-=+\;:<>,./?`~ should not go to results page
    def test_specialchars(self):
        c = Client()
        response = c.get('/search/' + '!@#$%^&*(){}[]-=+\;:<>,./?`~')
        self.assertEquals(response.status_code, 302)

    # Query has one of those special characters in front of a word should search as is, but suggest version without the special character
    def test_wordspecialstart(self):
        c = Client()
        response = c.get('/search/' + '$word')
        self.assertEquals(response.status_code, 200)

    # Query has the special character in the middle of the word should search as is, but suggest the version without the special character
    def test_wordspecialmid(self):
        c = Client()
        response = c.get('/search/' + 'wor$d')
        self.assertEquals(response.status_code, 200)

    # Query has the special character at the end of a word (same as above two)
    def test_wordspecialend(self):
        c = Client()
        response = c.get('/search/' + 'word$')
        self.assertEquals(response.status_code, 200)

    # Hyphenated word should consider the hyphenated piece as a single token
    def test_hyphenword(self):
        c = Client()
        response = c.get('/search/' + 'the-word')
        self.assertEquals(response.status_code, 200)

    # Long input (>256 chars) should work as normal
    def test_long(self):
        c = Client()
        response = c.get('/search/' + 'jbtebcupgsshrahadqbn oonilkbifubyqrsltokt hogufsosskekawtolvko lrwmfbdsnpasnltejitw odttytmwyrouuykaghbt mbigvwqgwufmjrmrmgvl urddzqliptufcrzzzeaw omgtkunromhkckgndudg dozgluozulctxqwmsqos albfezkveforstpfwlbp mvintizcenetqsxnqzou jiqeqschxfyggcnbiupi plgxcjmlomtudyjpikxu ') 
        self.assertEquals(response.status_code, 200)

    # Huge input (>1024 chars) should truncate to 1024 and work as normal
    def test_verylong(self):
        c = Client()
        response = c.get('/search/' + 'dueqxnfcwovjfqbdiuuc yscucdneldygnadgppxf inqlfiqezeurcxidfdga pjobubatfnflkwitgmuh ynufvepxpyusicyuiqdu vqmpapagedchfwozoelp xxyjdgyobdqzaxwuysvj ansbymoijehjzkiqwggd okrqfykrxcatckhxblpg xvbriqxgahxxsfbvtgty fkhsigvnuapmhtthwjmf xtbjquwzinvbdmbcpmxa niyljwcteuipxfhldpii mwacnujgfsjgaudpmnil nhvynmcutuwuckpazpcs pczbbyoauqqhvemljbrq ppvxemysnlefozjirppx yuzjiixsgntdmzfrlmdq oggwdbkncmsgkbvpirlx emviolstlmmmrdwuxgnz rozmyurxxjoucslzbdat eyzoudifcdfpniopsiby tjfddqjrhmktfwswqcvk ifvarkfsfetqdqqxnxil xyvqlqxwimucyzziedqw tknfqeivfpxeqwxgptrp ainbnfbwbkozuvzmkzjv ynopewmylnovteoclxjp gxffgccimthhozegmlwh obdnwbrdforrdrharkwi dtpyviknhrlezbjsotmc kgejwxgdxfjfirpddjdw bbrqwfceizvnhohqvwag wzhshutfpncjmnbiqjvb oaiogheyqhavjbwsytdn ehlykwcxevgmjzexoyfc iguuexmbmepunmgzuhcd mciajhgjewfswplrgsvk ecxaqxchqjpjlddtefdq fdfcampzxsrmzmipqojf rixiqxnkzwqptfphisxk msmsmspjcrmdokcjdqqo isiuhneksjdhkxndisqj sdkubpvkeelackvwsqnp cqsfgwgtgvjhewovwavz lurzdjnlyhyudpcobbkv oryggahyrekpnpfjsxzq oniyyutxcnlkugrlqedj kdornbhbdsztbknmylof luwzjpheaykxuhtuowtk quavjmtswgqqwxmsmxjl ryhpjytuiskxnxbxvhsx')
        self.assertEquals(response.status_code, 200)

    # Non-printing characters should ignore the nonprinting character and parse normally (do not treat the null term as a space, so middle is a single token)
    def test_nonprint(self):
        c = Client()
        response = c.get('/search/' + 'mid\0dle')
        self.assertEquals(response.status_code, 200)


    # Foreign-letters should work as normal, but suggest English word instead
    def test_foreign(self):
        c = Client()
        response = c.get('/search/' + 'öst façade')
        self.assertEquals(response.status_code, 200)

    # Random unicode chars
    def test_unicode(self):
        c = Client()
        response = c.get('/search/' + '🅱 ')
        self.assertEquals(response.status_code, 200)
