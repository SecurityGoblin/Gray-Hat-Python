import my_debugger

debugger = my_debugger.debugger()

pid = raw_input("enter the PID of the process to attach to: ")

#debugger.load(b"C:\\WINDOWS\\system32\\calc.exe")

debugger.attach(int(pid))

debugger.dettach()
