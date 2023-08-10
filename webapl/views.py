from flask import request, redirect, url_for, render_template, flash
from webapl import app
import face_recognition
from PIL import Image, ImageDraw
import os


@app.route('/', methods=['GET', 'POST'])
def upload():
    # URLでhttp://127.0.0.1:5000/uploadを指定したときはGETリクエストとなるのでこっち
    if request.method == 'GET':
        return render_template('upload.html')
    # formでsubmitボタンが押されるとPOSTリクエストとなるのでこっち
    elif request.method == 'POST':
        file = request.files['img']
        if not file.filename:
            flash('ファイルを選択してください')
            return redirect(url_for('upload'))
        file.save(os.path.join('./webapl/static/image', file.filename))
        return redirect(url_for('uploaded_file', filename=file.filename))

@app.route('/<filename>')
def uploaded_file(filename):
        # 画像を読み込む
    load_image = face_recognition.load_image_file(os.path.join('./webapl/static/image', filename))
    os.remove(os.path.join('./webapl/static/image', filename))
    # 認識させたい画像から顔検出する
    face_locations = face_recognition.face_locations(load_image)

    pil_image = Image.fromarray(load_image)
    draw = ImageDraw.Draw(pil_image)

    # 検出した顔分ループする
    for (top, right, bottom, left) in face_locations:
        # 顔の周りに四角を描画する
        draw.rectangle(((left, top), (right, bottom)),
                    outline=(255, 0, 0), width=2)

    del draw
    pil_image.save(os.path.join('./webapl/static/image', "mosaic.png"))
    
    # 結果の画像を表示する
    return render_template("uploaded_file.html")


