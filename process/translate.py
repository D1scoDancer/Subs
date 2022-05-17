import requests

def translate(texts):
    IAM_TOKEN = get_iam_token()
    folder_id = 'b1got1e9ura7lrubkir9'  
    target_language = 'ru'              

    body = {
        "targetLanguageCode": target_language,
        "texts": texts,
        "folderId": folder_id,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(IAM_TOKEN)
    }

    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
        json = body,
        headers = headers
    )

    return response

def get_iam_token():
    headers = {'Content-Type': 'application/x-www-form-urlencoded',}
    data = '{"yandexPassportOauthToken":"AQAAAABRifOPAATuwakY-M_p50s4nIzyJB2mHwk"}'

    response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', headers=headers, data=data)
    iam = response.json()['iamToken']

    return iam