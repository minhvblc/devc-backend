import facebook
import requests
import datetime
import dateutil.parser
import pandas as pd
import nltk
# nltk.download('punkt')

# Columns to extract files
commentCols = ['Post ID', 'Comment ID', 'Comment', 'Label']
likeCols = ['Post ID', 'Likes']

print(datetime.datetime.now(tz=datetime.timezone.utc).isoformat())
lastCollectTime = '2020-11-19T05:36:39.205632+00:00'
isTheFirstTimeCollect = True

def getLongTermUserToken(user_access_token):
    app_id = '666275994291953'
    app_secret = 'f1f37f76cb9eb0dc554ee0d4959e679b'
    data = requests.get('https://graph.facebook.com/v8.0/oauth/access_token?grant_type=fb_exchange_token&client_id={0}&client_secret={1}&fb_exchange_token={2}'.format(app_id, app_secret, user_access_token))
    data = data.json()
    return data['access_token']

def getLongTermPageToken(longterm_user_access_token, user_id):
    data = requests.get('https://graph.facebook.com/v8.0/{0}/accounts?access_token={1}'.format(user_id, longterm_user_access_token))
    data = data.json()
    return data['access_token']
    
# Get page names and ids for user to choose from
# Return id back to initial campagne
def getPageNames(user_access_token, user_id):
    userPages = getLongTermPageToken(user_access_token, user_id)

    if len(userPages): 
        return list(map(lambda obj: {'page_name': obj['name'], 'page_id': obj['id']}, userPages))
    else: return []

def getUserPage(user_access_token, page_id, keywords):
    userGraph = facebook.GraphAPI(access_token=user_access_token)
    userPages = userGraph.get_object(id='me/accounts')['data']

    pagesFounded = [object for object in userPages if object['id'] == page_id]
    if len(pagesFounded):
        page_access_token = pagesFounded[0]['access_token']
    else: 
        page_access_token = ''
    return (page_id, page_access_token, keywords)

def collectData(page_id, page_access_token, keywords):

    # Keywords to search for in posts' description
    # keywords = ['merakee']

    # Get all posts from this certain page id
    graph = facebook.GraphAPI(access_token=page_access_token)
    page_post_data = graph.get_object(id=page_id, fields="posts")
    page_posts = page_post_data['posts']['data']

    # Filter posts contain certain keywords 
    posts = [(post['id'], post['created_time'])for post in page_posts if all([keyword in post['message'].lower() for keyword in keywords])]

    # Get comments from posts
    commentRows, likeRows = getCommentsFromPosts(graph, [], [], posts)

    # Save to files
    return (commentRows, likeRows)

def getCommentsFromPosts(graph, commentRows, likeRows, posts):
    # Filter = stream to get both original comments and their direct replies
    # Paginating if possible
    for post_id, created_time in posts:
        post_comments = graph.get_connections(id=post_id, connection_name='comments', filter='stream', limit='100')
        commentRows += appendComments(post_id, post_comments)

        post_likes = graph.get_object(id=post_id, fields='likes.summary(true)')
        likeRows += appendLikes(created_time, post_id, post_likes)
        
        try: 
            nextPage = post_comments['paging']['next']
            while nextPage:
                nextPageComments = requests.get(nextPage).json()
                commentRows += appendComments(post_id, nextPageComments)
                nextPage = nextPageComments['paging']['next']
        except KeyError:
            pass
    return (commentRows, likeRows)

# Check if comment is created after the last time comments were collected
# check if comment was not posted by the page itself
# then format as a row 
def appendComments(post_id, response):
    res = []
    
    if len(response['data']) != 0:
        for post in response['data']:
            sentences = []
            if isTheFirstTimeCollect:
                if post['created_time'] < lastCollectTime and 'from' not in post:
                    sentences += nltk.sent_tokenize(post['message'])
            else:
                if post['created_time'] >= lastCollectTime and 'from' not in post:
                    sentences += nltk.sent_tokenize(post['message'])
            res += list({'PostID': post_id, 'CommentID': post['id'], 'Comment': sentence.strip(), 'Label': None} for sentence in sentences)
        return res

def appendLikes(createdTime, post_id, response):
    if isTheFirstTimeCollect:
        if createdTime < lastCollectTime:
            return [{'PostID': post_id, 'Likes': response['likes']['summary']['total_count']}]
    else:
        if createdTime >= lastCollectTime:
            return [{'PostID': post_id, 'Likes': response['likes']['summary']['total_count']}]
    return []

def saveFiles(commentRows, likeRows):
    print(len(commentRows))
    print(len(likeRows))

    commentDf = pd.DataFrame(commentRows, columns = commentCols)
    likeDf = pd.DataFrame(likeRows, columns = likeCols)

    if isTheFirstTimeCollect:
        commentDf.to_csv('comments.csv', header=True, index=False)
        likeDf.to_csv('likes.csv', header=True, index=False)
    else:
        commentDf.to_csv('comments.csv', mode='a', header=False, index=False)
        likeDf.to_csv('likes.csv', mode='a', header=False, index=False)


# Main
# Evoke functions from here
# page_id, page_access_token, keywords = getUserPage('101858671714061', 'EAAPBbNbQICIBAI7IonZCG1PM70bK5P7abJMfCVLUoMhaWWwPDlcIHGd1GEstFw4eRG4ARybHqZB1L6ZA3wVu9ZBZAOQbLmTekHWrX1UN8bwcu4iArdZBwxCdZCuCw50KPwqnlz1yQmdzUH3OHuFIss7aYZAXfOM7HG98MvEaMsGAzZAAZAGVP6bJJnrCoKF4NifHx3aUKsJnwwDdfYZCpOzXbxZAu2RnZBtCBUmsUu4PJmwYJfAZDZD', ['melakee'])
# commentRows, likeRows = collectData(page_id, page_access_token, keywords)
# print(commentRows)