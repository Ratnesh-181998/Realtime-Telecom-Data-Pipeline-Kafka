# 🚀 Real-Time Telecom Data Streaming Pipeline

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Kafka](https://img.shields.io/badge/Apache%20Kafka-3.x-black?style=for-the-badge&logo=apache-kafka)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?style=for-the-badge&logo=postgresql)
![Supabase](https://img.shields.io/badge/Supabase-Cloud-green?style=for-the-badge&logo=supabase)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=for-the-badge&logo=streamlit)
![Docker](https://img.shields.io/badge/Docker-Compose-blue?style=for-the-badge&logo=docker)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> **A production-ready, end-to-end data engineering project demonstrating real-time streaming analytics using Apache Kafka, PostgreSQL/Supabase, and interactive Streamlit dashboards.**

---

# DE 

<img width="1586" height="1403" alt="image" src="https://github.com/user-attachments/assets/41e58683-82ed-4ad9-ae7d-7d584f112118" />

<img width="600" height="324" alt="image" src="https://github.com/user-attachments/assets/e8bd50bd-dcfb-4863-bfb4-7c1789600aef" />

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Live Demo](#-live-demo)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Dashboard Tabs](#-dashboard-tabs-detailed-description)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Screenshots](#-screenshots)
- [Performance Metrics](#-performance-metrics)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 🌐🎬 Live Demo
🚀 **Try it now:**
- **Streamlit Profile** - https://share.streamlit.io/user/ratnesh-181998
- **Project Demo** - https://realtime-telecom-data-pipeline-kafka-rqf9q28jaxeq56hflarcch.streamlit.app/
- *Experience the real-time analytics dashboard with live data streaming from Supabase!*

---
## 🎯 Overview

This project implements a **real-time telecom Call Detail Record (CDR) processing pipeline** that demonstrates modern data engineering practices. It captures, processes, stores, and visualizes streaming data with sub-second latency, making it perfect for:

- 📊 **Data Engineers|ML Engineers** learning streaming architectures
- 🎓 **Students** exploring real-time analytics
- 💼 **Professionals** building portfolio projects
- 🏢 **Companies** needing telecom analytics solutions

### Key Highlights

✅ **Real-time streaming** with Apache Kafka  
✅ **Dual deployment** - Local (Docker) & Cloud (Supabase)  
✅ **Interactive dashboards** with auto-refresh  
✅ **Production-ready** code with error handling  
✅ **Scalable architecture** supporting millions of events  
✅ **Beautiful UI** with glassmorphism design  

---

## ✨ Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Real-Time Streaming** | Process CDRs with <100ms latency using Kafka |
| **Auto-Refresh Dashboard** | Updates every 30 seconds with countdown timer |
| **Dual Database Support** | Local PostgreSQL (Docker) + Cloud Supabase |
| **Interactive Visualizations** | Plotly charts with hover details & animations |
| **Data Quality Checks** | Validates records before database insertion |
| **Scalable Architecture** | Handles 1000+ events/second |
| **Cloud Deployment** | One-click deploy to Streamlit Cloud |
| **Docker Compose** | Complete local environment setup |

### Dashboard Features

- 📈 **Live KPIs**: Total calls, revenue, avg duration, total minutes
- 🥧 **Provider Analytics**: Donut charts, bar graphs, box plots
- 📊 **Time Series**: Dual-axis charts showing calls & revenue trends
- 📋 **Data Table**: Recent 20 records with formatted display
- 🔄 **Auto-Refresh**: Countdown timer with manual refresh option
- 🎨 **Premium UI**: Gradient backgrounds, glassmorphism cards, glow effects

---

## 🏗️ Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Producer  │ ───▶ │    Kafka    │ ───▶ │  Consumer   │ ───▶ │  Database   │
│ (Faker CDR) │      │   Broker    │      │ (Validator) │      │  Postgres   │
└─────────────┘      └─────────────┘      └─────────────┘      └─────────────┘
                                                                       │
                                                                       ▼
                                                              ┌─────────────────┐
                                                              │    Streamlit    │
                                                              │    Dashboard    │
                                                              └─────────────────┘
```

### Data Flow

1. **Producer** generates realistic CDRs using Faker library
2. **Kafka** queues messages in `telecom-data` topic
3. **Consumer** validates and processes records
4. **Database** stores processed data (PostgreSQL/Supabase)
5. **Dashboard** queries DB and renders interactive charts

---

## 🛠️ Tech Stack

### Core Technologies

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Language** | Python 3.11 | Core development language |
| **Streaming** | Apache Kafka 3.x | Message broker & event streaming |
| **Database** | PostgreSQL 15 | Local data warehouse |
| **Cloud DB** | Supabase | Cloud-hosted PostgreSQL |
| **Visualization** | Streamlit 1.x | Interactive web dashboard |
| **Charts** | Plotly 5.x | Dynamic, interactive visualizations |
| **Containerization** | Docker Compose | Local environment orchestration |
| **Data Generation** | Faker | Realistic test data creation |

### Python Libraries

```
kafka-python-ng==2.2.2
psycopg2-binary==2.9.9
streamlit==1.31.0
plotly==5.18.0
pandas==2.2.0
numpy==1.26.3
Faker==22.6.0
```

### Infrastructure Components

- **Zookeeper**: Kafka cluster coordination
- **Schema Registry**: Message schema management
- **Control Center**: Kafka monitoring UI
- **pgAdmin**: PostgreSQL management (optional)

---

## 📊 Dashboard Tabs (Detailed Description)

### Tab 1: 📊 Live Analytics

**Purpose**: Real-time monitoring of telecom operations with auto-refreshing metrics and charts.

#### Features:

1. **Status Bar**
   - 🟢 Live data indicator with pulsing animation
   - ⏰ Last updated timestamp (HH:MM:SS)
   - 📊 Total record count from database
   - ⏳ Auto-refresh countdown (30s timer)

2. **Key Performance Indicators (KPIs)**
   - **Total Calls**: Aggregate call count with phone icon
   - **Total Revenue**: Sum of billing amounts ($)
   - **Avg Duration**: Mean call length in minutes
   - **Total Minutes**: Cumulative talk time

3. **Network Provider Analytics**
   - **Donut Chart**: Call distribution by provider
     - Interactive hover with call count & percentage
     - Center annotation showing total calls
     - Color-coded by provider (Verizon, AT&T, T-Mobile, Sprint)
   
   - **Revenue Bar Chart**: Provider-wise revenue comparison
     - Gradient color scale from cyan to yellow
     - Dollar amounts displayed on bars
     - Hover details with exact revenue figures

4. **Call Activity Timeline**
   - **Dual-Axis Time Series**
     - Primary Y-axis: Number of calls (area chart)
     - Secondary Y-axis: Revenue in dollars (dotted line)
     - Hourly aggregation with unified hover
     - Gradient fill under call volume line

5. **Data Distribution Analysis**
   - **Call Duration Histogram**
     - 25 bins showing duration frequency
     - X-axis in minutes, Y-axis showing count
     - Cyan bars with green borders
   
   - **Box Plot by Provider**
     - Shows duration quartiles per provider
     - Outlier detection enabled
     - Color-coded by provider

6. **Recent Call Records Table**
   - Latest 20 records in formatted table
   - Columns: Caller, Receiver, Duration, Provider, Amount, Time
   - Duration formatted as "Xm Ys"
   - Amount formatted as "$X.XX"
   - Full-width responsive design

---

### Tab 2: 🏗️ Architecture & Tech Stack

**Purpose**: Comprehensive technical documentation for developers and data engineers.

#### Sections:

1. **Data Flow Architecture Diagram**
   - Visual flowchart with gradient boxes
   - Components: Producer → Kafka → Consumer → Database → Dashboard
   - Each box shows:
     - Component name with icon
     - Script filename
     - Brief description
   - Black bold text on colorful gradients
   - Arrows showing data flow direction

2. **Technology Stack Details**
   - **4 Technology Cards**:
     - 🐍 **Python 3.11**: Core language with libraries
     - 📨 **Apache Kafka**: Stream processing components
     - 🐘 **PostgreSQL**: Data storage options
     - 🐳 **Docker**: Containerization tools
   - Each card includes:
     - Large icon
     - Technology name
     - Description
     - List of specific tools/libraries

3. **Data Processing Pipeline Steps**
   - **5 Numbered Steps**:
     1. **Data Generation**: CDR creation with Faker
     2. **Kafka Publishing**: JSON serialization & topic publish
     3. **Stream Consumption**: Real-time message reading
     4. **Database Storage**: Validated record insertion
     5. **Visualization**: Dashboard querying & rendering
   - Each step has:
     - Numbered badge (01-05)
     - Icon and title
     - Detailed description

4. **How to Run This Project**
   - **Prerequisites Checklist**:
     - Docker Desktop
     - Python 3.8+
     - Java 11/17 (for Spark)
     - Git
   
   - **Installation Commands**:
     ```bash
     git clone <repo>
     pip install -r requirements.txt
     docker-compose up -d
     ```
   
   - **Running the Pipeline**:
     - Terminal 1: Producer
     - Terminal 2: Consumer
     - Terminal 3: Dashboard
   
   - **Verification Commands**:
     - Database connection test
     - Direct SQL query

---

### Tab 3: ℹ️ Project Documentation

**Purpose**: Beginner-friendly explanation making the project accessible to non-technical audiences.

#### Sections:

1. **What is This Project? (Simple Explanation)**
   - 3-paragraph overview using everyday language
   - Explains telecom call processing
   - Highlights real-time capabilities
   - Uses relatable examples

2. **Pizza Shop Analogy**
   - **Comparison Table**:
     - Pizza Orders ↔ Phone Calls
     - Order Tickets ↔ Kafka Messages
     - Kitchen ↔ Consumer
     - Sales Report ↔ Dashboard
   - Visual flow with arrows
   - Colored info boxes

3. **Follow the Data Journey (6 Steps)**
   - Each step has:
     - **Emoji number** (1️⃣-6️⃣)
     - **Title** with icon
     - **Simple explanation**: Plain English
     - **Technical explanation**: Developer terms
   - Expandable sections (all open by default)
   - Example: "John calls Sarah for 5 minutes"

4. **What Does Each Part Do? (Super Simple!)**
   - **5 Component Cards**:
     - 📝 Kafka Producer
     - 📨 Apache Kafka
     - 🔄 Consumer
     - 🗄️ PostgreSQL Database
     - 📊 Streamlit Dashboard
   - Each card includes:
     - Icon
     - Component name
     - Real-world analogy
     - Simple explanation
     - Concrete example

5. **Why Should You Care?**
   - **Real-World Applications**:
     - Uber: Real-time ride tracking
     - Netflix: Viewing analytics
     - Credit cards: Fraud detection
     - Gaming: Live leaderboards
   - **Business Value**:
     - Instant insights
     - Cost savings
     - Better decisions
     - Competitive advantage

6. **Common Questions (Beginner-Friendly)**
   - **FAQ with 8 Questions**:
     - What is streaming?
     - Why use Kafka?
     - What is a CDR?
     - Is this production-ready?
     - Can I modify it?
     - What skills do I learn?
     - How fast is it?
     - Can I deploy to cloud?
   - Simple, jargon-free answers

7. **Skills Demonstrated**
   - **4-Column Table**:
     - Skill Category
     - Technologies Used
     - What You Learn
     - Industry Relevance
   - Categories:
     - Data Engineering
     - Stream Processing
     - Database Management
     - Visualization & UI
     - DevOps & Deployment

8. **About the Creator**
   - Name: Ratnesh Singh
   - Role: Data Scientist (4+ Years)
   - Contact links (GitHub, LinkedIn, Email)

---

## 🚀 Installation

### Prerequisites

- **Docker Desktop** (for local setup)
- **Python 3.8+**
- **Git**
- **Supabase Account** (for cloud deployment)

### Local Setup (Docker + PostgreSQL)

```bash
# 1. Clone the repository
git clone https://github.com/Ratnesh-181998/realtime-telecom-pipeline.git
cd realtime-telecom-pipeline

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start Docker containers
docker-compose up -d

# 5. Wait for services to be healthy (30-60 seconds)
docker-compose ps

# 6. Create database table
docker exec -it postgres psql -U admin -d telecom_db -f /docker-entrypoint-initdb.d/init.sql
```

### Cloud Setup (Supabase)

```bash
# 1. Navigate to cloud dashboard folder
cd Supabase_cloud-dashboard

# 2. Create .streamlit/secrets.toml
mkdir -p .streamlit
cat > .streamlit/secrets.toml << EOF
SUPABASE_HOST = "your-project.supabase.co"
SUPABASE_PORT = "5432"
SUPABASE_DB = "postgres"
SUPABASE_USER = "postgres"
SUPABASE_PASSWORD = "your-password"
EOF

# 3. Run setup script to create table
python supabase_setup.py

# 4. (Optional) Bulk insert sample data
python bulk_insert.py
```

---

## 💻 Usage

### Running the Pipeline

**Terminal 1: Start Kafka Producer**
```bash
python kafka_producer.py
```
Output: `✅ Producing CDRs to Kafka... (Ctrl+C to stop)`

**Terminal 2: Start Consumer**
```bash
python kafka_to_postgres.py
```
Output: `✅ Consuming from Kafka and writing to PostgreSQL...`

**Terminal 3: Start Dashboard**

*Local Version:*
```bash
streamlit run Local_Postgres_Version/local_streamlit_app.py
```

*Cloud Version:*
```bash
streamlit run Supabase_cloud-dashboard/cloud_streamlit_app.py
```

**Terminal 4: (Optional) Start Supabase Producer**
```bash
cd Supabase_cloud-dashboard
python supabase_producer.py
```

### Accessing Dashboards

| Dashboard | URL | Data Source |
|-----------|-----|-------------|
| Local PostgreSQL | http://localhost:8501 | Docker PostgreSQL |
| Cloud Supabase | http://localhost:8504 | Supabase Cloud |

### Monitoring Kafka

Access Confluent Control Center: http://localhost:9021

---

## 📁 Project Structure

```
realtime-telecom-pipeline/
│
├── 📁 Local_Postgres_Version/          # Local Docker setup
│   ├── local_streamlit_app.py          # Local dashboard
│   └── README.md
│
├── 📁 Supabase_cloud-dashboard/        # Cloud deployment
│   ├── cloud_streamlit_app.py          # Cloud dashboard (main)
│   ├── supabase_producer.py            # Cloud data generator
│   ├── supabase_setup.py               # DB initialization
│   ├── bulk_insert.py                  # Bulk data loader
│   ├── requirements.txt                # Python dependencies
│   ├── .streamlit/
│   │   └── secrets.toml                # Supabase credentials
│   └── README.md
│
├── 📁 AWS_Version/                      # AWS Redshift version
│   └── (legacy files)
│
├── 📄 kafka_producer.py                 # Main Kafka producer
├── 📄 kafka_to_postgres.py              # Main consumer
├── 📄 postgres_connect.py               # DB connection test
├── 📄 postgres_create_table.sql         # Table schema
├── 📄 docker-compose.yml                # Docker orchestration
├── 📄 requirements.txt                  # Python dependencies
├── 📄 README.md                         # This file
├── 📄 LICENSE                           # MIT License
└── 📄 .gitignore                        # Git ignore rules
```

---

## 📸 Screenshots

### Dashboard Overview & Live Analytics Tab
<img width="2815" height="1466" alt="image" src="https://github.com/user-attachments/assets/c8df0dab-0684-4c26-babd-427963b7456a" />
<img width="2837" height="1434" alt="image" src="https://github.com/user-attachments/assets/d6a19be9-2316-4474-bfba-4e46ed411bfa" />
<img width="2863" height="1454" alt="image" src="https://github.com/user-attachments/assets/7c4bb6e7-beac-41d5-8f94-1f13168e5681" />
<img width="2861" height="1449" alt="image" src="https://github.com/user-attachments/assets/4229d042-2a70-4e77-8eeb-8f9de10dd2a7" />
<img width="2869" height="1443" alt="image" src="https://github.com/user-attachments/assets/90b878db-dcb7-4a2c-b1a3-aab3e65df3da" />
<img width="2856" height="1445" alt="image" src="https://github.com/user-attachments/assets/d4d0a1d9-2986-4c78-a148-3a98e7397ec0" />
<img width="2868" height="1432" alt="image" src="https://github.com/user-attachments/assets/9d386c69-56e4-40c8-8ea4-d506f5977b96" />

### Architecture Diagram
<img width="2872" height="1454" alt="image" src="https://github.com/user-attachments/assets/9db8c681-be60-4548-8ee8-e90765917879" />
<img width="2852" height="1422" alt="image" src="https://github.com/user-attachments/assets/39a56986-4493-4371-b81e-c475cbb85e4e" />
<img width="2837" height="1438" alt="image" src="https://github.com/user-attachments/assets/d77f8611-b994-4fc1-bfff-609a7dd5f4f4" />
<img width="2856" height="1439" alt="image" src="https://github.com/user-attachments/assets/f78bcd26-41ea-4330-b670-e18eef3a6715" />

### Documentation Tab
<img width="2850" height="1437" alt="image" src="https://github.com/user-attachments/assets/21f9f1d4-172b-4754-a166-a9913e9fa11a" />
<img width="2871" height="1375" alt="image" src="https://github.com/user-attachments/assets/f2f366c4-475f-4b22-a4c7-8a5e744d4b57" />
<img width="2821" height="1420" alt="image" src="https://github.com/user-attachments/assets/ccb3d0d0-3a47-4cf2-884a-be52c7b5ddaf" />
<img width="2830" height="1414" alt="image" src="https://github.com/user-attachments/assets/2679e14d-70e1-44d2-b81a-181e27110988" />
<img width="2860" height="1437" alt="image" src="https://github.com/user-attachments/assets/d392efd1-b35d-4a3a-86a1-0ef5602a1d78" />

### Backed Runing Code
<img width="940" height="466" alt="image" src="https://github.com/user-attachments/assets/bd26154f-e3ae-45b2-a61c-1e6655cd0032" />
<img width="940" height="501" alt="image" src="https://github.com/user-attachments/assets/f5597f59-45d1-4de8-9107-e610ef302b57" />
<img width="940" height="381" alt="image" src="https://github.com/user-attachments/assets/363d5ac3-6f56-472c-b264-ce7dc48b023f" />


---

## ⚡ Performance Metrics

| Metric | Value |
|--------|-------|
| **Throughput** | 1,000+ events/second |
| **Latency** | <100ms end-to-end |
| **Dashboard Refresh** | 30 seconds (auto) |
| **Data Retention** | Unlimited (PostgreSQL) |
| **Concurrent Users** | 100+ (Streamlit Cloud) |
| **Database Size** | Tested with 100K+ records |

---

## 🌐 Deployment

### Streamlit Cloud Deployment

1. **Push to GitHub**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `Supabase_cloud-dashboard/cloud_streamlit_app.py`
   - Add secrets in Advanced Settings:
     ```toml
     SUPABASE_HOST = "your-project.supabase.co"
     SUPABASE_PORT = "5432"
     SUPABASE_DB = "postgres"
     SUPABASE_USER = "postgres"
     SUPABASE_PASSWORD = "your-password"
     ```
   - Click Deploy!

3. **Configure Git LFS (for large files)**
```bash
git lfs install
git lfs track "*.csv"
git lfs track "*.parquet"
git add .gitattributes
git commit -m "Configure Git LFS"
git push
```

### Docker Deployment

```bash
# Build custom image
docker build -t telecom-dashboard .

# Run container
docker run -p 8501:8501 telecom-dashboard
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 style guide
- Add docstrings to functions
- Update README if needed
- Test locally before submitting
- Write clear commit messages

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

```
Copyright (c) 2024 Ratnesh Singh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Contact

**RATNESH SINGH**  
*Data Scientist | AI/ML Engineer| 4+ Years Experience*

- 📧 Email: [rattudacsit2021gate@gmail.com](mailto:rattudacsit2021gate@gmail.com)
- 💼 LinkedIn: [linkedin.com/in/ratneshkumar1998](https://www.linkedin.com/in/ratneshkumar1998/)
- 🐙 GitHub: [github.com/Ratnesh-181998](https://github.com/Ratnesh-181998)
- 📱 Phone: +91-947XXXXX46

### Project Links

- 🌐 **Live Demo**: [Streamlit Cloud](https://realtime-telecom-data-pipeline-kafka-rqf9q28jaxeq56hflarcch.streamlit.app/)
- 📖 **Documentation**: [GitHub Wiki](https://github.com/Ratnesh-181998/Realtime-Telecom-Data-Pipeline-Kafka/wiki)
- 🐛 **Issue Tracker**: [GitHub Issues](https://github.com/Ratnesh-181998/Realtime-Telecom-Data-Pipeline-Kafka/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Ratnesh-181998/Realtime-Telecom-Data-Pipeline-Kafka/discussions)

---

## 🌟 Acknowledgments

- **Apache Kafka** - Distributed streaming platform
- **Streamlit** - Open-source app framework
- **Supabase** - Open-source Firebase alternative of AWS Services 
- **Plotly** - Interactive graphing library
- **Docker** - Containerization platform

---

## 📈 Project Stats

![GitHub stars](https://img.shields.io/github/stars/Ratnesh-181998/realtime-telecom-pipeline?style=social)
![GitHub forks](https://img.shields.io/github/forks/Ratnesh-181998/realtime-telecom-pipeline?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/Ratnesh-181998/realtime-telecom-pipeline?style=social)
![GitHub issues](https://img.shields.io/github/issues/Ratnesh-181998/realtime-telecom-pipeline)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Ratnesh-181998/realtime-telecom-pipeline)

---

<div align="center">

**⭐ If you found this project helpful, please consider giving it a star! ⭐**

Made with ❤️ by [Ratnesh Singh](https://github.com/Ratnesh-181998)

</div>

---


<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=24,20,12,6&height=3" width="100%">


## 📜 **License**

![License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge&logo=opensourceinitiative&logoColor=white)

**Licensed under the MIT License** - Feel free to fork and build upon this innovation! 🚀

---

# 📞 **CONTACT & NETWORKING** 📞


## 💼 Professional Networks

[![LinkedIn](https://img.shields.io/badge/💼_LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ratneshkumar1998/)
[![GitHub](https://img.shields.io/badge/🐙_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Ratnesh-181998)
[![X](https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/RatneshS16497)
[![Portfolio](https://img.shields.io/badge/🌐_Portfolio-FF6B6B?style=for-the-badge&logo=google-chrome&logoColor=white)](https://share.streamlit.io/user/ratnesh-181998)
[![Email](https://img.shields.io/badge/✉️_Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:rattudacsit2021gate@gmail.com)
[![Medium](https://img.shields.io/badge/Medium-000000?style=for-the-badge&logo=medium&logoColor=white)](https://medium.com/@rattudacsit2021gate)
[![Stack Overflow](https://img.shields.io/badge/Stack_Overflow-F58025?style=for-the-badge&logo=stack-overflow&logoColor=white)](https://stackoverflow.com/users/32068937/ratnesh-kumar)

## 🚀 AI/ML & Data Science  [AI/ML 1620+ Problem Solved](https://github.com/Ratnesh-181998/DSML)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://share.streamlit.io/user/ratnesh-181998)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/RattuDa98)
[![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/rattuda)

## 💻 Competitive Programming [Including all coding plateform's 5000+ Problems/Questions solved](https://github.com/Ratnesh-181998/Algorithms-and-Data-Structures)
[![LeetCode](https://img.shields.io/badge/LeetCode-FFA116?style=for-the-badge&logo=leetcode&logoColor=black)](https://leetcode.com/u/Ratnesh_1998/)
[![HackerRank](https://img.shields.io/badge/HackerRank-00EA64?style=for-the-badge&logo=hackerrank&logoColor=black)](https://www.hackerrank.com/profile/rattudacsit20211)
[![CodeChef](https://img.shields.io/badge/CodeChef-5B4638?style=for-the-badge&logo=codechef&logoColor=white)](https://www.codechef.com/users/ratnesh_181998)
[![Codeforces](https://img.shields.io/badge/Codeforces-1F8ACB?style=for-the-badge&logo=codeforces&logoColor=white)](https://codeforces.com/profile/Ratnesh_181998)
[![GeeksforGeeks](https://img.shields.io/badge/GeeksforGeeks-2F8D46?style=for-the-badge&logo=geeksforgeeks&logoColor=white)](https://www.geeksforgeeks.org/profile/ratnesh1998)
[![HackerEarth](https://img.shields.io/badge/HackerEarth-323754?style=for-the-badge&logo=hackerearth&logoColor=white)](https://www.hackerearth.com/@ratnesh138/)
[![InterviewBit](https://img.shields.io/badge/InterviewBit-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://www.interviewbit.com/profile/rattudacsit2021gate_d9a25bc44230/)

---

## 📊 **GitHub Stats & Metrics** 📊



![Profile Views](https://komarev.com/ghpvc/?username=Ratnesh-181998&color=blueviolet&style=for-the-badge&label=PROFILE+VIEWS)




<img 
  src="https://streak-stats.demolab.com?user=Ratnesh-181998&theme=radical&hide_border=true&background=0D1117&stroke=4ECDC4&ring=F38181&fire=FF6B6B&currStreakLabel=4ECDC4"
  alt="GitHub Streak Stats"
width="48%"/>





<img src="https://github-readme-activity-graph.vercel.app/graph?username=Ratnesh-181998&theme=react-dark&hide_border=true&bg_color=0D1117&color=4ECDC4&line=F38181&point=FF6B6B" width="48%" />

---

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=24&duration=3000&pause=1000&color=4ECDC4&center=true&vCenter=true&width=600&lines=Ratnesh+Kumar+Singh;Data+Scientist+%7C+AI%2FML+Engineer;4%2B+Years+Building+Production+AI+Systems" alt="Typing SVG" />

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=18&duration=2000&pause=1000&color=F38181&center=true&vCenter=true&width=600&lines=Built+with+passion+for+the+AI+Community+🚀;Innovating+the+Future+of+AI+%26+ML;MLOps+%7C+LLMOps+%7C+AIOps+%7C+GenAI+%7C+AgenticAI+Excellence" alt="Footer Typing SVG" />


<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=footer" width="100%">


