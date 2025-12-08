# 🚀 Deployment Guide

## Quick Start for GitHub Upload

### Step 1: Initialize Git Repository

```bash
cd C:\Users\rattu\Downloads\kafka-spark-redshift-streaming

# Initialize Git (if not already done)
git init

# Add remote repository
git remote add origin https://github.com/Ratnesh-181998/realtime-telecom-pipeline.git
```

### Step 2: Configure Git LFS

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.csv"
git lfs track "*.parquet"
git lfs track "*.db"

# Add .gitattributes
git add .gitattributes
```

### Step 3: Stage and Commit Files

```bash
# Add all files
git add .

# Commit
git commit -m "Initial commit: Real-time Telecom Data Pipeline"

# Push to GitHub
git push -u origin main
```

---

## Streamlit Cloud Deployment

### Step 1: Prepare Repository

1. Ensure `Supabase_cloud-dashboard/requirements.txt` exists
2. Ensure `Supabase_cloud-dashboard/cloud_streamlit_app.py` is the main file
3. Remove or gitignore `secrets.toml`

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repository: `Ratnesh-181998/realtime-telecom-pipeline`
4. Set main file path: `Supabase_cloud-dashboard/cloud_streamlit_app.py`
5. Click "Advanced settings"

### Step 3: Add Secrets

In Advanced Settings → Secrets, add:

```toml
SUPABASE_HOST = "db.qsqlawrciwrtrlotodke.supabase.co"
SUPABASE_PORT = "5432"
SUPABASE_DB = "postgres"
SUPABASE_USER = "postgres"
SUPABASE_PASSWORD = "Ratan@181998"
```

### Step 4: Deploy

1. Click "Deploy!"
2. Wait 2-3 minutes for deployment
3. Your app will be live at: `https://your-app-name.streamlit.app/`

---

## Supabase Setup

### Create Table in Supabase

1. Go to [supabase.com](https://supabase.com)
2. Open SQL Editor
3. Run this query:

```sql
CREATE TABLE IF NOT EXISTS telecom_data (
    id SERIAL PRIMARY KEY,
    caller_name VARCHAR(256),
    receiver_name VARCHAR(256),
    caller_id VARCHAR(20),
    receiver_id VARCHAR(20),
    start_datetime TIMESTAMP,
    end_datetime TIMESTAMP,
    call_duration INTEGER,
    network_provider VARCHAR(50),
    total_amount DECIMAL(5,2)
);

CREATE INDEX idx_start_datetime ON telecom_data(start_datetime DESC);
CREATE INDEX idx_network_provider ON telecom_data(network_provider);
```

### Start Data Producer

```bash
cd Supabase_cloud-dashboard
python supabase_producer.py
```

This will continuously insert data into Supabase.

---

## Troubleshooting

### Issue: Port already in use

**Solution:**
```bash
# Find process using port
netstat -ano | findstr :8501

# Kill process (replace PID)
taskkill /PID <PID> /F
```

### Issue: Git LFS not working

**Solution:**
```bash
# Reinstall Git LFS
git lfs install --force

# Migrate existing files
git lfs migrate import --include="*.csv,*.parquet"
```

### Issue: Streamlit Cloud deployment fails

**Solution:**
1. Check `requirements.txt` has all dependencies
2. Verify secrets are correctly added
3. Check logs in Streamlit Cloud dashboard
4. Ensure main file path is correct

---

## Post-Deployment Checklist

- [ ] Repository pushed to GitHub
- [ ] Git LFS configured for large files
- [ ] Streamlit app deployed and running
- [ ] Supabase table created
- [ ] Secrets added to Streamlit Cloud
- [ ] Data producer running (optional)
- [ ] README updated with live demo link
- [ ] Screenshots added to repository

---

## Updating the App

```bash
# Make changes to code
# ...

# Commit and push
git add .
git commit -m "Update: <description>"
git push

# Streamlit Cloud will auto-deploy
```

---

## Monitoring

### Streamlit Cloud
- View logs: Streamlit Cloud dashboard → Logs
- Check metrics: Dashboard → Metrics
- Restart app: Dashboard → Reboot

### Supabase
- View data: Supabase → Table Editor
- Check logs: Supabase → Logs
- Monitor usage: Supabase → Settings → Usage

---

## Support

If you encounter issues:
1. Check [GitHub Issues](https://github.com/Ratnesh-181998/realtime-telecom-pipeline/issues)
2. Review [Streamlit Docs](https://docs.streamlit.io)
3. Contact: rattudacsit2021gate@gmail.com
