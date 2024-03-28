from huaweicloudsdkcore.auth.credentials import GlobalCredentials
from huaweicloudsdkiam.v3.region.iam_region import IamRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkiam.v3 import *
import json
from huaweicloudsdkiam.v3 import *
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from myapp.models import Data


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, KeystoneCreateUserTokenByPasswordResponse):
            return obj.to_dict()
        return super().default(obj)

def getToken():
    # The AK and SK used for authentication are hard-coded or stored in plaintext, which has great security risks. It is recommended that the AK and SK be stored in ciphertext in configuration files or environment variables and decrypted during use to ensure security.
    # In this example, AK and SK are stored in environment variables for authentication. Before running this example, set environment variables CLOUD_SDK_AK and CLOUD_SDK_SK in the local environment
    ak = "MJI56TRASQOYAPJEFIDE"
    sk = "U0Fm1sBqFD7fSbaUjpCD19j9sXk1aOs1YD6Vig3O"
    credentials = GlobalCredentials(ak, sk) \

    client = IamClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(IamRegion.value_of("cn-north-4")) \
        .build()

    try:
        request = KeystoneCreateUserTokenByPasswordRequest()
        projectScope = AuthScopeProject(
            id="22f29e6c93b4485ab7540fe2c8f8e353",
            name="cn-north-4"
        )
        scopeAuth = AuthScope(
            project=projectScope
        )
        domainUser = PwdPasswordUserDomain(
            name="darren_jiang"
        )
        userPassword = PwdPasswordUser(
            domain=domainUser,
            name="jiang1",
            password="jly134679852."
        )
        passwordIdentity = PwdPassword(
            user=userPassword
        )
        listMethodsIdentity = [
            "password"
        ]
        identityAuth = PwdIdentity(
            methods=listMethodsIdentity,
            password=passwordIdentity
        )
        authbody = PwdAuth(
            identity=identityAuth,
            scope=scopeAuth
        )
        request.body = KeystoneCreateUserTokenByPasswordRequestBody(
            auth=authbody
        )
        response = client.keystone_create_user_token_by_password(request)
        # print(response)
        response_str = json.dumps(response,cls=CustomEncoder)
        json_data = json.loads(response_str)
        token = json_data["x_subject_token"]
        print(token)
        return token
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)


@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        url = "https://c634a986f3644512a8d495a5bb082c07.apig.cn-north-4.huaweicloudapis.com/v1/infers/44c521be-946d-4f20-a21a-9ce99c72195b"
        token = getToken()
        save_path = './resource/' + image_file.name
        # 将图片文件保存到指定路径
        with open(save_path, 'wb') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)
        headers = {
            'X-Auth-Token': token
        }
        files = {
            'images': open(save_path, 'rb')
        }
        resp = requests.post(url, headers=headers, files=files)
        json_data = resp.json()
        original = json_data
        predict = json_data['predicted_label']
        new_data = Data(original_data=original,identify_data=predict)
        new_data.save()

        print(resp.status_code)
        print(resp.text)

        return JsonResponse({'message': 'Image uploaded successfully'})
    else:
        return JsonResponse({'error': 'Image upload failed'})