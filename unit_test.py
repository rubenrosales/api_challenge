import unittest
from app import json_api
def fun(x):
    return x + 1

class MyTest(unittest.TestCase):
    def test_replace_usernames(self):
        assertUsername =  "hello <a href=\"https://twitter.com/user1\">@user1</a> and <a href=\"https://twitter.com/user2\">@user2</a>"
        usernameList = ["user1","user2"]
        tweet = "hello @user1 and @user2"
        
        self.assertEqual(json_api.replace_usernames(usernameList,tweet),assertUsername)

    def test_replace_hashtags(self):
        assertHashtag =  "Test <a href=\"https://twitter.com/hashtag/hashtag1\">#hashtag1</a> and <a href=\"https://twitter.com/hashtag/hashtag2\">#hashtag2</a>"
        hashtagList = ["hashtag1","hashtag2"]
        tweet = "Test #hashtag1 and #hashtag2"
        
        self.assertEqual(json_api.replace_hashtags(hashtagList, tweet), assertHashtag)
    
    def test_replace_media(self):
        assertMedia = 'Test <a href="twitter.com">t.co</a>'
        url = 'tweet.com'
        media = {}
        media[url] = ('t.co','twitter.com')
       
        tweet = "Test tweet.com"
        self.assertEqual(json_api.replace_media(media,tweet),assertMedia)
    
    def test_verify_user_null(self):
        fakeuser = "aac43plk"
        self.assertDictEqual(json_api.verify_user(fakeuser,1,None),{})
if __name__ == '__main__':
    unittest.main()