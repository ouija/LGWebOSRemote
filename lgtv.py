
import sys
import os
import json
from inspect import getfullargspec
from LGTV import LGTVScan, LGTVClient, getCommands

os.system('clear')
print ("LGWebOSRemote [@ouija fork / original script by Karl Lattimer]")

def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def usage(error=None):
    if error:
        print ("Error: " + error)
    print ("Usage: lgtv <command> [parameter]\n")
    print ("Available Commands:")

    print ("  scan")
    print ("  auth                  Hostname/IP    Authenticate and exit, creates initial config ~/.lgtv.json")

    for c in getCommands(LGTVClient):
        print ("  " + c, end=" ")
        print (" " * (20 - len(c)), end=" ")
        args = getfullargspec(LGTVClient.__dict__[c])
        print (' '.join(args.args[1:-1]))


def parseargs(command, argv):
    args = getfullargspec(LGTVClient.__dict__[command])
    args = args.args[1:-1]

    if len(args) != len(argv):
        raise Exception("Argument lengths do not match")

    output = {}
    for (i, a) in enumerate(args):
        #
        # do some basic conversions for bools, ints and floats
        #
        if argv[i].lower() == "true":
            argv[i] = True
        elif argv[i].lower() == "false":
            argv[i] = False
        try:
            f = int(argv[i])
            argv[i] = f
        except:
            try:
                f = float(argv[i])
                argv[i] = f
            except:
                pass
        output[a] = argv[i]
    return output

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage("Too few arguments")
    elif sys.argv[1] == "notificationWithURL": #or sys.argv[1] == "notificationWithIcon":
        if len(sys.argv) < 4:
            usage("message and url required for {0}".format(sys.argv[1]))
        elif not which("ffmpeg") or not which("base64") and sys.argv[1] == "notificationWithURL":
            usage("ffmpeg or base64 NOT found and required for {0}".format(sys.argv[1]))
        else:
            try:
                ws = LGTVClient()
                try:
                    args = parseargs(sys.argv[1], sys.argv[2:])
                except Exception as e:
                    usage(e.message)
                ws.connect()
                ws.exec_command(sys.argv[1], args)
                ws.run_forever()
            except KeyboardInterrupt:
                ws.close()
    elif sys.argv[1] == "scan":
        results = LGTVScan()
        if len(results) > 0:
            print (json.dumps({
                "result": "ok",
                "count": len(results),
                "list": results
            }))
        else:
            print (json.dumps({
                "result": "failed",
                "count": len(results)
            }))
    elif sys.argv[1] == "on":
        ws = LGTVClient()
        ws.on()
    elif sys.argv[1] == "auth":
        if len(sys.argv) < 3:
            usage("Hostname or IP is required for auth")
        ws = LGTVClient(sys.argv[2])
        ws.connect()
        ws.run_forever()
    else:
        try:
            ws = LGTVClient()
            try:
                args = parseargs(sys.argv[1], sys.argv[2:])
            except Exception as e:
                usage(e.message)
            ws.connect()
            ws.exec_command(sys.argv[1], args)
            ws.run_forever()
        except KeyboardInterrupt:
            ws.close()
