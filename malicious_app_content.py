APP_QUESTIONS = [
    {
        'id': 1,
        'app_name': 'Super Flashlight Pro',
        'developer': 'Flashlight Tools Inc.',
        'icon': '🔦',
        'description': 'The brightest flashlight app for your phone!',
        'permissions': [
            'Camera',
            'Read SMS',
            'Read Contacts',
            'Access Location'
        ],
        'answer': 'malicious',
        'red_flags': [
            'A flashlight app needs ZERO of these permissions',
            'Reading SMS is used to steal OTPs',
            'Reading Contacts is used to spread scams',
            'Location tracking is a massive privacy risk'
        ],
        'explanation': 'This is a classic "Trojan" app. A real flashlight only needs camera (flash) access, and even that is optional. Requesting SMS and Contacts is a massive red flag for spyware and OTP theft.'
    },
    {
        'id': 2,
        'app_name': 'SBI YONO Official',
        'developer': 'com.sbi.yono',
        'icon': '🏦',
        'description': 'Official banking app for State Bank of India customers.',
        'permissions': [
            'Camera (for scanning cheques)',
            'Network access',
            'Biometric authentication'
        ],
        'answer': 'safe',
        'red_flags': [],
        'explanation': 'These permissions are standard for a banking app. The developer name "com.sbi.yono" is the official package name. Real banking apps will NEVER ask for your PIN or OTP via push notification or SMS links.'
    },
    {
        'id': 3,
        'app_name': 'Free Netflix Premium',
        'developer': 'FreeMovies4U (APK download)',
        'icon': '🎬',
        'description': 'Get Netflix Premium absolutely free! Just install this APK.',
        'permissions': [
            'Accessibility Services',
            'Draw over other apps',
            'Read SMS',
            'Billing'
        ],
        'answer': 'malicious',
        'red_flags': [
            'No such thing as "Free Netflix Premium"',
            'Sideloaded APK from outside Play Store',
            '"Accessibility Services" is used by malware to read your screen and tap buttons for you',
            '"Draw over other apps" can create fake login screens to steal passwords'
        ],
        'explanation': 'This is a very common banking malware. It uses "Accessibility Services" to read your screen and steal passwords, and "Draw over other apps" to show fake bank login screens when you open your real bank app.'
    },
    {
        'id': 4,
        'app_name': 'Google Maps',
        'developer': 'Google LLC',
        'icon': '🗺️',
        'description': 'Navigate the world with real-time traffic and local business info.',
        'permissions': [
            'Precise Location',
            'Camera (for Street View)',
            'Microphone (for voice search)'
        ],
        'answer': 'safe',
        'red_flags': [],
        'explanation': 'These permissions align perfectly with the app\'s core functionality. Location is needed for maps, camera for Street View, and mic for voice search. Context is everything when evaluating permissions.'
    }
]