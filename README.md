# Project Integrator II - Compressor Energy Information Monitoring

This repository contains the code and documentation for the UTFPR Project Integrator II, which aims to monitor the energy information of a compressor and send alerts in case of anomalies.

## Overview

The project consists of acquiring the data from the compressor, transmitting it to a Raspberry Pi, which has a Node-RED script that stores this information in a local MySQL database and another hosted on azure. Also, the Node-RED transmit the information through a MQTT broker, which is read by the ESP32, to indicate the current opeation mode of the compressor. If there is any anomaly in the compressor's operation, Node-RED will send an email to the responsible professors while also activating a visual signal. The collected data can also be viewed on a web page.

<p align="center"> <img src="https://iili.io/JKN59Q2.png" width="600"/> </p>

### Implementations

About the sensor, we have the following implementation: 

<p align="center">  <img src="https://iili.io/JKNaaTb.png" width="600"/> </p>

About the ESP32, we have the following implementation: 

<p align="center">  <img src="https://iili.io/JKNlT79.png" width="600"/> </p>

## Technology

The following technologies were used in this project:

- PZEM-004T: sensor used to acquire the energy informations (voltage, current, power, phase angle and power factor) of the compressor. 
- Raspberry Pi 3: used to link the sensor by a USB port, host a MySQL database and to host Node-RED and mosquitto broker.  
- Node-RED: used to acquire sensor data, store this data in a MySQL database, send the information of live operation mode through a mosquitto broker and send alerts in case of anomalies.
- MySQL: used to store the collected data.
- MQTT: used to transmit the live operation mode of the compressor to the ESP.
- ESP32: used to sinalize the compressor operation mode, indicating the current mode of the compressor. 
- Streamlit: used to create the web page for viewing the collected data.
- Azure: used to host a MySQL database and the Streamlit web site.
- Terraform: used to create azure resources.

## Repository Structure

The repository is organized as follows:

- `espCode`: contains the code for the ESP32 microcontroller.
- `mysql`: contains the MySQL table structure.
- `nodered`: contains the Node-RED json.
- `streamlit_app`: contains the streamlit code.
- `terraform`: contains required azure resources.

## Results

The physical implementation looks as the following:

<p align="center"> <img src="https://iili.io/JKN0RaI.png" width="300" height="400"/> <img src="https://iili.io/JKN0dEQ.png" width="300" height="400"/> </p>

The operation mode sinalization implementation looks as the following:

<p align="center"> <img src="https://iili.io/JKN13oG.png" width="600"/> </p>

The Node-RED flow looks as the following:

<p align="center"> <img src="https://iili.io/JKN1Rix.png" width="500"/> </p>

The Streamlit final front-end dashboard looks as the following:

<p align="center"> <img src="https://iili.io/JKNET7I.png" width="600"/> </p>

<p align="center"> <img src="https://iili.io/JKNGnje.png" height="600" width="400"/> <img src="https://iili.io/JKNEL4R.png" height="600" width="400"/> </p>

This project helped the university to derive insights about the compressor usage, helping to understand why the compressor was wasting that much energy. 

## Contributing

This project was developed as part of the UTFPR Project Integrator II course. However, if you encounter any issues or have any suggestions for improvement, feel free to open an issue or send a pull request.

## Authors <img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" width="25" height="25" /> 

- [Flávio Neto](https://www.linkedin.com/in/flavio-sidnei-dos-santos-neto/)
- [Gustavo Carpejani](https://www.linkedin.com/in/gustavo-carpejani-a04631184/)
- [Júlio Tinti](https://www.linkedin.com/in/juliotinti/)
- [Lucas Moletta](https://www.linkedin.com/in/lucasmoletta/)

## License

This project is licensed under the MIT License. See the LICENSE file for details.
