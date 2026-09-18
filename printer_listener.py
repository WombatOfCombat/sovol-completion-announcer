import time,requests,serial

printerDataSource="http://<printer IP>:<moonraker port>/printer/objects/query?print_stats="
stateBank=["standby","standby"]
idle=True

print("[printer_listener] starting up",flush=True)


while True:
    try:
        print(f"[printer_listener] polling {printerDataSource}",flush=True)
        response=requests.get(printerDataSource,timeout=10)
        print(f"[printer_listener] http status={response.status_code}",flush=True)
        data=response.json()["result"]["status"]["print_stats"]["state"]
        print(f"[printer_listener] printer state read = '{data}'",flush=True)

        if data not in ["standby","complete"]:
            idle=False
            print("[printer_listener] idle set False (printer not in standby and turned on)",flush=True)

        stateBank[0]=stateBank[1]
        stateBank[1]=data
        print(f"[printer_listener] stateBank now = {stateBank}",flush=True)

        if stateBank[0]!="standby" and stateBank[1]=="standby":
            print("[printer_listener] transition detected: printing -> standby",flush=True)
            #TODO here put your code to execute upon printer completion
            pass
            idle=True
            print("[printer_listener] idle set True (print complete, notified)",flush=True)

    except requests.exceptions.ConnectionError as e:
        print(f"[printer_listener] ERROR: connection error reaching printer: {e}",flush=True)
        idle=True
        print("[printer_listener] idle set True (connection error)",flush=True)

    except requests.exceptions.Timeout as e:
        print(f"[printer_listener] ERROR: request to printer timed out: {e}",flush=True)

    except (KeyError, ValueError) as e:
        print(f"[printer_listener] ERROR: unexpected/malformed JSON response: {e}",flush=True)

    except Exception as e:
        print(f"[printer_listener] ERROR: unhandled exception: {type(e).__name__}: {e}",flush=True)

    sleep_for=30 if idle else 1
    print(f"[printer_listener] sleeping for {sleep_for}s (idle={idle})",flush=True)
    time.sleep(sleep_for)
