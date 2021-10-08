# Casper_MiniWallet
## Introduction:
  This repository contains a small implementation of a Casper (CSRP) coin wallet written with Python, Kivy, and the Casper Python SDK. It was created exclusively for a Gitcoin hackathon (more information can be found here: https://gitcoin.co/issue/casper-network/gitcoin-hackathon/28/100026610) and known aesthetical and security concerns have been overlooked during the development. Therefore, it should not, by any means, be used in a production environment. That aside, the repository is made of two different components responsible for creating QR Codes for basic account-to-account transactions in the Casper Testnet and then, subsequently, loading the aforementioned QR Codes, signing the corresponding transactions, and releasing them into the network. These two functions are implemented in creator_side.py and sender_side.py, respectively, which can be run as two separate Kivy apps. Following is a reasonably detailed explanation of the implementation.
## Getting it up and running:
  The first step is to download or clone the repository into your working directory and move into it. In terms of programming languages, Python 3 and pip are the only requirements to run the code. Kivy is a cross-platform python library for developing GUI applications and runs pretty well on both Linux and Windows operating systems. With some effort, this app could be also theoretically compiled to run on Android and iOS, but I didn't venture that far.
Next, install all the necessary python dependencies with:
```
pip install -r requirements.txt
```
  In order to work successfully, the repository needs access to a valid testnet key pair with enough funds to perform transactions. You can get both the key pair and the funds at https://testnet.cspr.live/ through the account creation and faucet option respectively. Notice that any CSRP transferred in the testnet has no economical value. All the three files (secret_key.pem, public_key.pem, public_key_hex.txt) should be downloaded and saved into pair1 directory to be accessed by the program. Ideally, a second fresh key pair would be required to test the functionality, but any valid public key from the testnet would do. For organization reasons, I saved my second key pair in the pair2 directory.
After all this has been taken care of, you can proceed to the next step.
## Generating QR Codes: creator_side.py
You can run this piece simply by typing
```
python creator_side.py
```
in your console. A few lines of log and info text will be printed and a Kivy app window will be spawned. Sometimes, a popup with additional information will appear. Most of the time, you just need to click on ok to dismiss it. As shown in the screenshot below, the window has three input fields to be filled with information, though only the Address and Value fields are required. If you try to omit either of them, a popup will warn you that you made a mistake.

![creator_side.py main window](https://raw.githubusercontent.com/FrGS-0/Casper_MiniWallet/main/screenshots/Creating%20QR%20Code%20(Window%20Only).PNG)

The necessary fields are self-explanatory. The address should be a valid testnet public key in hexadecimal format (The one within public_key_hex.txt) and correspond to the recipient address. The Value (in CSRP) should be, obviously, within the spending power of the person who is going to read and sign the transaction. All the CSRP values are later converted to motes for the generation of the QR Code (1 CSRP = 10 ** 9 motes). If you try to read the QR Code with your phone, for example, the value will be 10 ** 9 times greater than what you inputted.
All this information is then encoded into a JSON string according to the following schema:
```
{
  "address": "Address of the recipient",
  "value": "Ammount to be transfered in motes",
  "message": "An optional greeting or informational message to be included in the QR Code"
}
```
Now, click on "Get QR" and get your QR Code.

![Getting your QR Code](https://raw.githubusercontent.com/FrGS-0/Casper_MiniWallet/main/screenshots/Created%20QR%20Code%20(Window%20Only).PNG)

You can save the generated QR Code as a file named qr.png in the same directory as the creator_side.py script to be used in the next section by clicking on "Save QR", or you can create a new QR Code by going with "New QR". Once you are done with it, you can exit the program by either closing the Kivy window or using Ctrl+C in the console.
