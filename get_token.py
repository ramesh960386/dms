import requests


def get_token(username, password):
    data = {
        'username': username,
        'password':password
    }
    url = 'http://localhost:9020/api-token-auth/' #username='admin' password="admin"
    r = requests.post(url, data=data)
    print(r.json())



if __name__ == '__main__':
    get_token('admin', 'admin')
    """
    https: // www.geeksforgeeks.org / implement - token - authentication - using - django - rest - framework /
    https://simpleisbetterthancomplex.com/tutorial/2018/11/22/how-to-implement-token-authentication-using-django-rest-framework.html
    https://studygyaan.com/django/how-to-secure-media-files-in-django
    @@@@@@@@@@
    https://stackoverflow.com/questions/50188750/ajax-response-need-to-be-converted-to-blob
    https://www.coderrocketfuel.com/article/get-the-url-origin-of-a-web-page-in-javascript
    https://pspdfkit.com/blog/2019/implement-pdf-viewer-pdf-js/
    viewer.js
    @@@@@@@@@@@@@@@@@
    curl POST http://localhost:9020/api-token-auth/ username='admin' password='admin'
    curl http://127.0.0.1:9020/media/uploads/dummy_pdf.pdf/ -H 'Authorization: token 90a03496eddfb421b5b795292eced8b64777f2d8'
    curl -X POST http://127.0.0.1:9020/media/uploads/dummy_pdf.pdf/ -H "Authorization: token 90a03496eddfb421b5b795292eced8b64777f2d8"
    """