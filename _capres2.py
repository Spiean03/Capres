import socket
import sys
import time
import _defines as d


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#class CapresControl():
#
#    def __init__(self, host, port, retryAttempts=10 ):
#        #this is the constructor that takes in host and port. retryAttempts is given 
#        # a default value but can also be fed in.
#        self.host = d.DEFAULT_HOST
#        self.port = d.DEFAULT_PORT
#        self.retryAttempts = retryAttempts
#        self.socket = None
#
#    def _connect(self, attempt=0):
#        if attempt<self.retryAttempts:
#            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#            sock.connect(("192.168.1.80", 23))
#        if connectionFailed:
#            self.connect(attempt+1)
#
#    def _diconnect_socket(self):
#        #perform all breakdown operations
#        sock.shutdown(1)
#        sock.close()
#        self.socket = None
#
#    def read_data(self):
#        #read data here
#        time.sleep(50.0 / 1000.0)
#        while True:
#            if self.socket is None:
#                self.connect()
#                
#
#    def send_current(self, data):
#        sock.sendall(bytes("\r" + ""))

class CapresControl():

    def __init__(self, sock=None):
        self.host = d.DEFAULT_HOST
        self.port = d.DEFAULT_PORT
        
        
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        
#        try:
#            self.sock.connect((d.DEFAULT_HOST, d.DEFAULT_PORT))
#        except socket.error as msg:
#            print("Socket Error: %s" % msg)
#        except TypeError as msg:
#            print("Type Error: %s" % msg)
            

    def _connect(self):
        try:
            self.sock.connect((d.DEFAULT_HOST, d.DEFAULT_PORT))
        except socket.error as msg:
            print("Socket Error: %s" % msg)
        except TypeError as msg:
            print("Type Error: %s" % msg)
    
#    def _accept(self):
#        self.accept = socket.socket.accept()
#        try:
#            self.accept
#        except socket.error as msg:
#            print("Socket Error: %s" % msg)
#        except TypeError as msg:
#            print("Type Error: %s" % msg)
        
            
#    def _send(self, message):
#        try:
#            # Connect to server and send data
#            sock.connect((d.DEFAULT_HOST, d.DEFAULT_PORT))
#            sock.sendall(bytes(message + "\r" + ""))
#            # Receive data from the server and shut down
#            print("Sent: " + message + ". Status: ok")
#            self.message = message
#        except (socket.error, TypeError) as msg:
#            print("Couldn't send command: " + message +" Error: %s" % msg)
#        finally:
#            print("close socket")
#            #sock.close()
#        time.sleep(50.0 / 1000.0)
        
        
    # _setcurrent is the command to set the current correctly. it accepts values between 50pA and 1mA 
    # all values for example 1uA, 1u, 1E-6, 0.000001 are accepted
    def _setcurrent(self,current): 
        #self._connect()
        #this deletes 'Amperes' from the input and converts p,n,u and m in numbers
        if 'A' in current:
            current = current.replace('A', '')
        elif 'p' in current:
            current = current.replace('p', 'E-12')
        elif 'n' in current:
            current = current.replace('n', 'E-9')
        elif 'u' in current:
            current = current.replace('u', 'E-6')
        elif 'm' in current:
            current = current.replace('m', 'E-3')
        else:
            current = current
        
        # to make sure that the entered value is a number
        try:
            current = float(current)
        except ValueError:
            print("Current parameter is not a number")
        
        # if the entered value is a number and between 50pA and 1mA, send the command
        if isinstance(current, float) == False:
            print("Current parameter is not a number")
        elif current >= 1E-3:
            print ("Value out of range 50pA-1mA")
        elif current <= 50E-12:
            print ("Value out of range 50pA-1mA")
        else:
            self.currentsend = current
            try:
                # Connect to server and send data
                sock.connect((self.host, self.port))
                sock.send("i" + str(self.currentsend) + "\r" + "")
                time.sleep(50.0 / 1000.0)
                # Receive data from the server and shut down
                self.globalcurrentread = sock.recv(512)
                self.currentread = self.globalcurrentread[self.globalcurrentread.find("#C ")+3:self.globalcurrentread.find(" V")]
                print("current ok")
            except (socket.error, TypeError) as msg:
                print("setcurrent doesnt work. Message: %s" %msg) 
            finally:
                #sock.shutdown(2)
                #sock.close()
                time.sleep(1)
                print("socket closed")
      
    # _setgain is the command to set the gain correctly. it accepts only the values in the list acceptedgainvalues
    # if the value got accepted, it sends it to the controller
    def _setgain(self,gain):      
        acceptedgainvalues = {'1','2','4', '8', '16', '32', '64', '100', '200', '400', '800', '1600', '3200', '6400', '12800', '25600', '51200', '102800', '204800', '409600'}
        
        if gain in acceptedgainvalues:
            print("valid gain")
            self.gainsend = gain
            try:
                # Connect to server and send data
                sock.connect((self.host, self.port))
                sock.send("g" + str(self.gainsend) + "\r" + "")
                time.sleep(50.0 / 1000.0)
                # Receive data from the server and shut down
                self.globalgainread = sock.recv(512)
                self.gainread = self.globalgainread[self.globalgainread.find("Gain=")+5:self.globalgainread.find("  Gout=")]
                print("setgain ok")
                print(self.gainread)
            except (socket.error, TypeError) as msg:
                    print("setgain doesnt work. Message: %s" %msg)             
            finally:
                #sock.shutdown(2)
                #sock.close() 
                print("socket closed")
        else:
            print("gain value not acceptable")
     
    # To perform a measurement and to get i, A, P, R, Ain, VEc, VSA, VSA, VSc, C and D back     
    def _getmeasurement(self):
        print("get measurement")
        try:
            sock.connect((d.DEFAULT_HOST, d.DEFAULT_PORT))
            sock.sendall(bytes("v1" + "\r" + ""))
            time.sleep(50.0 / 1000.0)
            # Receive data from the server and shut down
            self.globalgetmeasurement = sock.recv(512)
            string = self.globalmeasurement
            
            self.i = string[string.find("i=")+2:string.find(" A=")]
            self.A = string[string.find("A=")+2:string.find(" P=")]
            self.P = string[string.find("P=")+2:string.find(" R=")]
            self.R = string[string.find("R=")+2:string.find(" Ain")]
            self.Ain = string[string.find("Ain ")+4:string.find(" VEc=")]
            self.VEc = string[string.find("VEc=")+4:string.find(" VSA=")]
            self.VSA = string[string.find(" VSA=")+5:string.find(" VSc=")]
            self.VSc = string[string.find(" VSc=")+5:string.find(" C=")]
            self.C = string[string.find("C=")+2:string.find(" D")]
            self.D = string[string.find(" D")+2:]
            print("getmeas ok")
        except (socket.error, TypeError) as msg:
            print("getmeasurement doesnt work. Message: %s" %msg)    
        finally:
            #sock.shutdown(1)
            #sock.close()
            print("socket closed")

    def _setrshunton(self):
        self.message = "rs1"
        try:
            sock.connect((d.DEFAULT_HOST, d.DEFAULT_PORT))
            sock.sendall(bytes("rs1" + "\r" + ""))
            time.sleep(50.0 / 1000.0)
            # Receive data from the server and shut down
            self.rshunt = sock.recv(512)
            if "R shunt on" in self.rshunt:
                self.rshunt = "on"
            elif "R shunt off" in self.rshunt:
                self.rshunt = "off"
            else:
                print("neither R shunt on nor off")
        except (socket.error, TypeError) as msg:
            print("rshunton doesnt work. Message: %s" %msg) 
        finally:
            print(self.rshunt)
            #sock.shutdown(1)            
            #sock.close()
            print("socket closed")
           
    
    def _setrshuntoff(self):
        try:
            sock.connect((d.DEFAULT_HOST, d.DEFAULT_PORT))
            sock.sendall(bytes("rs0" + "\r" + ""))
            time.sleep(50.0 / 1000.0)
            # Receive data from the server and shut down
            self.rshunt = sock.recv(512)
            if "R shunt on" in self.rshunt:
                self.rshunt = "on"
            elif "R shunt off" in self.rshunt:
                self.rshunt = "off"
            else:
                print("neither R shunt on nor off")
        except (socket.error, TypeError) as msg:
            print("setrshuntoff doesnt work. Message: %s" %msg) 
        finally:
            print(self.rshunt)
            #sock.shutdown(1)
            #sock.close()
            print("socket closed")
             
    
    def _settriggeron(self):
        try:
            sock.connect((d.DEFAULT_HOST, d.DEFAULT_PORT))
            sock.sendall(bytes("t" + "\r" + ""))
            time.sleep(50.0 / 1000.0)
            # Receive data from the server and shut down
            self.trigger = sock.recv(512)
            self.triggermessage = "Trigger on"
        except (socket.error, TypeError) as msg:
            print("settriggeron doesnt work. Message: %s" %msg) 
        finally:
            print(self.triggermessage)
            #sock.shutdown(1)            
            #sock.close()
            print("socket closed")
        
    def _settriggeroff(self):
        try:
            sock.connect((d.DEFAULT_HOST, d.DEFAULT_PORT))
            sock.sendall(bytes("t" + "\r" + ""))
            time.sleep(50.0 / 1000.0)
            # Receive data from the server and shut down
            self.trigger = sock.recv(512)
            self.triggermessage = "Trigger off"
        except (socket.error, TypeError) as msg:
            print("settriggeroff doesnt work. Message: %s" %msg) 
        finally:
            print(self.triggermessage)
            #sock.shutdown(1)
            #sock.close() 
            print("socket closed")
    
    def _setvsensegain(self, vsensegain):
        acceptedvsensegainvalues = {'1','100'}
        
        if vsensegain in acceptedvsensegainvalues:
            print("valid gain")
            
            if vsensegain == "1":
                self.vsensegain = vsensegain
                self.vsensegainsend = "g0"
                try:
                    # Connect to server and send data
                    sock.connect((d.DEFAULT_HOST, d.DEFAULT_PORT))
                    sock.sendall(bytes(self.vsensegainsend + "\r" + ""))
                    time.sleep(50.0 / 1000.0)
                    # Receive data from the server and shut down
                    self.vsensegainread = sock.recv(512)
                    print(self.vsensegainread)
                except (socket.error, TypeError) as msg:
                    print("Vsensegain doesnt work. Message: %s" %msg)     
                finally:
                    #sock.shutdown(1)
                    #sock.close() 
                    print("socket closed")
                
            elif vsensegain == "100":
                self.vsensegain = vsensegain
                self.vsensegainsend = "g2"
                try:
                    # Connect to server and send data
                    sock.connect((d.DEFAULT_HOST, d.DEFAULT_PORT))
                    sock.sendall(bytes(self.vsensegainsend + "\r" + ""))
                    time.sleep(50.0 / 1000.0)
                    # Receive data from the server and shut down
                    self.vsensegainread = sock.recv(512)
                    print(self.vsensegainread) 
                except (socket.error, TypeError) as msg:
                    print("Vsensegain doesnt work. Message: %s" % msg)   
                finally:
                    #sock.shutdown(1)
                    #sock.close() 
                    print("socket closed")
            else:
                print("There went something wrong with setting the Vsense gain level to either 1 or 100")
            
        else:
            print("Gain value for VSense not acceptable")       

    def _getvsense(self):
        try:
            sock.connect((d.DEFAULT_HOST, d.DEFAULT_PORT))
            sock.sendall(bytes("s" + "\r" + ""))
            time.sleep(50.0 / 1000.0)
            # Receive data from the server and shut down
            self.getglobalvsense = sock.recv(512)
            print(self.getglobalvsense)
        except (socket.error, TypeError) as msg:
            print("getvsense doesnt work. Message: %s" % msg)
        finally:
            #sock.shutdown(1)
            #sock.close() 
            print("socket closed")
    
    def _setmultiplexdefault(self):
        try:
            sock.connect((d.DEFAULT_HOST, d.DEFAULT_PORT))
            sock.sendall(bytes("mus" + "\r" + ""))
            time.sleep(50.0 / 1000.0)
            # Receive data from the server and shut down
            self.getglobalmultiplexdefault = sock.recv(512)
            print(self.getglobalmultiplexdefault)
        finally:
            print("socket closed")
            #sock.close() 
    def _setmultiplexreset(self):
        try:
            sock.connect((d.DEFAULT_HOST, d.DEFAULT_PORT))
            sock.sendall(bytes("muc" + "\r" + ""))
            time.sleep(50.0 / 1000.0)
            # Receive data from the server and shut down
            self.getglobalmultiplexreset = sock.recv(512)
            print(self.getglobalmultiplexreset)
        finally:
            print("socket closed")
            #sock.close() 
    def _setmultiplexallground(self):
        try:
            sock.connect((d.DEFAULT_HOST, d.DEFAULT_PORT))
            sock.sendall(bytes("muc" + "\r" +"muxd2s" + "\r" +"muxd3s" + "\r" + "muxd10s" + "\r" + "muxd11s" + "\r" ""))
            time.sleep(50.0 / 1000.0)
            # Receive data from the server and shut down
            self.getglobalmultiplexallground = sock.recv(512)
            print(self.getglobalmultiplexallground)
        finally:
            print("socket closed")
            #sock.close() 
    
    def _setmultiplex(self, probename, probevalue, probestatus):
        
        acceptedprobes = {'P1','P2', 'P3', 'P4'}
        acceptedprobevalue = {'Iout', 'Vplus', 'Vminus', 'GND'}
        acceptedprobestatus = {'on', 'off'}
       
        if probename in acceptedprobes:
            if probevalue in acceptedprobevalue:
                if probestatus in acceptedprobestatus:
                    if probename == 'P1':
                        setprobe = '2'
                    elif probename == 'P2':
                        setprobe = '3'
                    elif probename == 'P3':
                        setprobe = '10'
                    else:
                        setprobe = '11'
                    if probevalue == 'Iout':
                        setprobevalue = 'a'
                    elif probevalue == 'Vplus':
                        setprobevalue = 'b'
                    elif probevalue == 'Vminus':
                        setprobevalue = 'c'
                    else:
                        setprobevalue = 'd'
                    if probestatus == 'on':
                        setprobestatus = 's'
                    else:
                        setprobestatus = 'c'
                    
                    self.setmultiplex = 'mux'+ setprobevalue + setprobe  + setprobestatus
                    print self.setmultiplex
                    
                    try:
                        # Connect to server and send data
                        sock.connect((d.DEFAULT_HOST, d.DEFAULT_PORT))
                        sock.sendall(bytes(str(self.setmultiplex) + "\r" + ""))
                        time.sleep(50.0 / 1000.0)
                        # Receive data from the server and shut down
                        self.globalmultiplexread = sock.recv(1024)
                        #print(self.globalmultiplexread)
                        self.multiplexread = self.globalmultiplexread[self.globalmultiplexread.find("Mux data"):self.globalmultiplexread.find("Mux data")+20]
                        print(self.multiplexread)
                    finally:
                        print "socket closed"
                        #sock.close()  
                else:
                    print("Probe status"+probestatus+"for probe not recognised. Use 'on' and 'off' to determine what you want.")
                
            else:    
                print("Probe value "+probevalue+" not valid to set probe to new status. Use 'Iout', 'Vplus', 'Vminus' and 'GND'")
        else:
            print("Probe name " +probename+ " not valid to set probe to new status. Use 'P1', 'P2', 'P3' and 'P4'")

    def _setfrequency(self,frequency):
         
        acceptedfrequency = {'1.5Hz','3.1Hz', '6.1Hz', '12.2Hz','24.4Hz', '48.8Hz', '97.7Hz', '195.3Hz', '390.6Hz','781.3Hz', '1562.5Hz'}
        if frequency in acceptedfrequency:
            if frequency == '1.5Hz':
                frequencyvalue = 'f14'
            elif frequency == '3.1Hz':
                frequencyvalue = 'f13'
            elif frequency == '6.1Hz':
                frequencyvalue = 'f12'
            elif frequency == '12.2Hz':
                frequencyvalue = 'f11'
            elif frequency == '24.4Hz':
                frequencyvalue = 'f10'
            elif frequency == '48.8Hz':
                frequencyvalue = 'f9'
            elif frequency == '97.7Hz':
                frequencyvalue = 'f8'
            elif frequency == '195.3Hz':
                frequencyvalue = 'f7'
            elif frequency == '390.6Hz':
                frequencyvalue = 'f6'
            elif frequency == '781.3Hz':
                frequencyvalue = 'f5'
            else:
                frequencyvalue = 'f4'
            
            self.frequencyvalue = frequencyvalue
            try:
                # Connect to server and send data
                sock.connect((d.DEFAULT_HOST, d.DEFAULT_PORT))
                sock.sendall(bytes(str(self.frequencyvalue) + "\r" + ""))
                time.sleep(50.0 / 1000.0)
                # Receive data from the server and shut down
                self.globalfrequencyread = sock.recv(1024)
                print(self.globalfrequencyread)
                #self.multiplexread = self.globalmultiplexread[self.globalmultiplexread.find("Mux data"):self.globalmultiplexread.find("Mux data")+20]
            finally:
                print "socket closed"
                #sock.close()  

        else:
            print("The value ' + frequency = ' is not accepted by the controller. Valid frequencies: '1.5Hz','3.1Hz', '6.1Hz', '12.2Hz','24.4Hz', '48.8Hz', '97.7Hz', '195.3Hz', '390.6Hz','781.3Hz' and '1562.5Hz'.")
        
    def _setintegrationtime(self,integrationtime):
        acceptedtimevalues = {'82ms', '164ms', '320ms', '660ms', '1.31s', '2.62s', '5.24s', '10.48s'}
        
        if integrationtime in acceptedtimevalues:
            if integrationtime == '82ms':
                integrationvalue = 'j0'
            elif integrationtime == '164ms':
                integrationvalue = 'j1'
            elif integrationtime == '320ms':
                integrationvalue = 'j2'
            elif integrationtime == '660ms':
                integrationvalue = 'j3'  
            elif integrationtime == '1.31s':
                integrationvalue = 'j4' 
            elif integrationtime == '2.62s':
                integrationvalue = 'j5'  
            elif integrationtime == '5.24s':
                integrationvalue = 'j6'                 
            else:
                integrationvalue = 'j7'
            
            self.integrationvalue = integrationvalue
            try:
                # Connect to server and send data
                sock.connect((d.DEFAULT_HOST, d.DEFAULT_PORT))
                sock.sendall(bytes(str(self.integrationvalue) + "\r" + ""))
                time.sleep(50.0 / 1000.0)
                # Receive data from the server and shut down
                self.globalintegrationtimeread = sock.recv(1024)
                print(self.globalintegrationtimeread)
                #self.multiplexread = self.globalmultiplexread[self.globalmultiplexread.find("Mux data"):self.globalmultiplexread.find("Mux data")+20]
            finally:
                print "socket closed"
                #sock.close()                    
        else:
            print("The inserted Integration time of "+integrationtime+" is not valide. Valid times: '82ms', '164ms', '320ms', '660ms', '1.31s', '2.62s', '5.24s' and '10.48s'.")
    
    def _overloadlevel(self,overloadlevel):
       
        if 'V' in overloadlevel:
            overloadlevel = overloadlevel.replace('V', '')
        else:
            overloadlevel = overloadlevel
        
        try:
            overloadlevel = float(overloadlevel)
            print(overloadlevel)
            if overloadlevel % 0.1 == 0:
                print("value accepted")
            else:
                test = round(overloadlevel,1)
                print(test)
                print("you can only put values from 0 to 10V in with smallest increment of 100mV")
                
            
        except ValueError:
            print("OverloadLevel parameter is not a number")

        
        
        
        
        

        
         
        
#    def mysend(self, msg):
#        totalsent = 0
#        while totalsent < MSGLEN:
#            sent = self.sock.send(msg[totalsent:])
#            if sent == 0:
#                raise RuntimeError("socket connection broken")
#            totalsent = totalsent + sent
#
#    def myreceive(self):
#        chunks = []
#        bytes_recd = 0
#        while bytes_recd < MSGLEN:
#            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
#            if chunk == '':
#                raise RuntimeError("socket connection broken")
#            chunks.append(chunk)
#            bytes_recd = bytes_recd + len(chunk)
#        return ''.join(chunks)                
#                
#import socket
#import sys
#import time
#
#HOST, PORT = "192.168.1.80", 23
#data1 = "i1E-6"
#data2 = "g1"
#data3 = "mus"
#data4 = "f14"
#data5 = "v1"
#
## Create a socket (SOCK_STREAM means a TCP socket)
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#
#try:
#    # Connect to server and send data
#    sock.connect((HOST, PORT))
#    sock.sendall(data1 + "\r" + "")
#    time.sleep(50.0 / 1000.0)
#    # Receive data from the server and shut down
#    received1 = sock.recv(512)
#finally:
#    print "works"
#   #sock.close()
#
#print("Sent:     {}".format(data1))
#print("Received: {}".format(received1))
#
#time.sleep(1)
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#try:
#    # Connect to server and send data
#    sock.connect((HOST, PORT))
#    sock.sendall(bytes(data2 + "\r" + ""))
#    time.sleep(50.0 / 1000.0)
#    # Receive data from the server and shut down
#    received2 = str(sock.recv(512))
#finally:
#    print "works"
#    #sock.close()
#
#print("Sent:     {}".format(data2))
#print("Received: {}".format(received2))
#
#time.sleep(1)
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#try:
#    # Connect to server and send data
#    sock.connect((HOST, PORT))
#    sock.sendall(bytes(data3 + "\r" + ""))
#    time.sleep(50.0 / 1000.0)
#    # Receive data from the server and shut down
#    received3 = str(sock.recv(512))
#finally:
#    print "works"    
#    #sock.close()
#
#print("Sent:     {}".format(data3))
#print("Received: {}".format(received3))
#
#time.sleep(1)
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#try:
#    # Connect to server and send data
#    sock.connect((HOST, PORT))
#    sock.sendall(bytes(data4 + "\r" + ""))
#    time.sleep(50.0 / 1000.0)
#    # Receive data from the server and shut down
#    received4 = str(sock.recv(512))
#finally:
#    print "works"
#    #sock.close()
#
#print("Sent:     {}".format(data4))
#print("Received: {}".format(received4))
#
#time.sleep(1)
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#try:
#    # Connect to server and send data
#    sock.connect((HOST, PORT))
#    sock.sendall(bytes(data5 + "\r" + ""))
#    time.sleep(50.0 / 1000.0)
#    # Receive data from the server and shut downhg
#    received5 = str(sock.recv(512))
#finally:
#    sock.shutdown(1)
#    sock.close()
#
#print("Sent:     {}".format(data5))
#print("Received: {}".format(received5))
#
#string = received5
#
#i = string[string.find("i=")+2:string.find(" A=")]
#A = string[string.find("A=")+2:string.find(" P=")]
#P = string[string.find("P=")+2:string.find(" R=")]
#R = string[string.find("R=")+2:string.find(" Ain")]
#Ain = string[string.find("Ain ")+4:string.find(" VEc=")]
#VEc = string[string.find("VEc=")+4:string.find(" VSA=")]
#VSA = string[string.find(" VSA=")+5:string.find(" VSc=")]
#VSc = string[string.find(" VSc=")+5:string.find(" C=")]
#C = string[string.find("C=")+2:string.find(" D")]
#D = string[string.find(" D")+2:string.find("\n\r")]
#D = D.replace("\n", "").replace("\r", "").replace(" ","")
#
#print "i=" +i, "A=" +A, "P="+P,"R="+R,"Ain="+Ain,"VEc="+VEc,"VSA="+VSA, "VSc="+VSc,"C="+C,"D="+D

#CapresControl()._connect()
#sock.connect((d.DEFAULT_HOST, d.DEFAULT_PORT))
#sock.shutdown(1)
#sock.close()
c = CapresControl()

#c._connect()
#c._setcurrent("0.000000015")
#print(c.currentsend)
#print(c.globalcurrentread)
#print("Current = " + c.currentread)
#sock.shutdown(2)
#sock.close()

#c._setfrequency("24.41Hz")
#c._setintegrationtime('10.48s')
c._overloadlevel("1.25V")
##print(c.gainsend)
##print("Gain = " + c.globalgainread)
#
#time.sleep(1)
##c._setrshuntoff()
#
##c._setrshunton()
#time.sleep(1)
##c._settriggeron()
#time.sleep(1)
##c._settriggeroff()
#
##c._setvsensegain("1")
#time.sleep(1)
##c._getvsense()
#
#
#
#c._setgain("100") 
#
sock.shutdown(2)
sock.close()


#try:
#    sock.connect((d.DEFAULT_HOST, d.DEFAULT_PORT))
#except socket.error , msg:
#    print 'Bind failed. Error code: ' + str(msg[0]) + 'Error message: ' + msg[1]
#    sys.exit()
#print 'Socket bind complete'
#while True:
#    command = raw_input('Enter your command: ')
#    if command == "quit":
#        break
#    else:
#        socket.send(command)
#        time.sleep(0.1)
#        receive = socket.recv(1024)



