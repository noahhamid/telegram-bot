import logging
import os
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
WELCOME, SERVICE_TYPE, SERVICES, NAME, PHONE = range(5)

async def start(update, context):
    """Start the conversation with welcome message."""
    await update.message.reply_text(
        "👋 Hello! Welcome to our Servant Agency!\n\n"
        "We're here to help you with all your household needs. "
        "Let's get started with your service request!",
        reply_markup=ReplyKeyboardMarkup(
            [["Standard", "Dynamic"]], 
            one_time_keyboard=True,
            input_field_placeholder="Choose service type..."
        )
    )
    return SERVICE_TYPE

async def service_type(update, context):
    """Store service type and ask for specific services."""
    service_type = update.message.text
    context.user_data['service_type'] = service_type
    
    service_description = {
        "Standard": "✅ Fixed schedule, regular services",
        "Dynamic": "🔄 Flexible timing, on-demand services"
    }
    
    await update.message.reply_text(
        f"Great! You selected {service_type} service.\n"
        f"{service_description.get(service_type, '')}\n\n"
        "Now please choose the specific services you need:",
        reply_markup=ReplyKeyboardMarkup(
            [
                ["Full House Work"],
                ["Cleaning the House"], 
                ["Doing the Laundry"],
                ["More Services"]
            ],
            one_time_keyboard=True,
            input_field_placeholder="Select services needed..."
        )
    )
    return SERVICES

async def services(update, context):
    """Store services and ask for name."""
    services = update.message.text
    context.user_data['services'] = services
    
    service_details = {
        "Full House Work": "🧹 Complete household maintenance",
        "Cleaning the House": "🏠 Deep cleaning and organization", 
        "Doing the Laundry": "👕 Washing, drying, and folding",
        "More Services": "📋 Additional custom services"
    }
    
    if services == "More Services":
        await update.message.reply_text(
            "For additional services like:\n"
            "• Cooking & Meal Prep 🍳\n"
            "• Child/Elderly Care 👶👵\n" 
            "• Pet Care 🐕\n"
            "• Gardening 🌿\n"
            "• Other custom requirements\n\n"
            "Our team will contact you to discuss your specific needs."
        )
    
    await update.message.reply_text(
        f"✅ {service_details.get(services, 'Service noted')}\n\n"
        "Please enter your full name:",
        reply_markup=ReplyKeyboardRemove()
    )
    return NAME

async def name(update, context):
    """Store name and ask for phone number."""
    name = update.message.text.strip()
    
    if len(name) < 2:
        await update.message.reply_text(
            "Please enter a valid full name (at least 2 characters):"
        )
        return NAME
    
    context.user_data['name'] = name
    
    await update.message.reply_text(
        f"Thank you, {name}!\n\n"
        "Please enter your phone number:\n"
        "(Format: +1234567890 or 1234567890)"
    )
    return PHONE

async def phone(update, context):
    """Store phone number and end conversation."""
    phone = update.message.text.strip()
    context.user_data['phone'] = phone
    
    # Get all collected data
    service_type = context.user_data.get('service_type', 'Not provided')
    services = context.user_data.get('services', 'Not provided')
    name = context.user_data.get('name', 'Not provided')
    
    # Log the submission
    logger.info(f"New service request - Name: {name}, Phone: {phone}, Type: {service_type}, Service: {services}")
    
    # Final confirmation message
    await update.message.reply_text(
        f"✨ Thank you, {name}!\n\n"
        "📋 Here's your service request summary:\n"
        f"• Service Type: {service_type}\n"
        f"• Service: {services}\n"
        f"• Contact: {phone}\n\n"
        "📞 We will contact you shortly to confirm your booking and discuss details.\n\n"
        "Thank you for choosing our Servant Agency! 🌟"
    )
    
    return ConversationHandler.END

async def cancel(update, context):
    """Cancel the conversation."""
    await update.message.reply_text(
        '❌ Conversation cancelled.\n\n'
        'Type /start to begin again if you need our services.',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def help_command(update, context):
    """Send a help message."""
    await update.message.reply_text(
        "🤖 Servant Agency Bot Help:\n\n"
        "Use /start to begin a new service request\n"
        "Use /cancel to stop the current conversation\n\n"
        "Our services include:\n"
        "• Full House Work\n"
        "• Cleaning Services\n" 
        "• Laundry Services\n"
        "• Custom Requirements\n\n"
        "We're here to help with all your household needs!"
    )

def main():
    """Start the client service bot."""
    # Get token from environment variables
    TOKEN = os.getenv('BOT_TOKEN_CLIENT')
    
    if not TOKEN:
        logger.error("❌ BOT_TOKEN_CLIENT not found in environment variables!")
        logger.error("Please check your .env file")
        return
    
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SERVICE_TYPE: [
                MessageHandler(filters.Regex('^(Standard|Dynamic)$'), service_type)
            ],
            SERVICES: [
                MessageHandler(filters.Regex('^(Full House Work|Cleaning the House|Doing the Laundry|More Services)$'), services)
            ],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Add handlers
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cancel", cancel))

    # Start the Bot
    print("🤖 Client Service Bot is starting...")
    print("✅ Token loaded from environment variables")
    print("🏠 Bot is ready to accept service requests!")
    print("Press Ctrl+C to stop the bot")
    
    try:
        application.run_polling()
    except Exception as e:
        logger.error(f"❌ Bot failed to start: {e}")
        print("❌ Bot failed to start. Please check your token and internet connection.")

if __name__ == '__main__':
    main()