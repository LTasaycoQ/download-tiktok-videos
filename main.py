import os
import re
from flask import Flask,request ,send_file, render_template
import http.client
import json

app = Flask(__name__, template_folder='src')



conn = http.client.HTTPSConnection("tiktok-scrapper-videos-music-challenges-downloader.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "a48bd620e4mshcce244fcebce6b1p19bc12jsn0411ee9231cf",
    'x-rapidapi-host': "tiktok-scrapper-videos-music-challenges-downloader.p.rapidapi.com"
}

@app.route("/")
def index():
    return send_file('src/index.html')


@app.route('/submit', methods=['POST'])
def submit():
    url_video = request.form['url_video'] 
    match = re.search(r'/video/(\d+)', url_video)
    if match:
        video_id = match.group(1)
        print(video_id) 
        conn.request("GET", "/video/"+video_id, headers=headers)
        res = conn.getresponse()
        data = res.read()
        decod = data.decode("utf-8")

        try:
            json_data = json.loads(decod)
            
            if 'data' in json_data:
                if 'aweme_detail' in json_data['data']:
                    if 'video' in json_data['data']['aweme_detail']:
                        if 'play_addr' in json_data['data']['aweme_detail']['video']:
                            if 'url_list' in json_data['data']['aweme_detail' ]['video']['play_addr']:
                                response_text = json_data['data']['aweme_detail']['video']['play_addr']['url_list'][0]
                                url_generada_api = response_text
                            else:
                                response_text = "No encontrado pero estamos aun mas cerca."
                        else:
                            response_text = "Ui, estamos mal :( perocerca"
                if 'aweme_detail' in json_data['data']:
                    if 'video' in json_data['data']['aweme_detail']:
                        if 'cover' in json_data['data']['aweme_detail']['video']:
                            if 'url_list' in json_data['data']['aweme_detail' ]['video']['cover']:
                                response_text_logo = json_data['data']['aweme_detail']['video']['cover']['url_list'][0]
                                logo_generada_api = response_text_logo
                            else:
                                response_text = "No encontrado pero estamos aun mas cerca."
                        else:
                            response_text = "Ui, estamos mal :( perocerca"
                    if 'author' in json_data['data']['aweme_detail']:

                        if 'unique_id' in json_data['data']['aweme_detail']['author']:
                            response_text_nombre = json_data['data']['aweme_detail']['author']['unique_id']
                            author_nombre = response_text_nombre

                        if 'nickname' in json_data['data']['aweme_detail']['author']:
                            response_text_nickname = json_data['data']['aweme_detail']['author']['nickname']
                            author_nickname = response_text_nickname

                        if 'avatar_300x300' in json_data['data']['aweme_detail']['author']:
                            if 'url_list' in json_data['data']['aweme_detail' ]['author']['avatar_300x300']:
                                response_text_author_logo = json_data['data']['aweme_detail']['author']['avatar_300x300']['url_list'][0]
                                author_logo = response_text_author_logo
                            else:
                                response_text = "No encontrado pero estamos aun mas cerca."
                        

                        else:
                            response_text = "Ui, estamos mal :( perocerca"
              
                else:
                    response_text = "Ui, estamos mal :("
                
            
            else:
                response_text = "Ui, estamos mal :("

        except json.JSONDecodeError:
            response_text = "Error al decodificar la respuesta JSON."

      
    return render_template('index.html',author_nickname_api= author_nickname,author_nombre_py= author_nombre, response=url_generada_api, logo_py=logo_generada_api, logo_author_api = author_logo)




def main():
    app.run(port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    main()
