# WiFi-extractor-

# WiFi Password Extractor & Token Manager GUI

A professional-grade Windows-based Python application to extract saved WiFi credentials, manage connections, and securely handle data using JWT (JSON Web Tokens). This tool features both CLI and a modern GUI built with PyQt5, and includes ASCII art via the `art` library for stylized terminal output.

## Features

* **Extract Saved WiFi Credentials**

  * Retrieve SSID and password for saved networks on Windows.
  * View and export credentials in JSON, CSV, and TXT formats.

* **WiFi Network Management**

  * Connect and disconnect from WiFi networks.
  * Scan for available SSIDs.
  * Wait for active connection with a timeout feature.

* **DNS Management**

  * View and configure static DNS servers on your network interface.

* **Secure Token Handling**

  * Encode WiFi credentials into encrypted JWT tokens.
  * Decode tokens to retrieve credentials securely.
  * Export/import encrypted JSON credential data.

* **ASCII Visualization**

  * Display stylized ASCII reports, summaries, and banners using the `art` package.

* **Graphical User Interface (GUI)**

  * Intuitive GUI built with PyQt5.
  * Table-based view of WiFi credentials.
  * Buttons to extract, export, and generate secure tokens.

## Requirements

* Windows OS
* Python 3.7+
* Dependencies:

  ```bash
  pip install pyjwt art pyqt5
  ```

## Usage

### CLI Mode

Run the script directly to use the terminal-based interface:

```bash
python wifi_tool.py
```

### GUI Mode

Launch the GUI with:

```bash
python wifi_tool.py
```

> The GUI includes functionality to extract credentials, generate tokens, and export data.

## File Outputs

* `wifi_credentials.json` — Plain JSON file of credentials
* `wifi_credentials.csv` — CSV format
* `wifi_credentials_encrypted.json` — JWT-encrypted credentials
* `wifi_token.jwt` — Token saved to file
* `wifi_log.txt` — Log of extractions

## Security Notice

> JWT tokens are only as secure as the secret key. Always store `SECRET_KEY` securely and rotate it periodically.

## Contributions

Contributions are welcome! Please fork the repository and submit a pull request.

## License

MIT License

---

Developed with ❤️ for security researchers, system admins, and penetration testers.
 
With utmost respect, we cordially invite all developers who are proficient and experienced in the python programming language to contribute to the development and expansion of this project. Please note that only contributions made using python will be considered and accepted. In conclusion, I sincerely request all developers who wish to contribute to this project to place creativity and innovation at the heart of their work before taking any action. Please ensure that your code is written with the utmost precision, clarity, and organization. It is also essential to continuously ask yourself: *Do the new features and functionalities I intend to implement align with the structure and logic of the existing codebase?*  Paying close attention to these considerations will undoubtedly enhance the quality of the project and lay the foundation for sustainable development. In conclusion, I sincerely request all developers who wish to contribute to this project to place creativity and innovation at the heart of their work before taking any action. Please ensure that your code is written with the utmost precision, clarity, and organization.  It is also essential to continuously ask yourself: *Do the new features and functionalities I intend to implement align with the structure and logic of the existing codebase?*  Paying close attention to these considerations will undoubtedly enhance the quality of the project and lay the foundation for sustainable development. 
