from django.db import models
import vrchatapi as vr
from vrchatapi.api import authentication_api, users_api, friends_api
from vrchatapi.model.limited_user import LimitedUser
from pprint import pprint

class vrchatLogin():

    def __init__(self,_id,pw):
        self.id = _id
        self.pw = pw
    
    def vrchatLoginID (_id, pw):
        configuration = vr.Configuration(
            username=_id,
            password=pw,
        )

        with vr.ApiClient(configuration) as api_client:

            print('*************************************** api의 권한 받기')
            auth_api = authentication_api.AuthenticationApi(api_client)

            try:
                current_user = auth_api.get_current_user()
                print('******************************* Logged in as:', current_user.display_name)
                a = configuration
                b = 'success'

            except vr.ApiException as e:
                print('*************************************** 로그인 실패')
                print('Exception when calling API: %s\n', e)
                a = None
                b = 'failed'

        if _id == None and pw == None :
            b = ''

        return a, b


class vrchatFriends():

        def vrchatFriends(self, configutration):

            with vr.ApiClient(configutration) as api_client:

                auth_api = authentication_api.AuthenticationApi(api_client)
                api_instance = friends_api.FriendsApi(api_client)
                api_instance_user = users_api.UsersApi(api_client)
                current_user = auth_api.get_current_user()

                offset = 0
                n = 60
                offline = True

                try:
                    # 친구 리스트 불러오기
                    f_Offiline = api_instance.get_friends(offset=offset, n=n, offline=True)
                    f_Online = api_instance.get_friends(offset=offset, n=n, offline=False)
                    f_full = f_Offiline + f_Online
                    print('*************************************** 유저 정보')
                    pprint(f_full[0])

                    # 오프라인과 온라인 구분 정렬
                    context = []
                    contextOn = []  # oline
                    contextOff = []  # offline
                    # contextSearch = [] # search

                    for i in f_full:

                        print('*************************************** 유저 접속 상태')
                        api_response = api_instance_user.get_user(i['id'])
                        print(api_response)
                        row = {
                            'displayName': i['display_name'],
                            'state': str(api_response['state']),
                            'status': str(i['status']),
                            'location': i['location'],
                            'lastLogin': i['last_login'],
                            'AvatarImg': i['current_avatar_thumbnail_image_url']}

                        # searchNameUp = searchName.upper() if searchName != None else ''
                        # rowNameUp = i['display_name'].upper()
                        #
                        # if searchNameUp == rowNameUp:
                        #     contextSearch.append(row)

                        if str(i['status']) == 'offline':
                            contextOff.append(row)
                        else:
                            contextOn.append(row)

                    # if len(contextSearch) == 0:
                    print('*************************************** 데이터 정렬')
                    context = contextOn + contextOff
                    print('*************************************** Online')
                    print(contextOn)
                    print('*************************************** Offline')
                    print(contextOff)

                    return context

                except vr.ApiException as e:
                    print("Exception when calling FriendsApi->get_friends: %s\n" % e)
