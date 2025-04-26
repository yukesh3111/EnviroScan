from datetime import datetime
from shutil import rmtree
from flask import Flask, abort,render_template,redirect,url_for,session,request,flash,jsonify,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Message,Mail
from ultralytics import YOLO
from werkzeug.utils import secure_filename
from ultralytics import YOLO
from roboflow import Roboflow
import os
import cv2
import numpy as np
app=Flask(__name__)


#upload folder configuration
upload_folder = os.path.join('static', 'uploads')
app.config['UPLOAD'] = upload_folder
#sesion scecret key
app.secret_key="dfsfdfsd;sd[flsfl[pgsd[sdfs'sddsasf55133]]]"
#database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///enviroscan.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
#mail configuration
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'iloveyoujuliet28@gmail.com'
app.config['MAIL_PASSWORD'] = 'ghbf dmmp umnl krge'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)
db=SQLAlchemy(app)

upload_folder = os.path.join('static', 'adminuploads')
app.config['UPLOAD'] = upload_folder



#mobile api functions
def apigreenland(imgpath,filename):
    rf = Roboflow(api_key="CUDoe3R064m7QBg7nP7b")
    project = rf.workspace().project("tree-detection-f6mmn")
    model = project.version(1).model
    model.opacity = 99
    model.overlap = 25
    model.predict(imgpath).save(f"static/greenspace/{filename}")
    green,land=apipercentage()
    return green,land

def apipercentage():
    image = cv2.imread(r'static/greenspace/prediction.jpg')
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([90, 255, 255])
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)
    green_visualization = cv2.bitwise_and(image, image, mask=green_mask)
    cv2.imwrite('static/greenspace/processed.jpg', green_visualization)
    green_area = np.count_nonzero(green_mask)
    total_area = image.shape[0] * image.shape[1]
    green_percentage = (green_area / total_area) * 100
    land_percentage = 100 - green_percentage
    return green_percentage,land_percentage




def delete_previous_predict_folders():
    # Delete previous 'predict' folders if they exist
        try:
            rmtree(r"runs\detect\predict")
        except Exception as e:
            print(f"Error occurred while deleting: {e}")


#this is a function for predicting trees count
def predict (image_path):
    delete_previous_predict_folders()
    infer=YOLO(r"best.pt")
    result=infer.predict(image_path,conf=0.95,save=True,save_txt=True)
    total_trees = 0             

    for result in result:
        total_trees += len(result.boxes)

    print("Total number of trees detected:", total_trees)
    return total_trees





def percentage(filename):
    image = cv2.imread(r'static/greenspace/'+filename)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([90, 255, 255])
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)
    green_visualization = cv2.bitwise_and(image, image, mask=green_mask)
    cv2.imwrite('static/greenspace/processed.jpg', green_visualization)
    green_area = np.count_nonzero(green_mask)
    total_area = image.shape[0] * image.shape[1]
    green_percentage = (green_area / total_area) * 100
    land_percentage = 100 - green_percentage
    return green_percentage,land_percentage


#this is a function for green space and land space
def greenland(imgpath,filename):
    rf = Roboflow(api_key="0YjWW9oyEX0rwncjLXbC")
    project = rf.workspace().project("tree-detection-f6mmn")
    model = project.version(1).model
    model.opacity = 99
    model.overlap = 25
    model.predict(imgpath).save("static/greenspace/"+filename)
    green,land=percentage(filename)
    return green,land


#this is a function for species identification
def species_indenti(img,filename):
    rf = Roboflow(api_key="mJgIDP0cpHzQD1XKvcu9")
    project = rf.workspace().project("tree-species-identification-rjtsb")
    model = project.version(1).model

    # infer on a local image
    result=model.predict(img, confidence=1, overlap=1).json()
    class_names = [prediction['class'] for prediction in result['predictions']]
    confidence = [prediction['confidence'] for prediction in result['predictions']]
    report=0
    if(len(confidence)>0 and max(confidence)>=0.18):
            report=1
    else:
        report=2
    print(class_names)
    print(confidence)
    print(report)
    # visualize your prediction
    model.predict(img, confidence=10, overlap=30).save("static/species/"+filename)

    return class_names,report,confidence




class userdetails(db.Model):
    username=db.Column("username",db.String(100),primary_key=True)
    password=db.Column("password",db.String(100))
    name=db.Column("name",db.String(100))
    surename=db.Column("surename",db.String(100))
    phone_no=db.Column("phone_no",db.Integer())
    email=db.Column("email",db.String(100))
    address=db.Column("address",db.String(100))
    city=db.Column("city",db.String(100))
    state=db.Column("state",db.String(100))

    def __init__ (self,username,name,surename,phone_no,email,address,city,state,password) :
        self.username=username
        self.name=name
        self.surename=surename
        self.phone_no=phone_no
        self.email=email
        self.address=address
        self.city=city
        self.state=state
        self.password=password
    def __repr__(self) :
        return f"{self.username}:{self.password}:{self.name}:{self.surename}:{self.phone_no}:{self.email}:{self.address}:{self.city}:{self.state}"


class greencover(db.Model):
    serial_no=db.Column("serial_no",db.Integer(),primary_key=True,autoincrement=True)
    green_percentage=db.Column("green_percentage",db.Integer())
    green_description=db.Column("green_description",db.String(100))
    green_recommentation=db.Column("gree_recommentation",db.String(10000))
    
    def __init__ (self,serial_no,green_percentage,green_recommentation,green_description):
        self.serial_no=serial_no
        self.green_percentage=green_percentage
        self.green_description=green_description
        self.green_recommentation=green_recommentation
        
    def __repr__(self) :
        return f"{self.serial_no}:{self.green_percentage}:{self.green_description}"


class admindetails(db.Model):
    adminname=db.Column("adminname",db.String(100),primary_key=True)
    password=db.Column("password",db.String(100))
    name=db.Column("name",db.String(100))
    phone_no=db.Column("phone_no",db.Integer())
    email=db.Column("email",db.String(100))
    def __init__ (self,adminname,name,phone_no,email,password) :
        self.adminname=adminname
        self.name=name
        self.phone_no=phone_no
        self.email=email
        self.password=password
    def __repr__(self) :
        return f"{self.adminname}:{self.password}:{self.name}:{self.phone_no}:{self.email}"

class article(db.Model):
    article_no=db.Column("Article_no",db.Integer(),primary_key=True, autoincrement=True)
    article_title=db.Column("Article_Title",db.String(1000000))
    article_subtitle=db.Column("Article_Subtitle",db.String(10000000))
    article_domain=db.Column("Article_Domain",db.String(10000000))
    article_abstraction=db.Column("Article_Abstraction",db.String(10000000))
    article_maincontent=db.Column("Article_Maincontent",db.String(100000000))
    article_conculsion=db.Column("Article_Conclusion",db.String(10000000))
    article_filename=db.Column("Article_filename",db.String(100000))
    article_date = db.Column("Published Date",db.String(12), nullable=False, default=lambda: datetime.utcnow().strftime('%d %b %Y'))
   
    def __init__ (self,article_title,article_filename,article_abstraction,article_subtitle,article_domain,article_maincontent,article_conculsion) :
       
        self.article_title=article_title
        self.article_subtitle=article_subtitle
        self.article_domain=article_domain
        self.article_abstraction=article_abstraction
        self.article_maincontent=article_maincontent
        self.article_conculsion=article_conculsion
        self.article_filename=article_filename
        
    def __repr__(self) :
        return f"{self.article_title}:{self.article_subtitle}:{self.article_domain}:{self.article_abstraction}:{self.article_maincontent}:{self.article_conculsion}"



class treecounting(db.Model):
    tree_id=db.Column("tree_id",db.Integer(),primary_key=True, autoincrement=True)
    longitude=db.Column("longitude",db.Integer())
    latitude=db.Column("latitude",db.Integer())
    tree_count=db.Column("tree_count",db.Integer())
    def __init__ (self,tree_count,latitude,longitude):
        self.tree_count=tree_count
        self.latitude=latitude
        self.longitude=longitude
    def __repr__(self) :
        return f"{self.tree_id}"


class statistics(db.Model):
    Species_id=db.Column("Species_id",db.Integer(),primary_key=True)
    Tree_Species=db.Column("Tree_Species",db.String(1000000))
    Species_Description=db.Column("Species_Description",db.String(100000))
    Physical_Charateristics=db.Column("Physical_Characteristics",db.String(100000))
    Ecological_role=db.Column("Ecological_role",db.String(100000))
    Intresting_fact=db.Column("Intresting_fact",db.String(100000))  
    
    def __init__ (self,Tree_Species,Species_Description,Intresting_fact,Ecological_role,Physical_Charateristics):
        self.Tree_Species=Tree_Species
        self.Species_Description=Species_Description
        self.Ecological_role=Ecological_role
        self.Physical_Charateristics=Physical_Charateristics
        self.Intresting_fact=Intresting_fact
        
    def __repr__(self) :
        return f"{self.Tree_Species}:{self.Species_Description}"
#Admin pages


@app.route('/adminlogin',methods=['POST','GET'])
def adminlogin():
    if 'admin' in session:
        session.pop('admin')
    if 'user' in session:
        session.pop('user')
    if request.method=='POST':
        login_adminname=request.form["adminname"]
        login_password=request.form["password"] 
        session["admin"]=login_adminname
        print(login_adminname,login_password)
        admin=admindetails.query.filter_by(adminname=login_adminname).first()
        print(admin)
        if admin and ('ADMIN' in login_adminname):
            if admin.password==login_password:
                print("login sucessfully")
                flash(f"Login Successful! Welcome back to our platform.")
                return redirect(url_for("adminhome"))
            else:
                flash(f"We're sorry, but the adminname or password you entered is incorrect. Please double-check your credentials and try again.")
                return redirect(url_for("adminlogin"))
        else :
            flash(f"We couldn't find an account registered with the provided credentials. Please make sure you've entered the correct information or consider signing up for an account.")
            return redirect(url_for("adminlogin"))
    else:
        return render_template("adminlogin.html")

@app.route('/adminhome/')
def adminhome():
    if 'admin' in session:
        role='admin'
        max_article1 = article.query.order_by(article.article_no.desc()).first()
        max_article2= article.query.order_by(article.article_no.desc()).offset(2-1).first()
        max_article3=article.query.order_by(article.article_no.desc()).offset(3-1).first()
        return render_template('adminhome.html',role=role,max1=max_article1.article_no,max2=max_article2.article_no,max3=max_article3.article_no,article1_title=max_article1.article_subtitle,article1_abstraction=max_article1.article_abstraction,article2_title=max_article2.article_subtitle,article2_abstraction=max_article2.article_abstraction,article3_title=max_article3.article_subtitle,article3_abstraction=max_article3.article_abstraction)
    else:
        return redirect(url_for('login'))


@app.route('/admin-post-article',methods=['POST','GET'])
def adminpost():
    if 'admin' in session:
        if(request.method=='POST'):
            title=request.form['article_title']
            subtitle=request.form['article_subtitle']
            domain=request.form['article_domain']
            abstration=request.form['article_abstraction']
            main_content=request.form['main_content']
            conclusion=request.form['conclusion']
            file=request.files["image"]
            filename=secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD'], filename))
            print(title,'\n',subtitle,'\n',domain,'\n',abstration,'\n',main_content,'\n',conclusion,'\n')
            articledetails=article(article_title=title,article_subtitle=subtitle,article_abstraction=abstration,article_domain=domain,article_maincontent=main_content,article_conculsion=conclusion,article_filename=filename)
            db.session.add(articledetails)
            db.session.commit()
            flash("Article post sucessfully")
            return redirect(url_for('adminpost'))
        else:
            return render_template('post_article.html')
    else:
        return redirect(url_for('login'))


@app.route('/article<name>/<role>')
def articlepage(name,role):
    if 'admin' in session: 
        max_article1=article.query.filter_by(article_no=name).first()
        return render_template("viewarticle.html",role=role,atricle_no=name,articel_title=max_article1.article_title,article_subtitle=max_article1.article_subtitle,article_abstraction=max_article1.article_abstraction,article_maincontent=max_article1.article_maincontent,article_conclusion=max_article1.article_conculsion,filename=max_article1.article_filename)
    elif 'user' in session:
        max_article1=article.query.filter_by(article_no=int(name)).first()
        print(max_article1.article_title, name)
        return render_template("viewarticle.html",role=role,atricle_no=name,articel_title=max_article1.article_title,article_subtitle=max_article1.article_subtitle,article_abstraction=max_article1.article_abstraction,article_maincontent=max_article1.article_maincontent,article_conclusion=max_article1.article_conculsion,filename=max_article1.article_filename)
        
    else:
        return redirect(url_for('login'))

@app.route('/user-mangement')
def usermanagement():
    if 'admin' in session:
        users = userdetails.query.all()
        return render_template('user-management.html',user=users)
    else:
        return redirect(url_for('adminlogin'))


@app.route('/user-mangement/<deluser>')
def deletuser(deluser):
    if 'admin' in session:
        user = userdetails.query.get(deluser)
        if user:
            db.session.delete(user)
            db.session.commit()
            flash(f"{deluser} remove sucessfully")
            return redirect(url_for('usermanagement'))
        return jsonify({'success': False, 'error': 'User not found'}), 404
    else:
        return redirect(url_for('adminlogin'))


@app.route('/delarticle/<delarticle>')
def deletarticle(delarticle):
    if 'admin' in session:
        articles = article.query.filter_by(article_no=delarticle).first()
        if articles:
            db.session.delete(articles)
            db.session.commit()
            flash(f"article {delarticle} remove sucessfully")
            return redirect(url_for('viewallarticle'))
        return jsonify({'success': False, 'error': 'User not found'}), 404
    else:
        return redirect(url_for('adminlogin'))

#search opotion

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search_query']  # Get the search query from the form data
        items = userdetails.query.filter(userdetails.username.ilike(f'%{search_query}%')).all()  # Use the search query in the filter
        return render_template('user-management.html', items=items)  # Pass the search results to the template
    return render_template('user-management.html',items=[])


@app.route('/adminprofile')
def adminprofile():
    if "admin" in session:
        admin=session["admin"]
        print(admin)
        user_username=admindetails.query.filter_by(adminname=admin).first()
        return render_template("admin-profile.html",adminname=user_username.adminname,name=user_username.name,phone_no=user_username.phone_no,email=user_username.email)
    else:
        return redirect(url_for("signup"))

@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
    if 'admin' in session:
        session.pop('admin')
    return redirect(url_for('login'))
#user page and admin page

@app.route('/viewallarticle')
def viewallarticle():
    articles = article.query.all()
    if('admin' in session):
        return render_template('adminviewarticle.html',role="admin",articles=articles)
    elif('user' in session):
        return render_template('adminviewarticle.html',role="user",articles=articles)

#user pages
@app.route('/')
def getstart():
    return render_template('getstart.html')
@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=="POST":
        username=request.form["username"]
        name=request.form["name"]
        surename=request.form["surename"]
        phone_no=request.form["phone_no"]
        email=request.form["email"]
        address=request.form["address"]
        city=request.form["city"]
        state=request.form["state"]
        password=request.form["password"]
        userdetail=userdetails(username=username,name=name,surename=surename,phone_no=phone_no,email=email,address=address,city=city,state=state,password=password)
        db.session.add(userdetail)
        db.session.commit()
        return render_template("signup-page.html")
    else:
        return render_template('signup-page.html')


@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        login_username=request.form["username"]
        login_password=request.form["password"] 
        session["user"]=login_username
        print(login_username,login_password)
        user=userdetails.query.filter_by(username=login_username).first()
        print(user)
        if user:
            if user.password==login_password:
                print("login sucessfully")
                flash(f"Login Successful! Welcome back to our platform.")
                return redirect(url_for("home"))
            else:
                flash(f"We're sorry, but the username or password you entered is incorrect. Please double-check your credentials and try again.")
                print("We're sorry, but the username or password you entered is incorrect")
                return redirect("login")
        else :
            flash(f"We couldn't find an account registered with the provided credentials. Please make sure you've entered the correct information or consider signing up for an account.")
            return redirect("login")
    else:
        return render_template("loginpage.html")


@app.route('/home')
def home():
    if "user" in session:
        max_article1 = article.query.order_by(article.article_no.desc()).first()
        max_article2= article.query.order_by(article.article_no.desc()).offset(2-1).first()
        max_article3=article.query.order_by(article.article_no.desc()).offset(3-1).first()
        return render_template('home.html',role="user",max1=max_article1.article_no,max2=max_article2.article_no,max3=max_article3.article_no,article1_title=max_article1.article_title,article1_abstraction=max_article1.article_abstraction,article2_title=max_article2.article_title,article2_abstraction=max_article2.article_abstraction,article3_title=max_article3.article_title,article3_abstraction=max_article3.article_abstraction)
    else:
        return redirect(url_for("login"))

@app.route('/about')
def about():
    if "user" in session:
        user=session["user"]
        return render_template('aboutus.html',user=user)
    else:
        return render_template('aboutus.html')

@app.route('/user-profile')
def userprofile():   
    if "user" in session:
        user=session["user"]
        print(user)
        user_username=userdetails.query.filter_by(username=user).first()
        return render_template("User-profile.html",user=user_username.username,username=user_username.username,password=user_username.password,name=user_username.name,surename=user_username.surename,phone_no=user_username.phone_no,email=user_username.email,address=user_username.address,city=user_username.city,state=user_username.state)
    else:
        return redirect(url_for("signup"))

@app.route('/contactus',methods=["GET","POST"])
def contactus():
    if "user" in session:
        if request.method=="POST":
            name=request.form["name"]
            Email=request.form["email"]
            content=request.form["message"]
            print(name,Email,content)
            msg=Message(f"{name} Feedback",sender="yukeshvip2003@gmail.com",recipients=[Email])
            msg.body=content
            mail.send(msg)

        return render_template('contactus.html')
    else:
        return redirect(url_for("login"))

@app.route('/tree_counting',methods=["GET","POST"])
def tree_count():
    if "user" in session:
        if request.method=="POST":
            file=request.files["image"]
            latitude=request.form["latitude"]
            longitude=request.form["longitude"]
            print(latitude,longitude)
            filename=secure_filename(file.filename)
            if filename:
                print(filename)
                #image_path=filename
                file.save(os.path.join(app.config['UPLOAD'], filename))
                img = os.path.join(app.config['UPLOAD'], filename)
                 
                total_trees=predict(img)
                check=treecounting.query.filter_by(latitude=latitude, longitude=longitude).first()
                if(check):
                    print("changed",check)
                    check.tree_count=total_trees
                    db.session.commit() 
                else:
                    print("Not Changed")
                    db.session.add(treecounting(latitude=latitude, longitude=longitude ,tree_count=total_trees))
                    db.session.commit()
                greenspace=greenland(img,filename)
                print(img)
                return render_template("tree_count.html",count=total_trees,filename=filename)
            else:
                flash("Oops! It looks like you forgot to upload an image. Please select an image and click the 'Process' button to view the summary report.")
                return redirect(url_for("tree_count"))

        else:
            return render_template("tree_count.html")
    else:
        return redirect(url_for("login"))    

@app.route('/tree_species',methods=['GET','POST'])
def tree_species():
    if "user" in session:
        if request.method=="POST":
            file=request.files["image"]
            filename=secure_filename(file.filename)
            if filename:
                print(filename)
                image_path=filename
                file.save(os.path.join(app.config['UPLOAD'], filename))
                img = os.path.join(app.config['UPLOAD'], filename)
                species,report,confidence=species_indenti(img,filename)
                confidence=[round(x,2) for x in confidence] 
                print(species[0],report)
                result=[]
                if(report==1):
                    species_detail=statistics.query.filter(statistics.Tree_Species.ilike(f'%{species[0]}%')).all()
                    bot_response = species_detail
                    return render_template("tree_species.html",filename=filename,fact=bot_response[0].Intresting_fact,eco=bot_response[0].Ecological_role,phy=bot_response[0].Physical_Charateristics,despription0=bot_response[0].Species_Description,species=species[0],filename2=filename,response=report)
                elif(report==2):
                    return render_template("tree_species.html",filename2=filename,response=report,species=species or "species name",filename=filename,confidence=confidence)

                    
                
            else:
                flash("Oops! It looks like you forgot to upload an image. Please select an image and click the 'Process' button to view the summary report.")
                return redirect(url_for("tree_species"))
        else:
            return render_template("tree_species.html")
    else:
        return redirect(url_for("login"))
@app.route('/comparewithexisting',methods=['GET','POST'])
def comparewithexist():
    try:
        if "user" in session:
            if request.method=="POST":
                file=request.files["image"]
                latitude = request.form["latitude"]
                longitude = request.form["longitude"]
                filename=secure_filename(file.filename)
                if filename:
                    print(filename)
                    res=treecounting.query.filter_by(latitude=latitude, longitude=longitude).first()
                    if res:
                        file.save(os.path.join(app.config['UPLOAD'], filename))
                        img = os.path.join(app.config['UPLOAD'], filename)
                        total_trees=predict(img)
                        greenspace=greenland(img,filename)
                        print(img)
                        return render_template("comparewith.html",previouscount=res.tree_count,presentcount=total_trees,filename=filename)
                    else:
                        flash("The specified area is not found in our database. Please verify the tree count in the Tree Enumeration tab to ensure accuracy.")
                        return redirect(url_for('comparewithexist'))
                else:
                    flash("Oops! It looks like you forgot to upload an image. Please select an image and click the 'Process' button to view the summary report.")
                    return redirect(url_for("comparewithexist"))
            else:    
                return render_template('comparewith.html')
        else:
            return redirect(url_for('login'))
    except:
        return"please recheck image formate 404"
@app.route('/greenlandspace',methods=['GET','POST'])
def space():

        if "user" in session:
            if request.method=="POST":
                file=request.files["image"]
                filename=secure_filename(file.filename)
                if filename:
                    print(filename)
                    file.save(os.path.join(app.config['UPLOAD'], filename))
                    img = os.path.join(app.config['UPLOAD'], filename)
                    green,land=greenland(img,filename)
                    print(green,land)
                    bot_response = greencover.query.filter_by(green_percentage=round(green)).first()
                    print(bot_response)
                    return render_template("greenlandspace.html",greenpercentage=round(green),landpercentage=round(land),filename=filename,bot=bot_response.green_description,rec=bot_response.green_recommentation)
                else:
                    flash("Oops! It looks like you forgot to upload an image. Please select an image and click the 'Process' button to view the summary report.")
                    return redirect(url_for("space"))
            else:
                return render_template('greenlandspace.html')
        else:
            return redirect(url_for('login'))



@app.route('/useredirprofile/<user>',methods=['POST','GET'])
def editprofile(user):

    user_username=userdetails.query.filter_by(username=user).first()
    if request.method=='POST':
        name=request.form["name"]
        surename=request.form["surename"]
        phone_no=request.form["phone_no"]
        email=request.form["email"]
        address=request.form["address"]
        city=request.form["city"]
        state=request.form["state"]
        print(name)
        user_username.name=name
        user_username.surename=surename
        user_username.phone_no=phone_no
        user_username.email=email
        user_username.address=address
        user_username.city=city
        user_username.state=state
        db.session.commit()
        flash("User Profile Updated Sucessfully")
        return redirect(url_for('userprofile'))
    return render_template('User-Profile.html',flage='edit',user=user_username.username,username=user_username.username,password=user_username.password,name=user_username.name,surename=user_username.surename,phone_no=user_username.phone_no,email=user_username.email,address=user_username.address,city=user_username.city,state=user_username.state)



# Mobile ApI routes

@app.route('/apisignup',methods=['POST','GET'])
def apisignup():
    if request.method=="POST":
        username=request.form["username"]
        name=request.form["name"]
        surename=request.form["surename"]
        phone_no=request.form["phone_no"]
        email=request.form["email"]
        address=request.form["address"]
        city=request.form["city"]
        state=request.form["state"]
        password=request.form["password"]
        user_exits=userdetails.query.filter_by(username=username).first()
        if(user_exits):
            return jsonify({'message':False,'status':"User Already exists"})
        else:    
            userdetail=userdetails(username=username,name=name,surename=surename,phone_no=phone_no,email=email,address=address,city=city,state=state,password=password)
            db.session.add(userdetail)
            db.session.commit()
        return jsonify({'message':True})
    else:
        return render_template('signup-page.html')

@app.route('/apilogin',methods=['POST','GET'])
def apilogin():
    user_agent = request.headers.get('User-Agent')
    print(user_agent)
    if 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent or 'okhttp' in user_agent:
        if request.method=='POST':
            login_username=request.form["login_username"]
            login_password=request.form["login_password"] 
            session["user"]=login_username
            print(login_username,login_password)
            user=userdetails.query.filter_by(username=login_username).first()
            print(user)
            if user:
                if user.password==login_password:
                    print("login sucessfully")
                    
                    return jsonify({'message':True,'username':user.username})
                else:
                    flash(f"We're sorry, but the username or password you entered is incorrect. Please double-check your credentials and try again.")
                    return jsonify({'message':False})
            else :
                flash(f"We couldn't find an account registered with the provided credentials. Please make sure you've entered the correct information or consider signing up for an account.")
                return jsonify({'message':False})
    else:
        return "Mobile User"
    

@app.route('/apihome')
def apihome():
        user_agent = request.headers.get('User-Agent')
        print(user_agent)
        if 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent or 'okhttp' in user_agent:
            max_article1 = article.query.order_by(article.article_no.desc()).first()
            max_article2= article.query.order_by(article.article_no.desc()).offset(2-1).first()
            max_article3=article.query.order_by(article.article_no.desc()).offset(3-1).first()
            json={'max1':max_article1.article_no,'max2':max_article2.article_no,'max3':max_article3.article_no,'article1_title':max_article1.article_title,'article1_abstraction':max_article1.article_abstraction,'article2_title':max_article2.article_title,'article2_abstraction':max_article2.article_abstraction,'article3_title':max_article3.article_title,'article3_abstraction':max_article3.article_abstraction}
            return jsonify(json)
        else:
            return "Mobile User"
    

@app.route('/apiuserprofile/<user>')
def apiuserprofile(user):
    user_agent = request.headers.get('User-Agent')
    print(user_agent)
    if 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent or 'okhttp' in user_agent:   
        print(user)
        user_username=userdetails.query.filter_by(username=user).first()
        json={'user':user_username.username,'username':user_username.username,'password':user_username.password,'name':user_username.name,'surename':user_username.surename,'phone_no':user_username.phone_no,'email':user_username.email,'address':user_username.address,'city':user_username.city,'state':user_username.state}
        return jsonify(json)
    else:
        return "mobile user"

@app.route('/apitree_counting',methods=["GET","POST"])
def apitree_count():
    user_agent = request.headers.get('User-Agent')
    print(user_agent)
    if 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent or 'okhttp' in user_agent:
        if request.method=="POST":
            file=request.files["image"]
            latitude=request.form["latitude"]
            longitude=request.form["longitude"]
            filename=secure_filename(file.filename)
            if filename:
                print(filename)
                image_path=filename
                file.save(os.path.join(app.config['UPLOAD'], filename))
                img = os.path.join(app.config['UPLOAD'], filename)
                total_trees=predict(img)
                check=treecounting.query.filter_by(latitude=latitude, longitude=longitude).first()
                if(check):
                    check.tree_count=total_trees
                    db.session.commit() 
                else:
                    db.session.add(treecounting(latitude=latitude, longitude=longitude, tree_count=total_trees))
                    db.session.commit()
                greenspace=apigreenland(img,filename)
                print(img)
                json={'count':total_trees,'filename':filename}
                return jsonify(json)
            else:
                
                return jsonify({'error':'Oops! It looks like you forgot to upload an image. Please select an image and click the Process button to view the summary report.'})

        else:
            return render_template("tree_count.html")
    else:
        return "Mobile User"


@app.route('/image/<filename>')
def apidisplay_img(filename):
    return send_from_directory('static/greenspace', filename)

@app.route('/species/<filename>')
def apispecies_display_img(filename):
    return send_from_directory('static/species', filename)

@app.route('/articleimage/<filename>')
def apiarticle_display_img(filename):
    return send_from_directory('static/adminuploads', filename)


@app.route('/apitree_species',methods=['GET','POST'])
def apitree_species():
    user_agent = request.headers.get('User-Agent')
    print(user_agent)
    if 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent or 'okhttp' in user_agent:
        if request.method=="POST":
            file=request.files["image"]
            filename=secure_filename(file.filename)
            if filename:
                print(filename)
                image_path=filename
                file.save(os.path.join(app.config['UPLOAD'], filename))
                img = os.path.join(app.config['UPLOAD'], filename)
                species,report,confidence=species_indenti(img,filename)
                confidence=[round(x,2) for x in confidence] 
                print(species[0],report)
                result=[]
                if(report==1):
                    
                    species_detail=statistics.query.filter(statistics.Tree_Species.ilike(f'%{species[0]}%')).all()
                    
                    jsontext1={'description':species_detail[0].Species_Description,'physical':species_detail[0].Physical_Charateristics,'ecological':species_detail[0].Ecological_role,'species':species[0],'fact':species_detail[0].Intresting_fact,'filename':filename,'response':report}
                    print(jsonify(jsontext1))
                    return jsonify(jsontext1)
                elif(report==2):
                    if(len(species)>=3):
                        species1=species[0]
                        confidence1=confidence[0]
                        species2=species[1]
                        confidence2=confidence[1]
                        species3=species[2]
                        confidence3=confidence[2]
                    elif(len(species)==2):
                        species1=species[0]
                        confidence1=confidence[0]
                        species2=species[1]
                        confidence2=confidence[1]
                        species3="Not Found"
                        confidence3="Not Found"
                    elif(len(species)==1):
                        species1=species[0]
                        confidence1=confidence[0]
                        species2="Not Found"
                        confidence2="Not Found"
                        species3="Not Found"
                        confidence3="Not Found"
                    else:
                        species1="Not Found"
                        confidence1="Not Found"
                        species2="Not Found"
                        confidence2="Not Found"
                        species3="Not Found"
                        confidence3="Not Found"
                    jsontext2={'filename':filename,'response':report,'species1':species1,'species3':species3,'species2':species2,'confidence1':confidence1,'confidence2':confidence2,'confidence3':confidence3}
                    return jsonify(jsontext2)

                    
                
            else:
                flash("Oops! It looks like you forgot to upload an image. Please select an image and click the 'Process' button to view the summary report.")
                return redirect(url_for("tree_species"))
        else:
            return render_template("tree_species.html")
    else:
        return "Mobile user"
    
@app.route('/apicomparewithexisting',methods=['GET','POST'])
def apicomparewithexist(): 
    user_agent = request.headers.get('User-Agent')
    print(user_agent)
    if 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent or 'okhttp' in user_agent:
        if request.method=="POST":
            file=request.files["image"]
            latitude=request.form["latitude"]
            longitude=request.form["longitude"]
            filename=secure_filename(file.filename)
            if filename:
                print(filename)
                res=treecounting.query.filter_by(latitude=latitude, longitude=longitude).first()
                print(res)
                if res:
                    file.save(os.path.join(app.config['UPLOAD'], filename))
                    img = os.path.join(app.config['UPLOAD'], filename)
                    total_trees=predict(img)
                    greenspace=apigreenland(img,filename)
                    print(img)
                    josntext={"Message":True,"Status":"Image Predict Sucessfully","previouscount":res.tree_count,"presentcount":total_trees,"filename":filename}
                    return jsonify(josntext)
                else:
                    return jsonify({"Message":False,"Status":"This area is not added in Tree eumneration Database"})
            else:
                return redirect(url_for('comparewithexist'))
        else:
                return render_template("comparewith.html")
    else:
        return "Mobile User"
    
@app.route('/apigreenlandspace',methods=['GET','POST'])
def apispace():
    user_agent = request.headers.get('User-Agent')
    print(user_agent)
    if 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent or 'okhttp' in user_agent:
            if request.method=="POST":
                file=request.files["image"]
                filename=secure_filename(file.filename)
                if filename:
                    print(filename)
                    file.save(os.path.join(app.config['UPLOAD'], filename))
                    img = os.path.join(app.config['UPLOAD'], filename)
                    green,land=apigreenland(img,filename)
                    print(round(green),round(land))

                    bot_response = greencover.query.filter_by(green_percentage=round(green)).first()
                    print(bot_response)
                    josontext={'greenpercentage':round(green),'landpercentage':round(land),'filename':filename,'bot':bot_response.green_description,'recommentation':bot_response.green_recommentation}
                    return jsonify(josontext)
                else:
                    
                    return jsonify({'message':False,'username':'Fail'})
    else:
        return "Mobile User"   
    
    
@app.route('/apiuseredirprofile/<user>',methods=['POST','GET'])
def apieditprofile(user):
    user_agent = request.headers.get('User-Agent')
    print(user_agent)
    if 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent or 'okhttp' in user_agent:    
        if request.method=='POST':
            user_username=userdetails.query.filter_by(username=user).first()
            name=request.form["name"]
            surename=request.form["surename"]
            phone_no=request.form["phone_no"]
            email=request.form["email"]
            address=request.form["address"]
            city=request.form["city"]
            state=request.form["state"]
            print(name)
            user_username.name=name
            user_username.surename=surename
            user_username.phone_no=phone_no
            user_username.email=email
            user_username.address=address
            user_username.city=city
            user_username.state=state   
            db.session.commit()
            return jsonify({'message':True,'username':user_username.username})
    else:
        return "Mobile User"


@app.route('/apiviewallarticle')
def apiviewallarticle():
    user_agent = request.headers.get('User-Agent')
    print(user_agent)
    if 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent or 'okhttp' in user_agent:
        articles = article.query.all()
        article_list=[{
            "articleTitle":i.article_title,
            "articleAbstraction":i.article_abstraction,
            "filename":i.article_filename,
            "publishDate":i.article_date,
            "articleid":i.article_no
        } for i in articles
        ] 
        return jsonify({"articles":article_list, "status":True})
    else:
        return "Mobile User"

@app.route('/apilogout')
def apilogout():
    user_agent = request.headers.get('User-Agent')
    print(user_agent)
    if 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent or 'okhttp' in user_agent:
        return jsonify({'message':True})
    else:
        return "Mobile User"

@app.route('/apiarticle/<name>')
def apiarticlepage(name):
    user_agent = request.headers.get('User-Agent')
    print(user_agent)
    if 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent or 'okhttp' in user_agent:
        max_article1=article.query.filter_by(article_no=name).first()
        json={'articel_title':max_article1.article_title,'article_domain':max_article1.article_domain,'article_date':max_article1.article_date,'article_subtitle':max_article1.article_subtitle,'article_abstraction':max_article1.article_abstraction,'article_maincontent':max_article1.article_maincontent,'article_conclusion':max_article1.article_conculsion,'filename':max_article1.article_filename}
        return jsonify(json)
    else:
        return "Mobile User"


with app.app_context():
    db.create_all()
if(__name__=="__main__"):
    app.run(host='0.0.0.0', port=5050, debug=True)