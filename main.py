from flask import Flask, render_template, request, flash, redirect, url_for, session, send_from_directory
from werkzeug.utils import secure_filename
import cv2
import os
import numpy as np

UPLOAD_FOLDER = 'D:/PROGRAMS/[[[ IMAGE PROCESSOR PROJECT ]]]/uploads'
PROCESSED_FOLDER = 'D:/PROGRAMS/[[[ IMAGE PROCESSOR PROJECT ]]]/static'
ALLOWED_EXTENSIONS = {'webp', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET','POST'])
def home():
    if request.method == "POST":
        operation = request.form.get("operation")
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            session['filename'] = filename
            session['operation'] = operation
        
        if operation == "crp":
            return redirect(url_for('crop'))
        elif operation == "rsz":
            return redirect(url_for('resize'))
        elif operation == "fltr":
            return redirect(url_for('filter'))
        else:
            flash("Invalid operation selected")
            return render_template("index.html")

    return render_template("index.html")

@app.route("/crop")
def crop():
    filename = session.get('filename')
    operation = session.get('operation')
    print(f"The operation is {operation} and filename is {filename}")
    img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    if img is not None:
        if operation == "crp":
            img = cv2.resize(img, (800, 600))

            def crop(event, x, y, flags, params):
                nonlocal img
                global flag, ix, iy
                if event == cv2.EVENT_LBUTTONDOWN:  # if left mouse button is clicked
                    flag = True
                    ix, iy = x, y
                elif event == cv2.EVENT_LBUTTONUP:  # if left mouse button is released
                    flag = False
                    fx, fy = x, y
                    cv2.rectangle(img, pt1=(ix, iy), pt2=(x, y), thickness=1, color=(0, 0, 0))
                    cropped = img[iy:fy, ix:fx]
                    cv2.imwrite(os.path.join("D:/PROGRAMS/[[[ IMAGE PROCESSOR PROJECT ]]]/static", filename), cropped)
                    cv2.destroyAllWindows()
                    return redirect(url_for('display_cropped_image', filename=filename))

            cv2.namedWindow(winname="window", flags=cv2.WINDOW_NORMAL)
            cv2.setMouseCallback("window", crop)
            cv2.imshow("window", img)
            cv2.setWindowProperty("window", cv2.WND_PROP_TOPMOST, 1)
            cv2.waitKey(0)
    return render_template("crop.html", image_filename=filename)


@app.route("/resize", methods=['GET', 'POST'])
def resize():
    if request.method == "POST":
        # Get the input dimensions from the form
        width = int(request.form.get("width"))
        height = int(request.form.get("height"))

        # Retrieve the filename from the session
        filename = session.get('filename')

        # Read the image using OpenCV
        img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Resize the image
        resized_img = cv2.resize(img, (width, height))

        # Save the resized image
        resized_filename = f"resized_{filename}"
        cv2.imwrite(os.path.join("D:/PROGRAMS/[[[ IMAGE PROCESSOR PROJECT ]]]/static", resized_filename), resized_img)

        # Render the template to display the resized image
        return render_template("resize.html", resized_filename=resized_filename)

    return render_template("resize.html")

@app.route("/filter", methods=['GET', 'POST'])
def filter():
    if request.method == "POST":
        # Get the selected filter option
        filter_option = request.form.get("filter_option")

        # Retrieve the filename from the session
        filename = session.get('filename')

        # Read the image using OpenCV
        img = cv2.imread("D:/PROGRAMS/[[[ IMAGE PROCESSOR PROJECT ]]]/uploads" + "/" + filename)

        # Apply the selected filter option
        if filter_option == "black_white":
            # Convert image to black and white
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_filtered = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
            filtered_filename = f"filtered_{filename}"
            cv2.imwrite(os.path.join("D:/PROGRAMS/[[[ IMAGE PROCESSOR PROJECT ]]]/static", filtered_filename), img_filtered)
        elif filter_option == "vintage":
            # Apply vintage filter (add your own filter logic)
            # Example: Convert image to sepia tone
            sepia_kernel = np.array([[0.272, 0.534, 0.131],
                                     [0.349, 0.686, 0.168],
                                     [0.393, 0.769, 0.189]])
            img_filtered = cv2.filter2D(img, -1, sepia_kernel)
            filtered_filename = f"filtered_{filename}"
            cv2.imwrite(os.path.join("D:/PROGRAMS/[[[ IMAGE PROCESSOR PROJECT ]]]/static", filtered_filename), img_filtered)
        elif filter_option == "painting":
            # Apply painting filter (add your own filter logic)
            # Example: Apply oil painting effect
            img_filtered = cv2.xphoto.oilPainting(img, 7, 1)
            filtered_filename = f"filtered_{filename}"
            cv2.imwrite(os.path.join("D:/PROGRAMS/[[[ IMAGE PROCESSOR PROJECT ]]]/static", filtered_filename), img_filtered)
        else:
            flash("Invalid filter option selected")
            return render_template("filter.html")

        # Render the template to display the filtered image
        return render_template("filter.html", filtered_filename=filtered_filename)

    return render_template("filter.html")


if __name__ == '__main__':
    app.run(debug=True, port=5001)
