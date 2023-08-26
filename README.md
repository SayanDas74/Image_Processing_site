
# ChromaCraft - an Image Editing Web Application

ChromaCraft is an Image Editing Flask Application which applies simple image editing on an image.


## About
ChromaCraft is a simple yet effective Image Editing web app built using Flask and OpenCV. This web application empowers users to upload images and unleash their creativity through a range of image processing operations. From cropping and resizing to applying filters, ChromaCraft offers an enjoyable experience for manipulating images.\
_**Back-end: Python**_ \
_**Front-end: HTML, CSS, JavaScript**_
## Features
**Upload Image:** ChromaCraft allows users to effortlessly upload images to perform editing that too in various formats, including webp, png, jpg, and jpeg.\
**Crop Image:** With the interactive cropping feature, users can easily select and extract specific regions of the uploaded image.\
**Resize Image:** Users have the flexibility to resize their images, maintaining the aspect ratio for consistent and balanced proportions.\
**Filters:** Offers a delightful array of filters to transform images into unique pieces of art. Users can choose from Black & White, Exposure, and Oil Painting filters.
## Frameworks and Libraries Used
- **Flask**: A lightweight web framework used for building the web applications.

- **OpenCV**: Utilized for powerful image processing operations, including cropping, resizing, and applying artistic filters.
## How to Use
1. Begin your journey by uploading an image. Click the "Choose File" button and select an image from your local machine.

2. Select the desired operation from the dropdown menu.

3. Execute the operation by clicking the corresponding button to process the uploaded image.

4. The result of the corresponding operation will be displayed.
## Endpoints
### Home
```python
@app.route("/", methods=['GET','POST'])
def home():
    if request.method == "POST":
        operation = request.form.get("operation")
        file = request.files['file']

        if file.filename == '':
            flash('No file chosen')
            return redirect(request.url)
        
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
            return redirect(request.url)

    return render_template("index.html")
```
### Crop
```python
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
                    cv2.imwrite(os.path.join("D:/PROGRAMS/IMAGE PROCESSING SITE/static", filename), cropped)
                    cv2.destroyAllWindows()
                    return redirect(url_for('display_cropped_image', filename=filename))

            cv2.namedWindow(winname="window", flags=cv2.WINDOW_NORMAL)
            cv2.setMouseCallback("window", crop)
            cv2.imshow("window", img)
            cv2.setWindowProperty("window", cv2.WND_PROP_TOPMOST, 1)
            cv2.waitKey(0)
    return render_template("crop.html", image_filename=filename)
```
### Resize 
```python
@app.route("/resize", methods=['GET', 'POST'])
def resize():
    if request.method == "POST":
        # Get the input dimensions from the form
        width = int(request.form.get("width"))
        height = int(request.form.get("height"))

        filename = session.get('filename')
        img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Resize the image
        resized_img = cv2.resize(img, (width, height))
        resized_filename = f"resized_{filename}"
        cv2.imwrite(os.path.join("D:/PROGRAMS/IMAGE PROCESSING SITE/static", resized_filename), resized_img)
        return render_template("resize.html", resized_filename=resized_filename)

    return render_template("resize.html")
```
### Filter 
```python
@app.route("/filter", methods=['GET', 'POST'])
def filter():
    if request.method == "POST":
        filter_option = request.form.get("filter_option")
        filename = session.get('filename')
        img = cv2.imread("D:/PROGRAMS/IMAGE PROCESSING SITE/uploads" + "/" + filename)

        # Apply the selected filter option
        if filter_option == "black_white":
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_filtered = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
            filtered_filename = f"filtered_{filename}"
            cv2.imwrite(os.path.join("D:/PROGRAMS/IMAGE PROCESSING SITE/static", filtered_filename), img_filtered)
        elif filter_option == "exposure":
            sepia_kernel = np.array([[0.272, 0.534, 0.131],
                                     [0.349, 0.686, 0.168],
                                     [0.393, 0.769, 0.189]])
            img_filtered = cv2.filter2D(img, -1, sepia_kernel)
            filtered_filename = f"filtered_{filename}"
            cv2.imwrite(os.path.join("D:/PROGRAMS/IMAGE PROCESSING SITE/static", filtered_filename), img_filtered)
        elif filter_option == "painting":
            img_filtered = cv2.xphoto.oilPainting(img, 7, 1)
            filtered_filename = f"filtered_{filename}"
            cv2.imwrite(os.path.join("D:/PROGRAMS/IMAGE PROCESSING SITE/static", filtered_filename), img_filtered)
        else:
            flash("Invalid filter option selected")
            return render_template("filter.html")
        return render_template("filter.html", filtered_filename=filtered_filename)

    return render_template("filter.html")
```
## Templates
- ### [index.html](https://github.com/SayanDas74/Image_Processing_site/blob/master/templates/index.html)

- ### [crop.html](https://github.com/SayanDas74/Image_Processing_site/blob/master/templates/crop.html)

- ### [resize.html](https://github.com/SayanDas74/Image_Processing_site/blob/master/templates/resize.html)

- ### [filter.html](https://github.com/SayanDas74/Image_Processing_site/blob/master/templates/filter.html)
## Note
1. ChromaCraft is designed for demonstration purposes and may require further optimization for large-scale deployment.

2. Ensure that you provide a valid image in one of the allowed formats for processing.

3. The uploaded images are temporarily stored in the "Uploads" folder, and the processed images are available in the "Static" folder.

4. Make sure to change the path in the code as per your local machine.
