DIGITAL_ARREST_SCENARIO = {
    'title': 'Incoming Video Call: +91-98XXXXXX21',
    'caller_name': 'Officer Sharma (CBI)',
    'steps': [
        {
            'id': 1,
            'speaker': 'Officer',
            'text': 'This is Officer Sharma from the CBI Cyber Crime Division. A parcel in your name containing illegal narcotics was intercepted today. Your Aadhaar is linked to a money-laundering case. You are under digital arrest. Do you understand?',
            'choices': [
                {
                    'text': 'Yes sir, I understand. Please tell me what to do.',
                    'is_correct': False,
                    'feedback': '❌ You just accepted a fake arrest. Real officers never arrest anyone over a video call. By agreeing, you gave the scammer psychological control.'
                },
                {
                    'text': 'Can you show me your official ID and badge?',
                    'is_correct': True,
                    'feedback': '✅ Good. You are testing their authority. (Spoiler: They will show a fake, photoshopped ID—but questioning them is the right instinct.)'
                },
                {
                    'text': 'I know this is a scam. I am hanging up.',
                    'is_correct': True,
                    'feedback': '✅ Perfect. Hanging up is the safest action. You recognized the hook immediately.'
                }
            ]
        },
        {
            'id': 2,
            'speaker': 'Officer',
            'text': '(Shows a blurry fake ID on screen) Do not test me! This is a top-secret operation. You are NOT allowed to tell your family or bank about this call. If you do, you will be charged with obstruction of justice and sent to Tihar Jail today.',
            'choices': [
                {
                    'text': 'I won\'t tell anyone. Please don\'t arrest me.',
                    'is_correct': False,
                    'feedback': '❌ This is the "Isolation" layer. Scammers demand secrecy so you can\'t get a second opinion from family who would instantly tell you it\'s a scam.'
                },
                {
                    'text': 'I am messaging my son right now to tell him.',
                    'is_correct': True,
                    'feedback': '✅ Excellent. Breaking isolation is the fastest way to destroy a scammer\'s power. They rely on you being alone and scared.'
                },
                {
                    'text': 'Why would a real officer demand secrecy from my own family?',
                    'is_correct': True,
                    'feedback': '✅ Smart. You are questioning the flawed logic. Real law enforcement never demands secrecy from family.'
                }
            ]
        },
        {
            'id': 3,
            'speaker': 'Officer',
            'text': 'Listen carefully. I am sending a "verification link" to your WhatsApp. You must transfer Rs. 50,000 to this RBI secure account to verify your funds. Once the investigation clears you, the money will be refunded within 24 hours.',
            'choices': [
                {
                    'text': 'Okay, I am transferring the money now.',
                    'is_correct': False,
                    'feedback': '❌ You just lost Rs. 50,000. No government agency has an "RBI secure account" for citizens to verify funds. This is the Payment Trap.'
                },
                {
                    'text': 'I will not transfer any money. I am disconnecting this call.',
                    'is_correct': True,
                    'feedback': '✅ Perfect. Money demands are the ultimate red flag. Disconnecting is the right move.'
                },
                {
                    'text': 'Can I come to the CBI office in person to pay?',
                    'is_correct': True,
                    'feedback': '✅ Good. Scammers will make excuses why you can\'t meet in person. Suggesting an in-person visit always exposes them.'
                }
            ]
        },
        {
            'id': 4,
            'speaker': 'Officer',
            'text': 'If you disconnect, a police team will be at your house in 10 minutes! I am sending an arrest warrant to your WhatsApp right now! (You receive a PDF with a fake warrant and a judge\'s signature).',
            'choices': [
                {
                    'text': 'I am terrified. Please, I will pay the money.',
                    'is_correct': False,
                    'feedback': '❌ The PDF is a template downloaded from the internet. Real warrants are never sent via WhatsApp. You are panicking—exactly what they want.'
                },
                {
                    'text': 'I am hanging up and calling 1930.',
                    'is_correct': True,
                    'feedback': '✅ PERFECT. 1930 is the national cybercrime helpline. Reporting immediately stops the scam and protects others.'
                },
                {
                    'text': 'I am hanging up and calling my lawyer/family.',
                    'is_correct': True,
                    'feedback': '✅ Excellent. Getting a trusted second opinion immediately breaks the scammer\'s spell.'
                }
            ]
        }
    ]
}