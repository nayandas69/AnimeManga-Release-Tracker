# **AnimeManga Release Tracker**  

🫠 **AnimeManga Release Tracker** is a Python-based automation tool that **fetches new anime episode releases** from **MyAnimeList** and **sends rich notifications** to a Discord webhook.  

🔹 **Supports:**  
✅ **Genres & Type** (TV, Movie, OVA) 📌  
✅ **Next Episode Countdown** (Time left until release) ⏳  
✅ **Localized Time Conversion** (UTC → Local Time) 🌍  
✅ **Popularity Stats** (Score, Rank, Members) 📊  
✅ **Rich Discord Messages** with **random embed colors** 🎨  


## 🛠 **Setup & Installation**  

### **Clone the Repository**
```bash
git clone https://github.com/nayandas69/AnimeManga-Release-Tracker.git
cd AnimeManga-Release-Tracker
```

### **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 🔐 **Setting Up Repository Secrets in GitHub**  

Instead of using a `.env` file locally, you can store **API keys securely** in **GitHub Secrets**.  

#### **Go to Your GitHub Repository**  
- Open your **GitHub repository**  
- Click on **Settings**  
- Scroll down to **"Secrets and variables" → "Actions"**  

#### **Add Secrets**  
Click **"New repository secret"** and add the following:  

| Secret Name          | Value (Example)             |
|----------------------|----------------------------|
| `MAL_CLIENT_ID`     | `your_mal_client_id_here`  |
| `DISCORD_WEBHOOK`   | `your_discord_webhook_url` |

#### **Use Secrets in GitHub Actions**  
The workflow **automatically loads** these secrets:  
```yaml
env:
  MAL_CLIENT_ID: ${{ secrets.MAL_CLIENT_ID }}
  DISCORD_WEBHOOK: ${{ secrets.DISCORD_WEBHOOK }}
```

**Now your API keys are secure!** 🔒

🔹 **How to get `MAL_CLIENT_ID`?**  
- Go to [MyAnimeList API](https://myanimelist.net/apiconfig)  
- Create an **application**  
- Copy your **Client ID**  

🔹 **How to get `DISCORD_WEBHOOK`?**  
- Go to your **Discord server settings**  
- Create a **new webhook** in a channel  
- Copy the **Webhook URL**  


## **Running the Script**  
```bash
python src/tracker.py
```
This will fetch new anime releases and send notifications to **Discord**.  


## **Example Discord Notification**
  


💖 **Enjoy & Star ⭐ this project if you find it useful!**