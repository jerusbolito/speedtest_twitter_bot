from configparser import *
import tweepy
import speedtest

if __name__ == '__main__':
    # Read config file. Set interpolation to None so it doesn't error out when handling the bearer token.
    config_object = ConfigParser(strict=False, interpolation=None)
    config_object.read("config.ini")
    # Assign config values
    api_key = config_object["API_DATA"]["api_key"]
    api_secret = config_object["API_DATA"]["api_secret"]
    bearer = config_object["BEARER"]["bearer_token"]
    access_token = config_object["ACCESS_TOKEN"]["access_token"]
    access_token_secret = config_object["ACCESS_TOKEN"]["access_token_secret"]
    download_threshold = config_object["SPEEDTEST_THRESHOLD"]["download"]
    upload_threshold = config_object["SPEEDTEST_THRESHOLD"]["upload"]

    # Init speedtest object
    st = speedtest.Speedtest()

    # Get internet speed
    download_speed = "{:.2f}".format(st.download() / 1000000)
    upload_speed = "{:.2f}".format(st.upload() / 1000000)

    print(f"""
    Your internet speed -
    Download: {download_speed}Mbps
    Upload: {upload_speed}Mbps
    """)

    # If the speed does not meet the threshold set
    if (download_speed < download_threshold) or (upload_speed < upload_threshold):
        # Authenticate Twitter using the keys and secrets given in the developer page
        tw_auth = tweepy.OAuthHandler(api_key, api_secret)
        tw_auth.set_access_token(access_token, access_token_secret)
        # Init Twitter API object
        tw_api = tweepy.API(tw_auth)

        # Get ISP Info from config
        isp_name = config_object["ISP_INFO"]["name"]
        isp_handle = config_object["ISP_INFO"]["handle"]
        account_number = config_object["ISP_INFO"]["account_number"]
        # Send tweet
        tweet = f"""
        Hi {isp_name} {isp_handle}, I am experiencing slow internet connection. My download speed is {download_speed}Mbps and my upload speed is {upload_speed}Mbps. Account number is {account_number}. Please fix.

Threshold set-
Download: {download_threshold}Mbps
Upload: {upload_threshold}Mbps
Sent via Python 3.9 bot
        """
        try:
            tw_api.update_status(tweet)
            print("Successfully sent Tweet")
        except Exception as e:
            print(f"Error: {e}")


