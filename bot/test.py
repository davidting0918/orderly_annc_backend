from lib.adaptor import AnnouncementClient


api_key = "a21e517c10cf09a245aff962a7c1e6ef"
api_secret = "3ee460f0e320971de84035266762ecba1bf8782f6b7891415093dcda20b3f79d"


if __name__ == "__main__":
    client = AnnouncementClient(api_key, api_secret)

    res = client.get_user_info(nums=100)
    print(res)