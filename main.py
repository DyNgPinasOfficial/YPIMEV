from pytube import YouTube
from pytube import Playlist
from moviepy.editor import AudioFileClip
import os
import re
import music_tag as mt

def remove_special_characters(input_string):
    pattern = re.compile(r'[^a-zA-Z0-9 .]')
    result_string = re.sub(pattern, '', input_string)
    return result_string


def webm_to_mp3(output_path, file:str, metadata:dict):
    try:
        webm_file_path = fr"{output_path}/{file}"
        webm_audio = AudioFileClip(webm_file_path, fps=48000)
        mp3_audio_path = webm_file_path.replace(".webm", ".mp3")
        webm_audio.write_audiofile(fr"{mp3_audio_path}", fps=48000, nbytes=4)
        
        mp3_tags = mt.load_file(mp3_audio_path)
        mp3_tags['title'] = metadata['title']
        mp3_tags['artist'] = metadata['artist']
        mp3_tags['album'] = metadata['album']
        mp3_tags['year'] = metadata['year']
        mp3_tags.save()
        if os.path.exists(webm_file_path):
            os.remove(webm_file_path)
    except Exception as error:
        print(error)


def yt_to_webm(link):
    yt_vid = YouTube(link)
    yt_title = yt_vid.title
    file_name = f"{remove_special_characters(yt_title)}.webm"
    metadata = {
        'title': yt_title,
        'artist': yt_vid.author,
        'album': yt_vid.author,
        'year': yt_vid.publish_date.year,
    }
    stream = yt_vid.streams.get_by_itag(251) #160 bit rate
    output_path = "downloads"
    stream.download(output_path= output_path, filename=file_name)
    webm_to_mp3(output_path, file_name, metadata)


if __name__ == "__main__":
    yt_Playlist = Playlist('https://www.youtube.com/watch?v=KFyGuJM6t7A&list=RDKFyGuJM6t7A')
    playlist_folder = yt_Playlist.title

    
    playlist_vids = yt_Playlist.video_urls
    total_vid = len(playlist_vids)

    for pos in range(total_vid):
        count = pos + 1
        vid_link = playlist_vids[pos]
        try:
            yt_to_webm(vid_link)
        except Exception as err:
            print(err)
        print(f"[{count}/{total_vid}] {((count / total_vid) * 100)//1}%: {vid_link}")



    
        
