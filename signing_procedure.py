import hashlib
import base64
import hmac
import requests
import json
import dateparse


def generateSignature(dateandtime):

    payload = {
        "externalIdentifier": "Ice cream",
        "destinationPayeeAccountUid": "36a2e1e4-5350-4e8a-b30e-44b0c7ab506f",
        "paymentRecipient": {
          "payeeName": "Bobs accounts",
          "payeeType": "INDIVIDUAL",
          "countryCode": "GB",
          "accountIdentifier": "12345678",
          "bankIdentifier": "123456",
          "bankIdentifierType": "SORT_CODE"
        },
        "reference": "Payment reference",
        "amount": {
          "currency": "GBP",
          "minorUnits": 500
        }
      }
    m = hashlib.sha512()
    # m.update("payload string".encode('utf-8'))
    m.update(str(payload).encode('utf-8'))

    b64encoded = base64.b64encode(bytes(m.hexdigest(), 'utf-8'))
    print('\nb64encoded: ')
    print(b64encoded)
    requestUrl = '/api/v2/payments/local/account/36a2e1e4-5350-4e8a-b30e-44b0c7ab506f/category/a1ad3541-1979-4421-8706-ea43b2fd38d9'
    
    # url from example
    # requestUrl = '/api/v2/payments/local/account/90d14796-c59f-4944-9146-7fc84deb253c/category/46168325-8d23-4efe-ba48-b3a74f85f23b'

    digest = b64encoded

    # target digest from java example
    # targetDigest = 'vRbwCwvyRmlkHVxa4A45M3n31DZGqtcd1Lso9JcueCd5IoZVKyKeWtl5yluy0eAgypiN2GXOyRoXwtv55RU/Tw=='
 
    textToSign = "(request-target): put {}\nDate: {}\nDigest: {}".format(requestUrl, dateandtime, digest)
    print(textToSign)

    with open('privkey-starlingapi.pem', 'rb') as key_file:
        pv_key = key_file.read()

    messageToSign = bytes(textToSign, 'utf-8')

    parsedSignature = hmac.new(pv_key, messageToSign, hashlib.sha256).hexdigest()

    print('signature:')
    print(parsedSignature)
    print(len(parsedSignature))

    # send signature

    # url = "https://api-sandbox.starlingbank.com/api/v2/accounts"
    url = "https://api-sandbox.starlingbank.com/api/v2/payments/local/account/36a2e1e4-5350-4e8a-b30e-44b0c7ab506f/category/a1ad3541-1979-4421-8706-ea43b2fd38d9"

    # authToken = 'Bearer n8JJ2NLlWzMxryf7XwXdn5w6Jp5LME0fKfmekXxprfkRb7tMmnj0Zs51fzgKewC5'
    authToken = 'Bearer n8JJ2NLlWzMxryf7XwXdn5w6Jp5LME0fKfmekXxprfkRb7tMmnj0Zs51fzgKewC5;Signature keyid="830d89e9-7351-4f13-a140-ac3fe82c2be8",algorithm="rsa-sha256",headers="(request-target) Date Digest",signature="' + str(parsedSignature) + '"'
    # print(authToken)
    headers = {
      "content-type": "application/json",
      "Authorization": authToken,
      "Digest": digest
    }

    r = requests.put(url, data=json.dumps(payload), headers=headers)
    print('headers: ')
    print(headers)
    print("r.text: ")
    print(r.text)


date = dateparse.generateCurrentDate()
generateSignature(date)
