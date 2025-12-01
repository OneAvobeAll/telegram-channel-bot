#!/usr/bin/env python
"""
Automated Telegram Channel Poster Bot
Sends posts with inline keyboard buttons to a Telegram channel.
Deploy-ready for Render.com
"""

import os
import logging
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler

# ===== CONFIGURATION =====
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHANNEL_ID = os.getenv("CHANNEL_ID", "")
ADMIN_USER_IDS = [int(id.strip()) for id in os.getenv("ADMIN_USER_IDS", "").split(",") if id.strip()]
# =========================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def send_channel_post(application):
    """Send initial post to channel when bot starts"""
    bot = application.bot
    try:
        post_text = (
            "🚀 **Welcome to Our Channel!** 🚀\n\n"
            "This is an automated post from our custom bot.\n"
            "Use the buttons below to interact!"
        )

        # Create inline keyboard with different button types
        keyboard = [
            [
                InlineKeyboardButton("🌐 Official Website", url="https://example.com"),
                InlineKeyboardButton("📚 Documentation", url="https://example.com/docs"),
            ],
            [
                InlineKeyboardButton("📢 Join Announcements", url="https://t.me/joinchat/EXAMPLE"),
                InlineKeyboardButton("👥 Community Chat", url="https://t.me/joinchat/EXAMPLE2"),
            ],
            [
                InlineKeyboardButton("✅ Mark as Read", callback_data="mark_read"),
                InlineKeyboardButton("📊 View Stats", callback_data="view_stats"),
            ],
            [
                InlineKeyboardButton("🔄 Refresh Post", callback_data="refresh"),
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)

        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=post_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        logger.info(f"✅ Posted to channel: {CHANNEL_ID}")

    except Exception as e:
        logger.error(f"❌ Failed to send post: {e}")

async def button_click_handler(update, context):
    """Handle inline button clicks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "mark_read":
        await query.message.reply_text("✅ Marked as read! (This appears in private chat)")
    elif query.data == "view_stats":
        await query.message.reply_text("📈 Channel stats: 1,000 members | 50 online")
    elif query.data == "refresh":
        new_text = f"{query.message.text}\n\n🔄 Last refreshed: Just now"
        await query.edit_message_text(text=new_text, reply_markup=query.message.reply_markup)

async def post_command(update, context):
    """Command to send a new post to channel"""
    user_id = update.effective_user.id
    
    # Authorization check
    if ADMIN_USER_IDS and user_id not in ADMIN_USER_IDS:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return
    
    await update.message.reply_text("📤 Sending new post to channel...")
    
    bot = context.bot
    try:
        post_text = (
            "📢 **New Announcement!**\n\n"
            "Important updates from the team:\n"
            "• New feature released\n"
            "• Bug fixes applied\n"
            "• Upcoming events"
        )
        
        keyboard = [
            [
                InlineKeyboardButton("📥 Download Update", url="https://example.com/download"),
                InlineKeyboardButton("📖 Read Changelog", url="https://example.com/changelog"),
            ],
            [
                InlineKeyboardButton("👍 Got It", callback_data="acknowledge"),
                InlineKeyboardButton("❓ Need Help", url="https://t.me/support_bot"),
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=post_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        await update.message.reply_text("✅ New post published successfully!")
        
    except Exception as e:
        logger.error(f"Post command failed: {e}")
        await update.message.reply_text(f"❌ Failed: {str(e)}")

async def start_command(update, context):
    """Start command handler"""
    user_id = update.effective_user.id
    is_admin = "✅" if user_id in ADMIN_USER_IDS else "❌"
    
    await update.message.reply_text(
        f"🤖 **Channel Poster Bot**\n\n"
        f"Admin Status: {is_admin}\n"
        f"Your ID: `{user_id}`\n\n"
        f"**Commands:**\n"
        f"/post - Send new post to channel\n"
        f"/help - Show this message\n\n"
        f"Channel: {CHANNEL_ID}",
        parse_mode="Markdown"
    )

async def help_command(update, context):
    """Help command"""
    await start_command(update, context)

def main():
    """Main function to start the bot"""
    # Validate required environment variables
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN environment variable is not set!")
        return
    if not CHANNEL_ID:
        logger.error("❌ CHANNEL_ID environment variable is not set!")
        return
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("post", post_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_click_handler))
    
    # Send initial post on startup
    application.post_init = send_channel_post
    
    # Start the bot
    logger.info("Starting Channel Poster Bot...")
    application.run_polling(allowed_updates=["message", "callback_query"])

if __name__ == "__main__":
    main()
