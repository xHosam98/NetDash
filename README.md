# NetDash

**NetDash** is a lightweight, real-time system and network monitoring dashboard built with Python and Dash.  
It is designed primarily for Linux environments to provide easy-to-use visual insights into system performance.

## 🚀 Features

- Real-time monitoring of:
  - CPU usage
  - RAM usage
  - Network upload/download speeds
  - Network interface and IP address
- Tabbed Interface (Live Monitor, History, About Project)
- Export historical logs to CSV
- Reset stats button
- Toggle between Dark and Light themes

## 📦 Technologies Used

- Python 3
- Dash (Plotly framework)
- psutil (system metrics collection)
- Pandas (data export)
- Dash Bootstrap Components (UI and themes)

## 📑 Setup and Usage

### Install requirements:

```bash
pip3 install -r requirements.txt
```

### Run the application:

```bash
python3 dashboard.py
```

### Access the dashboard:

Visit [http://localhost:8050](http://localhost:8050) or your server's IP address + port from your web browser.

## 🔧 Configuration

The application is configured to allow connections from the local network.  
Make sure your firewall allows port `8050` if you are accessing from another device.

## 📌 Future Improvements

- Add alert notifications for CPU/RAM thresholds
- Database integration for persistent logs
- Remote access dashboard (outside local network)
- Additional language support

## 📖 License

This project is for academic use only.

---

**Developed by Hosam**  
Network Operating Systems Project | April 2025
