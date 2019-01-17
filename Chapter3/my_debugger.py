from ctypes import *
from my_debugger_defines import *

kernel32 = windll.kernel32

class debugger():
    def __init__(self):
        self.h_process  = None
        self.PID        = None
        self.debugger_active = False
    
    def load(self, path_to_exe):
        #dwCreation flag determines how to create the process
        #ie. creation_flag = CREATE_NEW_CONSOLE show the target GUI
        creation_flags = DEBUG_PROCESS

        #prepare the structures
        startupinfo =           STARTUPINFO()
        process_information =   PROCESS_INFORMATION()

        #The following allows the started process to be shown as a seperate window.
        startupinfo.dwFlags =       0x1
        startupinfo.wShowWindow =   0x0

        #Initializing cb variables in the startupinfo struct (which is the size of the struct itself)
        startupinfo.cb = sizeof(startupinfo)

        if kernel32.CreateProcessA( path_to_exe,
                                    None,
                                    None,
                                    None,
                                    None,
                                    creation_flags,
                                    None,
                                    None,
                                    byref(startupinfo),
                                    byref(process_information)):

            print("[*] Process launched successfully")
            print ("[*] PID: %d" % process_information.dwProcessId)

        else:
            print ("[*] Error: 0x%08x." % kernel32.GetLastError())

        def open_process(self, pid):

            h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, pid, False)
            return h_process

        def attach(self, pid):

            self.h_process = self.open_process(pid)

            #Attempt to attach to the process
            #If it fails, exit the call
            if kernel32.DebugActiveProcess(pid):
                self.debugger_active = True
                self.pid = int(pid)
                self.run()
            else:
                print "[*] Unable to attach to process"

        def run(self):
            #Now we poll the debuggee for debugging events

            while self.debugger_active == True:
                self.get_debug_event()

        def get_debug_event(self):

            debug_event = DEBUG_EVENT()
            continue_status = DBG_CONTINUE

            if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):

                raw_input("Press and key to continue...")
                self.debugger_active = False
                kernel32.ContinueDebugEvent(\
                    debug_event.dwProcessId, \
                    debug_event.dwThreadId, \
                    continue_status)
            
            def detach(self):
                if kernel32.DebugActiveProcessStop(self.pid):
                    print "[*] Finished debugging. Exiting..."
                    return True
                else:
                    print "Error"
                    return False

