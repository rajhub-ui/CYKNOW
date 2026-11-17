PHISHING_QUESTIONS = [
    {
        'id': 1,
        'sender_name': 'HDFC Bank Security',
        'sender_email': 'alerts@hdfcbank-secure.com',
        'subject': 'URGENT: Your account will be blocked in 24 hours',
        'body': '''Dear Customer,

We have detected unusual activity in your HDFC account ending in 4852.

To prevent permanent account block, complete your KYC verification immediately.

Click here to verify: http://hdfcbank-kyc-update.com/verify

If you do not complete KYC within 24 hours, your account will be permanently blocked and funds may be frozen.

HDFC Bank Security Team''',
        'answer': 'scam',
        'red_flags': [
            'Sender domain "hdfcbank-secure.com" is NOT the real HDFC domain (hdfcbank.com)',
            'Extreme urgency — 24-hour threat of account block',
            'Generic "Dear Customer" greeting',
            'Link goes to "hdfcbank-kyc-update.com" — a lookalike domain',
            'Real HDFC never asks for KYC via email links'
        ],
        'explanation': 'Classic phishing scam. Banks never use lookalike domains like "hdfcbank-secure.com" and never threaten to block accounts within 24 hours. Always inspect the domain AFTER the @ symbol.'
    },
    {
        'id': 2,
        'sender_name': 'Amazon.in',
        'sender_email': 'auto-confirm@amazon.in',
        'subject': 'Your Amazon.in order has been confirmed',
        'body': '''Hello Test User,

Thank you for your order.

Order #404-1234567-1234567
Item: USB-C Cable (1)
Delivery by: Nov 20, 2026

View your order: https://www.amazon.in/gp/css/order-history

Thank you for shopping with us.

Amazon.in''',
        'answer': 'safe',
        'red_flags': [],
        'explanation': 'Legitimate order confirmation. The sender domain is amazon.in (the real domain), the greeting is personalized, there is no urgency, and the link goes to amazon.in. Legitimate order confirmations never ask for passwords, OTPs, or card details.'
    },
    {
        'id': 3,
        'sender_name': 'CBI Cyber Crime Division',
        'sender_email': 'notice@cbi-investigation-gov.in',
        'subject': 'URGENT: Legal notice - Case No. CBI/2026/8847',
        'body': '''This is an official notice from the Central Bureau of Investigation.

A case has been registered against you under Section 420 IPC and the IT Act, for suspected involvement in money laundering linked to your Aadhaar.

You are hereby directed to:
1. Remain available on video call within 2 hours
2. Do NOT discuss this case with anyone — this is a CONFIDENTIAL investigation
3. For verification, deposit Rs. 75,000 to secure your release

Failure to comply will result in immediate arrest and 7 years of imprisonment.

Call this number immediately: +91-98XXXXXXX

CBI Cyber Crime Division''',
        'answer': 'scam',
        'red_flags': [
            'Fake domain "cbi-investigation-gov.in" — real government domains end in .gov.in only',
            'Demand for secrecy ("do not discuss with anyone")',
            'Payment demand ("deposit Rs. 75,000")',
            'Extreme urgency ("within 2 hours")',
            'Real agencies never conduct investigations over phone/video'
        ],
        'explanation': 'This is a textbook "digital arrest" scam. Real CBI, police, or any government agency NEVER conducts investigations over video calls, never asks for money, and never demands secrecy from family. Hang up immediately and report to 1930 or cybercrime.gov.in.'
    },
    {
        'id': 4,
        'sender_name': 'University Library',
        'sender_email': 'library@yourcollege.edu.in',
        'subject': 'Reminder: 2 books due on Nov 25, 2026',
        'body': '''Dear Student,

Friendly reminder that the following books are due on 25 November 2026:

- Introduction to Algorithms (Cormen)
- Operating System Concepts (Silberschatz)

Please return them by the due date to avoid late fees (Rs. 10/day).

Renew online: https://library.yourcollege.edu.in/renew

University Library Team''',
        'answer': 'safe',
        'red_flags': [],
        'explanation': 'Legitimate library reminder. The domain matches your college, the content is expected, there is no urgency beyond a normal deadline, and no sensitive info is requested. Context matters — if you did borrow these books, this is normal.'
    },
    {
        'id': 5,
        'sender_name': 'HR Recruiting',
        'sender_email': 'hr@internship-placement-2026.com',
        'subject': 'Summer Internship Opportunity — Apply now!',
        'body': '''Dear Student,

We came across your profile and believe you are a great fit for our summer internship program.

Position: Software Development Intern
Stipend: Rs. 25,000/month
Duration: 2 months
Location: Work from home

To apply, complete this 5-minute form:
https://tinyurl.com/internship-apply-2026

Limited slots available — apply before Nov 20!

HR Team
TechBridge Solutions''',
        'answer': 'suspicious',
        'red_flags': [
            'Vague company name with no verifiable website',
            'Lookalike domain "internship-placement-2026.com" — not a real company',
            'Too good to be true — Rs. 25k/month for an internship',
            'Shortened URL (tinyurl) hides destination',
            'Generic "Dear Student" greeting',
            'Time pressure "limited slots available"'
        ],
        'explanation': 'This shows classic phishing patterns but no overt financial/personal-info demand yet. Likely a scam — treat as SUSPICIOUS. Do NOT click the tinyurl. Instead, independently search for "TechBridge Solutions" or ask your placement cell to verify.'
    },
    {
        'id': 6,
        'sender_name': 'Delivery Support',
        'sender_email': 'support@delivery-update-in.info',
        'subject': 'Your package delivery failed — action required',
        'body': '''Your package (Tracking: DEL-7734-9912-IN) could not be delivered due to incorrect address.

To reschedule delivery, click here and pay a small redelivery fee of Rs. 25:
https://delivery-update-in.info/reschedule?track=DEL-7734-9912

If not rescheduled within 48 hours, the package will be returned to sender.

Delivery Team''',
        'answer': 'suspicious',
        'red_flags': [
            'Suspicious domain "delivery-update-in.info" — not a known courier',
            'No company name given (which courier?)',
            'Small payment demand — common "smishing" template',
            'Deadline pressure (48 hours)',
            'Generic greeting (no name)'
        ],
        'explanation': 'Could be a legitimate delivery notification, but the sender domain is not from any known courier (Delhivery, BlueDart, India Post). This pattern (small fee + link + deadline) is a very common smishing template. Treat as SUSPICIOUS: if you are not expecting a package, ignore it; if you are, call the courier directly using their official number.'
    },
]