LEARNING_MODULES = {
    'phishing': {
        'beginner': {
            'title': '🎣 Phishing Basics (Beginner)',
            'intro': 'Phishing is when scammers pretend to be your bank or a company to steal your passwords.',
            'points': [
                'Check the sender: If your bank usually texts from "HDFCBK", a random 10-digit number is a scam.',
                'Look for panic: Scammers say "Your account will be blocked today!" to make you act fast without thinking.',
                'Never click links in SMS: Open your official bank app directly instead of clicking a link in a message.'
            ]
        },
        'intermediate': {
            'title': '🎣 Advanced Phishing Tactics (Intermediate)',
            'intro': 'Scammers use fake domains and cloned websites to bypass basic checks.',
            'points': [
                'Lookalike Domains: Check the spelling. "hdfcbank.com" is real, but "hdfcbank-secure.com" is fake.',
                'Hover over links: On a computer, hover your mouse over a link to see the real destination at the bottom of the screen.',
                'Greetings: Real companies use your name ("Dear Rajesh"). Scammers often use "Dear Customer".'
            ]
        },
        'advanced': {
            'title': '🎣 Spear Phishing & Social Engineering (Advanced)',
            'intro': 'Targeted attacks that use your personal data (from LinkedIn/Facebook) to build extreme trust.',
            'points': [
                'Spear Phishing: An email might reference your actual boss or a recent project. Verify via a separate channel (e.g., call your boss directly).',
                'Email Header Analysis: Check the "Reply-To" address. A scammer can spoof the "From" address, but the Reply-To will go to their inbox.',
                'Zero-Trust Mindset: Even if an email looks 100% real, if it asks for credentials or payment, verify through a known phone number.'
            ]
        }
    },
    'digital_arrest': {
        'beginner': {
            'title': '🚨 What is a Digital Arrest? (Beginner)',
            'intro': 'A scam where fake police or CBI officers call you on video and threaten to arrest you.',
            'points': [
                'Police never call on WhatsApp video: Real arrests happen in person. There is no such thing as a video arrest.',
                'They will ask for money: They will say "Pay a clearance fee or we will arrest you." This is always a lie.',
                'You are safe: Do not panic. Hang up and tell your family immediately.'
            ]
        },
        'intermediate': {
            'title': '🚨 The Anatomy of a Digital Arrest (Intermediate)',
            'intro': 'Understanding the psychological manipulation used by these scammers.',
            'points': [
                'The Isolation Tactic: They will say, "This is a confidential case, do not tell anyone." They do this so your family can\'t tell you it\'s a scam.',
                'Fake Documents: They will send you a PDF warrant with a fake judge\'s signature. Real warrants are delivered physically by court officials.',
                'The "Verification" Trap: They demand you transfer money to an "RBI account" to prove your innocence. The government has no such account.'
            ]
        },
        'advanced': {
            'title': '🚨 Digital Arrest: Psychological Defense (Advanced)',
            'intro': 'How to handle high-pressure interrogation tactics if you are targeted.',
            'points': [
                'Refuse the Script: Scammers use a script to keep you on the back foot. Interrupt them, ask for their department ID, and state you are calling your lawyer.',
                'Deepfake Threats: Advanced scammers use AI voice cloning to sound like a relative in distress or a real officer. Use a "safe word" with your family.',
                'The Law: Indian law enforcement agencies do not conduct interrogations over Skype/WhatsApp. If they threaten immediate arrest, they are violating protocol.'
            ]
        }
    },
    'malicious_app': {
        'beginner': {
            'title': '📱 Safe App Downloading (Beginner)',
            'intro': 'Fake apps are used to steal your photos, contacts, and banking passwords.',
            'points': [
                'Use the App Store: Only download apps from Google Play or Apple App Store. Never download APK files sent on WhatsApp.',
                'Too Good to Be True: If an app promises "Free Recharge" or "Free Netflix," it is a scam.',
                'Read the Permissions: If a simple calculator app asks for your SMS and Contacts, deny it and uninstall.'
            ]
        },
        'intermediate': {
            'title': '📱 Permission Auditing (Intermediate)',
            'intro': 'Learn which permissions are safe and which are dangerous.',
            'points': [
                'SMS & Call Logs: Very few apps actually need this. If a game or a photo editor asks for SMS access, it wants to steal OTPs.',
                'Accessibility Services: This is the most dangerous permission. It allows an app to read your screen and click buttons for you. Only give this to trusted apps like screen readers.',
                'Play Protect: Always keep Google Play Protect enabled in your settings.'
            ]
        },
        'advanced': {
            'title': '📱 Malware Mechanics & Sideloading (Advanced)',
            'intro': 'How Android malware actually takes over your phone.',
            'points': [
                'Overlay Attacks: Malware uses "Draw over other apps" to display a fake bank login screen over your real bank app to steal your password.',
                'Sideloading Risks: APKs from outside the Play Store do not go through security vetting. They often contain Trojans.',
                'Isolation: If you must run a risky APK, do it in a secure folder or emulator, never on your primary device with your real bank accounts.'
            ]
        }
    }
}