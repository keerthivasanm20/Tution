from django.shortcuts import render,redirect
import pyrebase

#from win10toast import ToastNotifier

config = {
  "apiKey": "AIzaSyB0o1nitaAVdZah346pksYqbMC41c9pqt0",
  "authDomain": "studentactivitymaintence.firebaseapp.com",
  "databaseURL": "https://studentactivitymaintence.firebaseio.com",
  "projectId": "studentactivitymaintence",
  "storageBucket": "studentactivitymaintence.appspot.com",
  "messagingSenderId": "64618605497",
  "appId": "1:64618605497:web:9cdd5d310a3b878e022468",
  "measurementId": "G-RB67K33HC5"
}

firebase=pyrebase.initialize_app(config)
auth1 = firebase.auth()
database=firebase.database()





def sam(request):
    l='keerthi,kiara,ava,kimberely,sherlock'
    return render(request,'slider.html',{'d':l})  
    # hr =ToastNotifier()
     #hr.show_toast("Alarm","someone Hacked da boi",icon_path="static/images/apple.jpg")
def sighin(request):
    
     return render(request,'sign.html')
def val(request):
     if request.method == 'GET':
          c=request.GET['sample']
         
          print(c[0])
     print(c)
     return render(request,'slider.html',{'c':c})
def demo(request):
     if request.method == 'GET':
          c=request.GET["sample"]
          print(c)
          print('poo')
          return render(request,'slider.html',{'s':'alert'})
               
     else:
          return render(request,'demo.html')

def logged(request):



     email = request.POST.get('email')
     password = request.POST.get('password')
     try :
         user = auth1.sign_in_with_email_and_password(email,password)
     except :
          msg = "invalid"
          return render(request,'image_views.html',{"msg":msg})
     session_id=user['idToken']
     request.session['uid']=str(session_id)

     return render(request,"image_views.html",{'er':'avlo'})
     
     
def logout(request):
       try:
            del request.session['uid']
       except KeyError:
            pass
       return render(request,"index.html")


def presignup(request):
     return render(request,"signup.html")
def signup(request):
     name = request.POST.get('name')
     email=request.POST.get('email')
     password=request.POST.get('pass')
     #creating  user with email and password 
     print(name)
     print(password)
     try:
         user=auth1.create_user_with_email_and_password(email,password)
     except:
          mg="Weak identity"
          return render(request,'popup.html',{'er','er'})
     
     
     uid = user['localId']
     
    
     idtoken = request.session['uid']
     
     data={
          "name":name,"status":"1"
     }
     #pushing of data
     database.child("users").child(uid).child("details").set(data,idtoken)
     return render(request,'popup.html')
def create(request):
      return render(request,"create.html")
def postcreate(request):
     #simple to convert the current area time into the milliseconds
     import time
     from datetime import datetime, timezone
     import pytz
     
     tz = pytz.timezone('Asia/Kolkata')
     time_now=datetime.now(timezone.utc).astimezone(tz)
     millis=int(time.mktime(time_now.timetuple()))
     #console.log("time stamp :"+str(millis)) 
     work = request.POST.get('work')
     pro = request.POST.get('progress')
     url=request.POST.get('url')
     data={

               'work':work,
               'progress':pro,
               'url':url,
     }
     try:
          idtoken=request.session['uid']
          a = auth1.get_account_info(idtoken)
               
          # getting timestamp and local id

          a = a['users']
          a=a[0]
          a = a['localId']
          #console.log(a)
          
          #pushing into the firebase 
          database.child('users').child(a).child('reports').child(millis).set(data,idtoken)
          name =database.child('users').child(a).child('details').child('name').get(idtoken).val()
          return render(request,"user_home.html") 
     except KeyError:
            mg="User Logged out please sign in again"
            return render(request,'popup.html',{'msg':mg}) 



def check(request):
          import datetime
          idtoken=request.session['uid']
          a = auth1.get_account_info(idtoken)
               
          # getting timestamp and local id

          a = a['users']
          a=a[0]
          a = a['localId']
          #to fetch the time stamps and to fetch each record
          timestamps=database.child('users').child(a).child('reports').shallow().get(idtoken).val()
          lis_tim=[]
          for i in timestamps:
               lis_tim.append(i)
          
          lis_tim.sort(reverse=True)
          work =[]
          progr=[]
          img=[]
          date=[]
          for i in lis_tim:
               work.append(database.child('users').child(a).child('reports').child(i).child('work').get(idtoken).val())
               progr.append(database.child('users').child(a).child('reports').child(i).child('progress').get(idtoken).val())
               img.append(database.child('users').child(a).child('reports').child(i).child('url').get(idtoken).val())
          for i in lis_tim:
               i=float(i)
               # to get current time 1.import time 2.then time.strftime('%H:%M:%s')
               dat=datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
               date.append(dat)
          for i in date:
                dic=zip(lis_tim,date,work,progr,img)
          name =database.child('users').child(a).child('details').child('name').get(idtoken).val()
          return render(request,'check.html',{'dic':dic,'e':name})




