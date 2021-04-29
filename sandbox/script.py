import os
import json
import config
import requests
import instaloader



def ocr_space_file(filename, overlay=False, api_key=config.OCR_API_KEY, language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()


def fetch_stories(influencer_handle = 'aboutritvi')->None:
    """[summary]

    Args:
        influencer_handle (str, optional): [description]. Defaults to 'aboutritvi'.
    """    
    profile = L.check_profile_id(influencer_handle) #returns a profile Object
    # print(profile.userid)
    for story in L.get_stories(userids=[profile.userid]):
        # story is a Story object
        for item in story.get_items():
            if item.is_video is not True:
                #download all non-video type stories
                L.download_storyitem(item, config.STORIES_DIR)

def process_all():
    for file in os.listdir(config.STORIES_DIR):
        if file.endswith(".jpg"):
            print(file)
            story_path = os.path.join(config.STORIES_DIR, file)
            ocr_result = ocr_space_file(filename = story_path)
            print(ocr_result)

    
    
    

if __name__ == '__main__':
    L = instaloader.Instaloader()
    L.load_session_from_file('ig.covid_scrapper') # (load session created w/
                                #  `instaloader -l USERNAME`)
    # fetch_stories()
    process_all()
    


