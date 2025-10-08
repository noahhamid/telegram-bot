import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
START, NAME, AGE, SKILLS, LOCATION, AVAILABILITY, WORK_TYPE, COMPLETE = range(8)

# Skill options
SKILL_OPTIONS = [
    ["Cleaning", "Cooking"],
    ["Laundry", "Child Care"],
    ["Elder Care", "All Skills"]
]

# Work type options
WORK_TYPE_OPTIONS = [
    ["Living In", "Part Time"],
    ["Full Time", "Flexible"]
]

async def start(update, context):
    """Start the servant registration process."""
    await update.message.reply_text(
        "🏠 **Welcome to Servant Agency Registration** 🏠\n\n"
        "Thank you for your interest in joining our team of professional servants!\n\n"
        "Let's collect your information to find you the perfect job opportunity.\n\n"
        "Please enter your **Full Name**:",
        reply_markup=ReplyKeyboardRemove()
    )
    return NAME

async def get_name(update, context):
    """Store name and ask for age."""
    name = update.message.text.strip()
    
    if len(name) < 2:
        await update.message.reply_text(
            "❌ Please enter a valid full name (at least 2 characters):"
        )
        return NAME
    
    context.user_data['name'] = name
    
    await update.message.reply_text(
        f"👤 Thank you, {name}!\n\n"
        "Please enter your **Age**:"
    )
    return AGE

async def get_age(update, context):
    """Store age and ask for skills."""
    age_text = update.message.text.strip()
    
    try:
        age = int(age_text)
        if age < 16 or age > 70:
            await update.message.reply_text(
                "❌ Please enter a valid age (16-70 years):"
            )
            return AGE
    except ValueError:
        await update.message.reply_text(
            "❌ Please enter a valid number for age:"
        )
        return AGE
    
    context.user_data['age'] = age
    
    await update.message.reply_text(
        f"✅ Age recorded: {age} years\n\n"
        "Now please select your **Skill Set**:\n\n"
        "• 🧹 Cleaning - House cleaning & maintenance\n"
        "• 🍳 Cooking - Meal preparation & cooking\n"
        "• 👕 Laundry - Washing, ironing & clothing care\n"
        "• 👶 Child Care - Baby sitting & child minding\n"
        "• 👵 Elder Care - Senior assistance & care\n"
        "• 🌟 All Skills - Comprehensive household management",
        reply_markup=ReplyKeyboardMarkup(
            SKILL_OPTIONS,
            one_time_keyboard=True,
            input_field_placeholder="Select your skills..."
        )
    )
    return SKILLS

async def get_skills(update, context):
    """Store skills and ask for location."""
    skills = update.message.text
    context.user_data['skills'] = skills
    
    skill_descriptions = {
        "Cleaning": "🧹 Professional cleaning specialist",
        "Cooking": "🍳 Skilled cook and meal preparer",
        "Laundry": "👕 Laundry and fabric care expert",
        "Child Care": "👶 Certified child care provider",
        "Elder Care": "👵 Compassionate elderly caregiver",
        "All Skills": "🌟 Comprehensive household manager"
    }
    
    await update.message.reply_text(
        f"✅ Skills recorded: {skills}\n"
        f"{skill_descriptions.get(skills, '')}\n\n"
        "Please enter your **Current Living Location** (City/Area):",
        reply_markup=ReplyKeyboardRemove()
    )
    return LOCATION

async def get_location(update, context):
    """Store location and ask for availability."""
    location = update.message.text.strip()
    
    if len(location) < 2:
        await update.message.reply_text(
            "❌ Please enter a valid location (city or area name):"
        )
        return LOCATION
    
    context.user_data['location'] = location
    
    await update.message.reply_text(
        f"📍 Location recorded: {location}\n\n"
        "Please describe your **Availability**:\n\n"
        "Examples:\n"
        "• 'Immediately available'\n"
        "• 'Available from next month'\n"
        "• 'Weekdays 9 AM - 5 PM'\n"
        "• 'Flexible schedule'\n"
        "• 'Need 2 weeks notice'"
    )
    return AVAILABILITY

async def get_availability(update, context):
    """Store availability and ask for work type."""
    availability = update.message.text.strip()
    
    if len(availability) < 3:
        await update.message.reply_text(
            "❌ Please provide more details about your availability:"
        )
        return AVAILABILITY
    
    context.user_data['availability'] = availability
    
    await update.message.reply_text(
        f"✅ Availability recorded!\n\n"
        "Now select your preferred **Type of Work**:\n\n"
        "• 🏠 **Living In** - Reside at employer's home\n"
        "• ⏱️ **Part Time** - Few hours daily/weekly\n"
        "• 💼 **Full Time** - Regular working hours\n"
        "• 🔄 **Flexible** - Adaptable to different schedules",
        reply_markup=ReplyKeyboardMarkup(
            WORK_TYPE_OPTIONS,
            one_time_keyboard=True,
            input_field_placeholder="Select work type..."
        )
    )
    return WORK_TYPE

async def get_work_type(update, context):
    """Store work type and complete registration."""
    work_type = update.message.text
    context.user_data['work_type'] = work_type
    
    # Get all collected data
    name = context.user_data.get('name', 'Not provided')
    age = context.user_data.get('age', 'Not provided')
    skills = context.user_data.get('skills', 'Not provided')
    location = context.user_data.get('location', 'Not provided')
    availability = context.user_data.get('availability', 'Not provided')
    
    # Create beautiful summary
    summary_text = (
        f"🎉 **REGISTRATION COMPLETE!** 🎉\n\n"
        f"👤 **Name:** {name}\n"
        f"🎂 **Age:** {age} years\n"
        f"🛠️ **Skills:** {skills}\n"
        f"📍 **Location:** {location}\n"
        f"📅 **Availability:** {availability}\n"
        f"💼 **Work Type:** {work_type}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "✅ **Thank you for registering with us!**\n\n"
        "We will review your application and contact you shortly with potential job opportunities that match your profile.\n\n"
        "For any urgent inquiries, please contact our recruitment team.\n\n"
        "Best regards,\n"
        "**Servant Agency Recruitment Team** 🌟"
    )
    
    # Log the registration
    logger.info(f"New servant registration: {name}, {age}, {location}, {skills}, {work_type}")
    
    await update.message.reply_text(
        summary_text,
        reply_markup=ReplyKeyboardRemove()
    )
    
    # Optional: Send notification to admin
    # await send_admin_notification(context, context.user_data)
    
    return ConversationHandler.END

async def cancel(update, context):
    """Cancel the registration process."""
    await update.message.reply_text(
        '❌ Registration cancelled.\n\n'
        'Type /start to begin registration again if you want to join our team.',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def help_command(update, context):
    """Send help information."""
    await update.message.reply_text(
        "🤖 **Servant Registration Bot Help**\n\n"
        "Use /start to begin your registration\n"
        "Use /cancel to stop the current registration\n\n"
        "**Registration Process:**\n"
        "1. 📝 Personal Information (Name, Age)\n"
        "2. 🛠️ Skill Set Selection\n"
        "3. 📍 Location Details\n"
        "4. 📅 Availability Information\n"
        "5. 💼 Work Type Preference\n\n"
        "We're excited to have you join our professional team!"
    )

async def send_admin_notification(context, user_data):
    """Optional: Send registration notification to admin."""
    # You can implement this to notify admins about new registrations
    # Example: Save to database, send email, or message admin chat
    pass

def main():
    """Start the servant registration bot."""
    # Your bot token (you can use the same or create a new bot for servants)
    TOKEN = "8298183314:AAGtNKOHmaafI7Z16VTTpHQ-sKooJls6tTo"
    
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            SKILLS: [MessageHandler(filters.Regex(
                '^(Cleaning|Cooking|Laundry|Child Care|Elder Care|All Skills)$'
            ), get_skills)],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_location)],
            AVAILABILITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_availability)],
            WORK_TYPE: [MessageHandler(filters.Regex(
                '^(Living In|Part Time|Full Time|Flexible)$'
            ), get_work_type)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Add handlers
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cancel", cancel))

    # Start the Bot
    print("🤖 Servant Registration Bot is starting...")
    print("Press Ctrl+C to stop the bot")
    application.run_polling()

if __name__ == '__main__':
    main()