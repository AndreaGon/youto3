from flask import Flask, render_template, request, send_file
import youtube_dl
import os

app=Flask(__name__, template_folder='template')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=['POST'])
def download():
    try:
        if request.method=='POST':
            url=request.form["url_name"]
            youtube_opts = {
                'outtmpl': 'temp/'+str(url)[16:]+'.mp3',
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
            }

            with youtube_dl.YoutubeDL(youtube_opts) as ydl:
                vid_info = ydl.extract_info(url, download=False)
                ydl.download([url])
                return send_file('temp/'+str(url)[16:]+'.mp3', attachment_filename='{}.mp3'.format(vid_info.get('title', None)), as_attachment=True)
    except:
        return render_template('index.html', text="Please provide a valid Youtube video url.")

    #os.remove('temp/dhW1mh7U6-U.mp3')



if __name__ == '__main__':
    app.debug=True
    app.run()
