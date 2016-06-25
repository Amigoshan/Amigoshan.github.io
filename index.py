#####################################################################
# This is the main project module
# Created on: 9 March 2011
# Author: Amigo
# Description:
#####################################################################

#!/usr/local/bin/python

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
from threading import Thread
import urllib2
from urllib2 import URLError

class MyThread(Thread):

    def __init__(self,seconds,action):
        self.action = action
        Thread.__init__(self,seconds)

    def run(self):
        Thread.run(self)
        self.action()

#########################################################
# Set device setting
#########################################################
def set_device(deviceID,url,powerState,deviceName):
    # import the needed libraries
    # the URL of the XML file 
    xbee_addr = deviceID

    if deviceID == "":
        deviceID = "00000000-00000000-00409DFF-FF43E79A"
        xbee_addr = deviceID

    if url == "":
        url = 'http://developer.idigi.com/ws/sci'

#<data><device name="smart_plug_1"><channel_set name="power_on" value="%s"/></device></data>
#<data><channel_set device="smart_plug_1" name="power_on" value="%s"/></data>
#<data><channel_set><device name="smart_plug_1"><channel name="power_on" value="%s"/></device></channel_set></data>

    SCI_REQUEST = """
        <sci_request version="1.0">
        <send_message>
        <targets>
        <device id="%s"/>
        </targets>
        <rci_request version="1.1">
        <do_command target="idigi_dia">
        <data><channel_set name="%s" value="%s"/></data>
        </do_command>
        </rci_request>
        </send_message>
        </sci_request>""" % (deviceID,deviceName,powerState)

#    if (debug_mode == "debug"):
#        print "<hr />"
#        print "Debug output from web services SCI Request:<br>"
#        temp_new_settings = SCI_REQUEST
#        temp_new_settings = temp_new_settings.replace ( '<', '&lt;' )
#        temp_new_settings = temp_new_settings.replace ( '>', '&gt;' )
#        print temp_new_settings
#        print "<hr />"        
#        print "<br>"
    # create a password manager with the username and password
    pswdMgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    pswdMgr.add_password(None, url, username, password)

    # create an authentication handler
    authHandler = urllib2.HTTPBasicAuthHandler(pswdMgr)

    # create an opener and install it
    opener = urllib2.build_opener(authHandler)
    urllib2.install_opener(opener)
    headers = {'Content-Type' : 'text/xml'}

    request = urllib2.Request(url, SCI_REQUEST, headers)

    # try opening the URL and thrown an exception if it's not found
    try:
        response = urllib2.urlopen(request)
        #print response.read()
        return response.read()
    except URLError, e:
        print e.reason
        sys.exit(1)
    
    # Now fetch again after sleep for a few seconds to let the sensors
    # settle down. Experimental stuff!!!
    c = MyThread(5,get_device_info(deviceID,url))
    c.start()

form = cgi.FieldStorage()

#global tempdeviceID
#global tempurl
#global username
#global password
#global deviceID
#global url
tempdeviceID = form.getvalue("deviceID", "")
tempurl = form.getvalue("url", "")
username = form.getvalue("username", "")
password = form.getvalue("password", "")
On1 = form.getvalue("led1","")
On2 = form.getvalue("led2","")
On3 = form.getvalue("led3","")
direction = form.getvalue("derection","")
# You need to translate the deviceID to upper case - else it won't be found!
deviceID = tempdeviceID.upper()
url = tempurl
if url.startswith('http://')==False and url!="":
    url='http://'+url

# if the user checks the default deviceID box, use Amigo's gateway
default_deviceID = form.getvalue("default_deviceID","")
if (len(default_deviceID) > 1):
    deviceID = default_deviceID
default_url = form.getvalue("default_url","")
if (len(default_url) > 1):
    url = default_url
#
# Also make sure the user has provided credentials before calling the get_device_info function
InputVariablesComplete = True
if len(deviceID) < 1:
    InputVariablesComplete = False
if len(url) < 1:
    InputVariablesComplete = False
if len(username) < 1:
    InputVariablesComplete = False
if len(password) < 1:
    InputVariablesComplete = False
if (InputVariablesComplete):
    # If the user requested setting the power state, make that request via RCI
    if (On1 == "On"):
        new_settings = set_device(deviceID,url,True,'xbib0.led1')
    else:
        if (On1 == "Off"):
            new_settings = set_device(deviceID,url,False,'xbib0.led1')
    if (On2 == "On"):
        new_settings = set_device(deviceID,url,True,'xbib0.led2')
    else:
        if (On2 == "Off"):
            new_settings = set_device(deviceID,url,False,'xbib0.led2')
    if (On3 == "On"):
        new_settings = set_device(deviceID,url,True,'xbib0.led3')
    else:
        if (On3 == "Off"):
            new_settings = set_device(deviceID,url,False,'xbib0.led3')
    if (direction == "Forward"):
        new_settings = set_device(deviceID,url,'Forward#','xbib0.write') 
    elif (direction == "Backward"):
        new_settings = set_device(deviceID,url,'Backward#','xbib0.write') 
    elif (direction == "Left"):
        new_settings = set_device(deviceID,url,'Left#','xbib0.write') 
    elif (direction == "Right"):
        new_settings = set_device(deviceID,url,'Right#','xbib0.write') 
    elif (direction == "RaiseLeftArm"):
        new_settings = set_device(deviceID,url,'RaiseLeftArm#','xbib0.write') 
    elif (direction == "RaiseRightArm"):
        new_settings = set_device(deviceID,url,'RaiseRightArm#','xbib0.write')
    elif (direction == "DropLeftArm"):
        new_settings = set_device(deviceID,url,'DropLeftArm#','xbib0.write')
    elif (direction == "DropRightArm"):
        new_settings = set_device(deviceID,url,'DropRightArm#','xbib0.write')
    else:
        pass
    #Shot the picture
    new_settings = set_device(deviceID,url,'Shot#','xbib0.write')
# Start creating the output html        
print "Content-type: text/html"
print

print """
<html>
<head>
<title>Ubiquitous Robotics Platform</title>
</head>

<BODY BGCOLOR="#ffffff" TOPMARGIN=0 TEXT="#000000" LINK="#0000FF" VLINK="purple" ALINK="#ff0000">
<TABLE BORDER=0 CELLSPACING="0" CELLPADDING="0" ALIGN="center" BGCOLOR="#FFFFFF">
<tr>
  <td height=20></td>
</tr>
<tr>
  <td><img src="resources/image/sjtulogo.jpg" width=100 height=100></td>
  <td width=801 height=100>
    <font color=#0b4da2 face="Australian Sunrise" size=6>Research institute of Robotics<br></font>
    <font color=#285572 face="Australian Sunrise" size=6>Shanghai Jiaotong University,Supported by YASKAWA<br></font>
  <td><img src="resources/image/yaskawalogo.jpg" width=100 height=100></td>
</tr>
<tr>
  <td height=5></td>
</tr>
<tr>
  <td colspan=3 align="center" bgcolor="#ffffff"><img src="resources/image/banner.jpg" width=1000></td>
</tr>
<tr>
  <td colspan=3 align="right" bgcolor="#ffffff" background="resources/image/bar.jpg" width=1000 height=27>
    <font color=#285572 face="Arial"  size=3>login&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</font>
  </td>
</tr>
<tr>
  <td height=5></td>
</tr>
</table>
<table BORDER=0 CELLSPACING="0" CELLPADDING="0" ALIGN="center" BGCOLOR="#FFFFFF">
  <tr>
    <td bgcolor=#aec3d0 width=15 height=1000> </td>
    <td width=685 height=1000>
      <table BORDER=0 CELLSPACING="0" CELLPADDING="0" ALIGN="top" BGCOLOR="#FFFFFF">
        <tr>
          <td rowspan=2 bgcolor=#aec3d0><font color=#7b8095 face="Arial"  size=4><b>&nbsp&nbsp;Device&nbsp&nbsp</b></font></td>
          <td colspan=2 width=300 height=30></td>
        </tr>
        <tr>
          <td height=3 bgcolor=#aec3d0></td>
        </tr>
      </table>
      <iframe height=302 width=680 frameborder=0 src ="
"""
str='test.py?deviceID='+deviceID+'&url='+url+'&username='+username+'&password='+password
print str

print"""
      ">
        <p>Your browser does not support iframes.</p>
      </iframe>
  <form method="post" action="index.py">
    <table border='0' cellspacing='1'cellpadding='0' align='center'>
      <tr valign=bottom>
"""
if (On1=="On"):
    str1="checked"
    str2=""
else:
    str1=""
    str2="checked"
print"  <td width=100><input type='radio' name='led1' value='On' %s/><font color=#3c3b66 face='Arial' size=2> On </font><br>" % str1
print"      <input type='radio' name='led1' value='Off' %s/><font color=#3c3b66 face='Arial' size=2> Off </font></td>" %str2
if (On2=="On"):
    str1="checked"
    str2=""
else:
    str1=""
    str2="checked"
print"  <td width=100><input type='radio' name='led2' value='On' %s/><font color=#3c3b66 face='Arial' size=2> On </font><br>" %str1
print"      <input type='radio' name='led2' value='Off' %s/><font color=#3c3b66 face='Arial' size=2> Off </td>" %str2
if (On3=="On"):
    str1="checked"
    str2=""
else:
    str1=""
    str2="checked"
print"  <td width=100><input type='radio' name='led3' value='On' %s/><font color=#3c3b66 face='Arial' size=2> On </font><br>" %str1
print"      <input type='radio' name='led3' value='Off' %s/><font color=#3c3b66 face='Arial' size=2> Off </font></td>" %str2
print"""  <td width=100>
          <input type="submit" value="&nbsp;OK&nbsp"/>
        <td width=100></td>
        <td width=100></td>
      </tr>
      <tr>
        <td height=35></td>
      </tr>
    </table>
"""#  </form>


print"""
      <table BORDER=0 CELLSPACING="0" CELLPADDING="0" ALIGN="top" BGCOLOR="#FFFFFF">
        <tr>
          <td rowspan=2 bgcolor=#aec3d0><font color=#7b8095 face="Arial"  size=4><b>&nbsp&nbsp;Virtual Robots&nbsp&nbsp</b></font></td>
          <td colspan=2 width=237 height=30></td>
        </tr>
        <tr>
          <td height=3 bgcolor=#aec3d0></td>
        </tr>
      </table>
      <table BORDER=0 CELLSPACING="0" CELLPADDING="0" ALIGN="top" BGCOLOR="#FFFFFF">
        <tr>
          <td height=300>
            <table BORDER=0 CELLSPACING=0 CELLPADDING=0 ALIGN="top" BGCOLOR="#FFFFFF">
              <tr>
                <td width=50>
                </td>
                <td width=130><img src="resources/image/SmartPal5.jpg"></td>
                <td width=100>
"""
print"            <input type='radio' name='derection' value='Forward' "
if (direction=='Forward'):
    print "checked"
print"/><font color=#3c3b66 face='Arial' size=2> Forward </font><br>"
print"            <input type='radio' name='derection' value='Backward' "
if (direction=='Backward'):
    print "checked"
print"/><font color=#3c3b66 face='Arial' size=2> Backward </font><br>"
print"            <input type='radio' name='derection' value='Left' "
if (direction=='Left'):
    print "checked"
print"/><font color=#3c3b66 face='Arial' size=2> Left </font><br>"
print"            <input type='radio' name='derection' value='Right' "
if (direction=='Right'):
    print "checked"
print"/><font color=#3c3b66 face='Arial' size=2> Right </font><br>"
print"""          </td>
                <td width=130>
    """
print"            <input type='radio' name='derection' value='RaiseLeftArm' "
if (direction=='RaiseLeftArm'):
    print "checked"
print"/><font color=#3c3b66 face='Arial' size=2> Raise Left Arm </font><br>"
print"            <input type='radio' name='derection' value='DropLeftArm' "
if (direction=='DropLeftArm'):
    print "checked"
print"/><font color=#3c3b66 face='Arial' size=2> Drop Left Arm </font><br>"
print"            <input type='radio' name='derection' value='RaiseRightArm' "
if (direction=='RaiseRightArm'):
    print "checked"
print"/><font color=#3c3b66 face='Arial' size=2> Raise Right Arm </font><br>"
print"            <input type='radio' name='derection' value='DropRightArm' "
if (direction=='DropRightArm'):
    print "checked"
print"/><font color=#3c3b66 face='Arial' size=2> Drop Right Arm </font><br>"
    
print"""
                </td>
                <td>
                  <input type="submit" value="&nbsp;OK&nbsp"/>
                </td>
				<td width=130><img src="resources/image/SoccorRobot.jpg">
				</td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
      <table BORDER=0 CELLSPACING="0" CELLPADDING="0" ALIGN="top" BGCOLOR="#FFFFFF">
        <tr>
          <td rowspan=2 bgcolor=#aec3d0><font color=#7b8095 face="Arial"  size=4><b>&nbsp&nbsp;User Command&nbsp&nbsp</b></font></td>
          <td colspan=2 width=226 height=30></td>
        </tr>
        <tr>
          <td height=3 bgcolor=#aec3d0></td>
        </tr>
      </table>
      <table BORDER=0 CELLSPACING="0" CELLPADDING="0" ALIGN="top" BGCOLOR="#FFFFFF">
        <tr>
          <td height=200>
            <font color=#3c3b66 face='Arial' size=3>
              &nbsp&nbsp&nbsp&nbsp;<a href="Location.html" target="_blank">View Robot Location</a><br><br>
              &nbsp&nbsp&nbsp&nbsp;<a href="">Robot Meet Guest</a><br><br>
              &nbsp&nbsp&nbsp&nbsp;<a href="">Move to Table</a><br><br>
            </font>
          </td>
          <td width=50>
          </td>
          <td>
            <iframe height=210 width=273 frameborder=0 src = "shotImg.py">
              <p>Your browser does not support iframes.</p>
            </iframe>
          </td>
          <td width=50>
          </td>
          <td>
            <input type="submit" value="Shot"/>
          </td>
        </tr>
      </table>
    </td>
    <td align="center" valign="top" bgcolor="#ffffff" background="resources/image/rightpanelbg.jpg" width=300 height=1000>
    <br>
      <table BORDER=0 CELLSPACING="0" CELLPADDING="0" ALIGN="center" BGCOLOR="#e8ecf0">
        <tr>
          <td rowspan=3 width=10></td>
          <td align="center" valign="bottom" width=230><font color=#7b8095 face="Arial" size=5>Configuration</font></td>
          <td rowspan=3 width=10></td>
        </tr>
        <tr>
          <td align="center"><hr size=2 width=210 color=#aec3d0></td>
        </tr>
        <tr>
          <td height=270 width=230>
"""
#          <form method="post" action="index.py">
print"""            <font color=#54869b face="Arial" size=4>Device ID: </font>
            <input type="text" name="deviceID" size=30 value="%s"/><br>
            <input type="checkbox" name="default_deviceID" value="00000000-00000000-00409DFF-FF43E79A">
            <font color=#a27eab face="Arial" size=2>00000000-00000000-00409DFF-FF43E79A</font><br>
            <font color=#54869b face="Arial" size=4>URL: </font>
            <input type="text" name="url" size=30 value="%s"/><br>
            <input type="checkbox" name="default_url" value="http://developer.idigi.com/ws/sci">
            <font color=#a27eab face="Arial" size=2>http://developer.idigi.com/ws/sci</font><br>
            <font color=#54869b face="Arial" size=4>Username: </font>
            <input type="text" name="username" size=20 value="%s"/><br>
            <font color=#54869b face="Arial" size=4>Password: </font><br>
            <input type="password" name="password" size=20 value="%s"/><br><br>&nbsp
            <input type="submit" value="&nbsp&nbsp;OK&nbsp&nbsp"/>&nbsp&nbsp&nbsp&nbsp
            <input type="reset" value="&nbsp;Reset&nbsp"/></br></form>
""" % (deviceID, url, username, password)

#deviceID = '00000000-00000000-'+deviceID

print"""
          </td>
        </tr>
      </table>
      <br><br>
      <table BORDER=0 CELLSPACING="0" CELLPADDING="0" ALIGN="center" BGCOLOR="#e8ecf0">
         <tr>
           <td align="center" valign="bottom"><font color=#7b8095 face="Arial" size=5>Broacast</font></td>
         </tr>
         <tr>
           <td align="center"><hr size=2 width=230 color=#aec3d0></td>
         </tr>
         <tr><td>
           <MARQUEE scrollAmount=1 direction=up height=170 width=250>
            <table width="100%" border="0" cellspacing="0" cellpadding="3">
              <tr>
                <td width="13%" height="25" align="center" valign="top"><img src="resources/image/dice.jpg" width="5" height="5" vspace="8" /></td>
                <td width="87%"><font color=#b87e78 face="Arial"  size=3>Platform Version1.0 has been released.</font></td>
              </tr>
              <tr>
                <td width="13%" height="25" align="center" valign="top"><img src="resources/image/dice.jpg" width="5" height="5" vspace="8" /></td>
                <td width="87%"><font color=#b778b8 face="Arial"  size=3>Complete the divice info, and then click the OK button, the device imformation will be shown at left.</font></td>
              </tr>
              <tr>
                <td width="13%" height="25" align="center" valign="top"><img src="resources/image/dice.jpg" width="5" height="5" vspace="8" /></td>
                <td width="87%"><font color=#b87e78 face="Arial"  size=3>Infame technique has been used, so that the device statment is changed every other seconds.</font></td>
              </tr>
              <tr>
                <td width="13%" height="25" align="center" valign="top"><img src="resources/image/dice.jpg" width="5" height="5" vspace="8" /></td>
                <td width="87%"><font color=#b778b8 face="Arial"  size=3>Click the button, you can change the position of the virtual robot.</font></td>
              </tr>
            </table>
          </MARQUEE>
        </td></tr>
      </table>
      <br><br>
      <table BORDER=0 CELLSPACING="0" CELLPADDING="0" ALIGN="center" BGCOLOR="#e8ecf0">
         <tr>
           <td align="center" valign="bottom"><font color=#7b8095 face="Arial" size=5>To be developed</font></td>
         </tr>
         <tr>
           <td align="center"><hr size=2 width=230 color=#aec3d0></td>
         </tr>
         <tr><td>
           <MARQUEE scrollAmount=1 direction=up height=170 width=250>
            <table width="100%" border="0" cellspacing="0" cellpadding="3">
              <tr>
                <td width="13%" height="25" align="center" valign="top"><img src="resources/image/dice.jpg" width="5" height="5" vspace="8" /></td>
                <td width="87%"><font color=#828267 face="Arial"  size=3>Password is deliverd between frame and inner frame, safty problem.</font></td>
              </tr>
              <tr>
                <td width="13%" height="25" align="center" valign="top"><img src="resources/image/dice.jpg" width="5" height="5" vspace="8" /></td>
                <td width="87%"><font color=#828267 face="Arial"  size=3>User login function.</font></td>
              </tr>
              <tr>
                <td width="13%" height="25" align="center" valign="top"><img src="resources/image/dice.jpg" width="5" height="5" vspace="8" /></td>
                <td width="87%"><font color=#828267 face="Arial"  size=3>Automatically configue the devices.</font></td>
              </tr>
              <tr>
                <td width="13%" height="25" align="center" valign="top"><img src="resources/image/dice.jpg" width="5" height="5" vspace="8" /></td>
                <td width="87%"><font color=#828267 face="Arial"  size=3>User command.</font></td>
              </tr>
            </table>
          </MARQUEE>
        </td></tr>
      </table>
      <br><br>
      <table BORDER=0 CELLSPACING="0" CELLPADDING="0" ALIGN="top" BGCOLOR="#e8ecf0">
        <tr>
          <td rowspan=3 width=10></td>
          <td align="center" valign="bottom" width=230><font color=#7b8095 face="Arial" size=3>Friendly Link</font></td>
          <td rowspan=3 width=10></td>
        </tr>
        <tr>
          <td height=50 width=230>
            <a href='http://robolab.sjtu.edu.cn'><font color=#576a65 face="Arial" size=2>Rescearch Institute of Robotics of Shanghai Jiaotong Universcity</font></a>
          </td>
        </tr>
      </table>
      
    </td>
  </tr>
  <tr>
    <td colspan=3 background="resources/image/bottom.jpg" width=1000 height=150>
      <center><font color=#557381 face="Freestyle Script"  size=6>(C) 2011. Amigo. SJTU Institute of Robotics. All rights reserved.<br>Shanghai Jiaotong Universcity<br>Recearch Institute of Robotics</font></center></td>
  </tr>
<tr>
  <td height=20></td>
</tr>
</table>

</body>

</html>
"""
