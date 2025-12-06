#  🚀 About

This is a robust, dockerized Python application designed to recursively scan a local directory and publish the file paths to a RabbitMQ queue.

### It uses a microservices architecture where:

- **RabbitMQ** runs in its own container to handle messaging.
- **Python Scanner** runs in a separate container, scanning the folder you provide and sending messages asynchronously.


The application is built to be stable, handling large directory structures and ensuring the RabbitMQ server is fully ready before the scanning begins.

##  How to Build & Run

### Prerequisites

    1 Install Docker Desktop: Download and install Docker Desktop for your operating system.

    2 Start Docker: Ensure Docker Desktop is running before typing any commands.


# ▶️ Running the Application

### You do not need to install Python or RabbitMQ on your computer. Docker handles everything. You only need to provide the path to the folder you want to scan.

**1. Open your terminal (Command Prompt, PowerShell, or Bash).**

**2. Run the command for your OS:**

### Windows (PowerShell)

Replace `C:\Users\YourName\Desktop\FilesToScan` with the actual path you want to scan:

```powershell
$env:HOST_PATH="C:\Users\YourName\Desktop\FilesToScan"; docker-compose up --build
```

### Mac or Linux (Bash): Replace ./my_folder with the actual path you want to scan.
```powershell
HOST_PATH="./my_folder" docker-compose up --build
```
### When you have already build the container (run the previous command and did not removed them)
#### For Windows (Powershell)
```powershell
$env:HOST_PATH="C:\Users\YourName\Desktop\FilesToScan"; docker-compose start 
```
#### Mac or Linux (Bash)
```powershell
HOST_PATH="./my_folder" docker-compose start
```

# ⚙️ Configuration & Ports

The application uses the following ports so they need to be free on your machine
| Port      | Service            | Description                          |
| --------- | ------------------ | ------------------------------------ |
| **5672**  | RabbitMQ Messaging | Used by Python Scanner               |
| **15672** | RabbitMQ Dashboard | For viewing messages in your browser |

# 🛠 Troubleshooting: "Port already allocated"

### If you see an error like:
```powershell
Bind for 0.0.0.0:5672 failed: port is already allocated
```
Another application is using that port.

### How to fix:

**1 Open docker-compose.yml**

**2 Locate the ports: section under rabbitmq**

**3 Change only the left-hand numbers**

### 🔧 Example — Changing to Ports 9000 and 9001

| Host Port | Container Port | Used For | Notes |
|-----------|----------------|----------|-------|
| **9000**  | 5672           | RabbitMQ Messaging | Python scanner will now connect to `localhost:9000` |
| **9001**  | 15672          | RabbitMQ Dashboard | Dashboard available at `http://localhost:9001` |


# ✅ Verifying Results

### Once running, you can confirm that messages are being received.

**1 Open your browser**

**2 Visit:** http://localhost:15672 (or your custom port, e.g. http://localhost:9001) before stopping the container

### Login credentials:

    Username: guest

    Password: guest 

### What to check:

**1 Click “Queues” at the top**

**2 Look for a queue named Files**

**3 Watch the Total messages count increase as scanning occurs**

# 🛑 Stopping the Application

### To stop all containers: 
    CTRL + C

### To remove containers completely:
    docker-compose down
    
