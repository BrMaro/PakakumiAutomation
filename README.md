# PakakumiAutomation
This script automates the betting process for the crash-style game Pakakumi, primarily based in Kenya. It utilizes the Selenium framework to interact with the game website and implement various strategies for betting.

## Features

- **Login Automation:** Provides a seamless login process for the user, prompting for phone number and password.
- **Betting Strategies:** Implements betting strategies based on the game's past outcomes, including calculation of previous bets and green vs red counters.
- **Dynamic Betting Amounts:** Adjusts betting amounts based on the user's account balance and green counters.
- **Auto-Cashout:** Allows users to set an auto-cashout value for their bets.

## Setup

1.**Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/pakakumi-automation.git
   ```
2.**Install Dependencies:**

```bash
pip install -r requirements.txt
```
3.**Run the Script:**

```bash
python pakakumi_automation.py
```
## Usage
Input your phone number and password when prompted.
The script will automatically log in and skip any entry dialog boxes.
Set your betting and auto-cashout preferences within the script.
The script will continuously monitor the game and execute betting strategies.

## Strategies and Features
1. **Previous Bets Calculation**
The script calculates the average outcome of previous bets to determine profitability.

2. **Dynamic Betting Amounts**
Adjusts betting amounts based on the user's account balance and green counters to optimize the betting strategy.

3. **Auto-Cashout**
Allows users to set an auto-cashout value for their bets, providing additional control over the betting process.

## Disclaimer
This script is provided for educational and experimental purposes only. Use it responsibly, and be aware of the risks involved in automated betting.

## Contributing
Feel free to contribute to the project by opening issues or submitting pull requests. Your feedback and enhancements are welcome!
