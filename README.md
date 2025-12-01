# Telegram Channel Poster Bot

A bot that posts messages with interactive buttons to your Telegram channel.

## 🚀 Quick Setup

### 1. Create Bot
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` and follow instructions
3. Save your bot token

### 2. Channel Setup
1. Add your bot as an **Administrator** to your channel
2. Grant at least "Post Messages" permission
3. Get your channel ID:
   - For public channels: Use `@channelname`
   - For private channels: Use numeric ID (e.g., -1001234567890)

### 3. Deploy on Render

**Method A: Using Blueprint (Recommended)**
1. Push these files to GitHub
2. Go to Render.com → "New +" → "Blueprint"
3. Connect your repository
4. Add environment variables

**Method B: Manual Deployment**
1. Create new Web Service on Render
2. Connect GitHub repository
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python channel_bot.py`
4. Add environment variables

### 4. Environment Variables

Add these in Render dashboard:
- `BOT_TOKEN`: Your bot token from @BotFather
- `CHANNEL_ID`: Your channel ID (e.g., -1001234567890)
- `ADMIN_USER_IDS`: Comma-separated admin user IDs (optional)
- `PORT`: 8080 (Render sets this automatically)

## 📋 Usage

Once deployed:
1. Send `/start` to your bot in Telegram
2. Send `/post` to publish a new announcement
3. Channel members can click buttons for interaction

## 🔧 Customization

Edit `channel_bot.py` to modify:
- Message content in `send_channel_post()` function
- Button layout in the `keyboard` arrays
- Button actions in `button_click_handler()`

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Bot not posting | Check bot is channel admin |
| Buttons not working | Verify bot is running on Render |
| Duplicate posts | Wait 15 mins after deployment |
| "Forbidden" error | Re-add bot as channel admin |

## 📞 Support

For issues, check Render logs or contact support.
