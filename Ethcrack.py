from pyfiglet import Figlet
import os, random, codecs, time, threading
from bit.format import bytes_to_wif
from bit import Key
from colored import fg, attr

rick = """
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%%%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%%%%%%%##%%%%%%%%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%%##****++++++++**###%%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%%%%##+==--:::::::::. ::::--=+*#%%%@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@%%%%%##+=--:-:-------::::::::.:::.:::-=+#%%%%@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@%%%%##+-::::--::::::::::::-::::----:::  :::-=*%%%@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@%%%%#=-:::----::===========--=======---  -----:-+#%%%%@@@%%%@@@@@@@@@@
@@@@@@@@@@@@@@@@@@%%%%#=::::--:---==++++===================-:===:..---=#%%%%%%%%%@@@@@@@@@
@@@@@@@@@@@@@@@@%%%%#+------==+++++++++++++++++++++*@#*+===+%@+==-:==---+#%%%%%%%@@@@@@@@@
@@@@@@@@@@@@@@%%%%%*-::===+++++++++++===+++++++++++*@@@@#+#@@@#=====+==---+#%%%%%%%@@@@@@@
@@@@@@@@@@@@@%%%%#+:-.-=+++++++++++=-=++===++*#*+++#@@@@@@@@@@@**#%@+-----:=##%%%%%%@@@@@@
@@@@@@@@@@@%%%%%#=:-==++++++++++++-=++++++++++#@@@%@@@@@@@@@@@@@@@@#-==----:-*##%%%%%@@@@@
@@@@@@@@@@@%%%%#=:-==+=++++++++++=+++***++=+*++*@@@@@@@@@@@@@@@@@@@*+**+==-::-*##%%%%@@@@@
@@@@@@@@@@%%%%#=:-==++ .=++++++++++***+++==*###%%@@@@@@@@@@@@@@@@@@@%%%%%+--::-*#%%%%@@@@@
@@@@@@@@@@%%%#+:-==+++: -+++++++++**++====+*#@@@@@@@@@@@@@@@@@@@@@@@%%%*==--  :+##%%%@@@@@
@@@@@@@@%%%%%#-:-==+=:===+++++++**++===++=*+==*@@@@@@#***%@%-. :=@@@@@#=-=--:::-*#%%%@@@@@
@@@@@@@@%%%%#*::-====-===++++++**+===++*=+*##%@@@@@*     -@:     +@@@@%%#+=---::+#%%@@@@@@
@@@@@@@%%%%##=:..-==+++-=++++++*********++++*%@@@@@%#%@@@@@%#%%##%@%@@@%#**=--:.-#%%%@@@@@
@@@@@@%%%%%#*-.  .===+++-=++#%@@@@@@@@@@%*=====+#@@@@@@@@@@@@@@@@@@%@%*=-====-::-#%%%@@@@@
@@@@@@%%%%%#*-:..:-===++==%@@@@@@@@@@@@@@@@#++#@@@@@@@@@@@@@@@@@@@@%@@#+=====--:-#%%%@@@@@
@@@@@@@%%%%##-.:::-:-==+#@@@@@@@@@@@@@@@@@@@@*+##@@@@@@@@@@@@@@@@@%%@%%%*====--:-#%%%@@@@@
@@@@@@@%%%%%#=:::::::-=#@@@@@@@@@@@@@@@@@@@@@@%=#@@@@@@@@@@@@@@@@@#@%++=====--::=#%%@@@@@@
@@@@@@@%%%%%#+::::::::+@@@@@@@@@@@@@@@@@@@@@@@@+==#@@@@@@@@@@@@@@%%@@*+=====--::+#%%@@@@@@
@@@@@@@@%%%%#*-:::::::+@@@@@@@%*:#@@-=%@@@@@@@@%=*##@@@@@@@@@@@@%%++*++====--::-#%%@@@@@@@
@@@@@@@%%%%%#*=.:::-::*@@+...    :@*    ..::@@@@***+*#%@@@@@@%*==+=+++====:---:*#%@@@@@@@@
@@@@@@@%%%%%##*-:::-===@@#.     .#@%:      +@@@#*+=====%@@@@%+=----++====-.-::=#%%@@@@@@@@
@@@@@@@%%%%%%##+-::-==+@@@@#+++#@@@@@#===*%@@@@#+#%%%%%@@@@@%%%%##*++====---:=#%%@@@@@@@@@
@@@@@@@@%%%%%%##+-::--*@@@@@@@@@@@@@@@@@@@@@@%@%*@@@%@%@@@@@%%%%%%%#====---:=#%%%@@@@@@@@@
@@@@@@@@@@%%%%%%#*=::::-=%@@@@@@@@@@@@@@@@@@#***@@@#@@#@@@@@%#%#%%%%=:-::-:=##%%%@@@@@@@@@
@@@@@@@@@@@@@%%%%##+-::-::*%@@@@@@@@@@@@@@#+===#@@#@@%%@@@@@%#%%#%%%#----:=*#%%%@@@@@@@@@@
@@@@@@@@@@@@@@@%%%%##=:::::-%@@@@@@%%%%##*----+@@%%@@#@@@@@%%#%%##%##+-:-+*#%%%@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@%%%#*=::-%%%@@@%%%@@@@@@*-=-%@@@%#%%@@@@@%%#####**+--+*##%%%%@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@%%%%%##+=*#%%%%@@@@@@@@@@+-+@@@@%%%@@@%%%%%%*#*+=-=+*##%%%%%@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@%%%%%#*++#%%%%%%%%%@%%#:%@@@#%@@@@@%%%%##+=--=*##%%%%%@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@%%%%%%%%#***#%%%%%%%%%=%%%@%@@@@%%%##*+=++*##%%%%%%@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%#%%#********#########*******##%%%%%%%%@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%%%%%%%%%%##*****#####%%%%%%%%%%%%%%@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%%@@@@%%%%%%%%%%%%%%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""

print(rick)

figlet = Figlet(font="poison")

text = figlet.renderText("0x_Zile")

color = fg("red")

colored_text = f"{color}{text}{attr('reset')}"

print(colored_text)

def _HexGen(size):
    key =""
    for i in range(size):
        k = str(random.choice("0123456789abcdef"))
        key += f"{k}"
    return key 

def _HexToWif(Hex):
    byteHex = codecs.decode(Hex, 'hex')
    wifcompressed = bytes_to_wif(byteHex, compressed=True)
    wifUncompressed = bytes_to_wif(byteHex, compressed=False)
    return wifcompressed, wifUncompressed

def _wifToaddr(wifCompressed, wifUnCompressed):
    BitCompressed = Key(wifCompressed)
    BitUncompressed = Key(wifUnCompressed)
    return BitCompressed.address, BitUncompressed.address

def _LoadTargetFile(FileName):
    trg = [i.strip() for i in open(FileName).readlines()] 
    return set(trg)

def MainCheck():
    global z, wf
    target= 'RichAddr.txt'
    Target = _LoadTargetFile(FileName=target)
    z = 0
    wf = 0
    ig = 0
    while True:
        z+= 1
        Private_Key = _HexGen(64)
        WifCompressed, wifUncompressed = _HexToWif(Hex=Private_Key)
        CompressAddr, UnCompressAddr = _wifToaddr(WifCompressed,wifUncompressed)
        Nai = time.localtime()
        if str(CompressAddr) in Target or str(UnCompressAddr) in Target:
            wf += 1
            open('Found.txt','a').write(f'Compressed Address: {CompressAddr}\n'
                                        f'UnCompressed Address:{UnCompressAddr}\n'
                                        f'Private Key: {Private_Key}\n'
                                        f'WIF (Compressed): {WifCompressed}\n'
                                        f'WIF (Uncompressed): {wifUncompressed}\n')
        
        elif int(z % 100000) == 0:
            ig += 100000
            print(f"Generated: {ig} (SHA-256- HEX)...")
        else: 
            tm = time.strftime("%Y-%m-%d %H:%M:%S", Nai)
            print(f"[{tm}][Total: {z} Check: {z * 2}] #Found: {wf}", end="\r")

MainCheck()

if __name__ == '__main__':
    t=threading.Thread(target=MainCheck)
    t.start()
    t.join()
    