import re
from .loader import load_lines

def detect_language(text: str) -> str:
    """Detect if text contains Gujarati, Hindi (Devanagari), or English."""
    if re.search(r'[\u0A80-\u0AFF]', text):
        return 'gu'
    elif re.search(r'[\u0900-\u097F]', text):
        return 'hi'
    return 'en'

def get_fallback_answer(question: str) -> str:
    """Intelligent, comprehensive, and multilingual answer engine for SRIMCA AI (English, Gujarati, Hindi)."""
    if not question or not question.strip():
        lang = detect_language(question or "")
        if lang == 'gu':
            return "કૃપા કરીને SRIMCA, કોર્સ, સમયપત્રક, સુવિધાઓ અથવા પ્રવેશ વિશે પ્રશ્ન પૂછો."
        elif lang == 'hi':
            return "कृपया SRIMCA, पाठ्यक्रम, समय सारणी, सुविधाओं या प्रवेश के बारे में प्रश्न पूछें।"
        return "Please ask a question about SRIMCA, courses, timetable, facilities, or admissions."

    q = question.lower().strip()
    clean_q = re.sub(r'[^\w\s\u0A80-\u0AFF\u0900-\u097F]', ' ', q)
    words = clean_q.split()
    lang = detect_language(question)

    lines = load_lines()

    # 1. Greetings & Bot Identity
    greeting_words_en = [
        'hi', 'hy', 'hyy', 'hyyy', 'hii', 'hiii', 'hey', 'heyy', 'heyyy',
        'hello', 'helloo', 'hlo', 'hllo', 'yo', 'namaste', 'good morning',
        'good afternoon', 'good evening'
    ]
    greeting_words_gu = ['નમસ્તે', 'કેમ છો', 'હલો', 'હાય', 'નમસ્કાર']
    greeting_words_hi = ['नमस्ते', 'नमस्कार', 'हेलो', 'हाय', 'कैसे हैं']

    is_greeting = (
        any(g == clean_q.strip() or clean_q.strip().startswith(g + ' ') for g in greeting_words_en + greeting_words_gu + greeting_words_hi)
        or re.match(r'^(h+[iayeo]+|hello+)\b', clean_q.strip())
    )

    if is_greeting:
        if lang == 'gu':
            return (
                "નમસ્તે! હું **SRIMCA AI Assistant** છું, તમારો સ્માર્ટ કોલેજ ગાઇડ. "
                "તમે મને નીચેના વિશે પૂછી શકો છો:\n\n"
                "• કોલેજ વિગતો, કોર્સ અને પ્રવેશ (BCA, MCA, MBA)\n"
                "• વર્ગ સમયપત્રક (Timetables)\n"
                "• કેમ્પસ સુવિધાઓ, લેબ, લાયબ્રેરી અને ટ્રાન્સપોર્ટ\n"
                "• પ્લેસમેન્ટ અને કારકિર્દીની તકો"
            )
        elif lang == 'hi':
            return (
                "नमस्ते! मैं **SRIMCA AI Assistant** हूँ, आपका स्मार्ट कॉलेज गाइड। "
                "आप मुझसे निम्न के बारे में पूछ सकते हैं:\n\n"
                "• कॉलेज विवरण, पाठ्यक्रम और प्रवेश (BCA, MCA, MBA)\n"
                "• कक्षा समय सारणी (Timetables)\n"
                "• परिसर की सुविधाएं, लैब, लाइब्रेरी और परिवहन\n"
                "• प्लेसमेंट और करियर के अवसर"
            )
        else:
            return (
                "Hello! I am **SRIMCA AI Assistant**, your smart college guide. "
                "You can ask me about:\n\n"
                "• College details, Courses & Admissions (BCA, MCA, MBA)\n"
                "• Class Timetables & Schedules\n"
                "• Campus Facilities, Labs, Library & Transport\n"
                "• Placement & Career opportunities"
            )

    identity_phrases = ['who are you', 'what are you', 'your name', 'about you', 'introduce yourself',
                        'તમે કોણ છો', 'તમારું નામ', 'તમારો પરિચય', 'કોણ છો',
                        'आप कौन हैं', 'आपका नाम', 'अपना परिचय', 'कौन हैं']
    if any(phrase in q for phrase in identity_phrases):
        if lang == 'gu':
            return (
                "હું **SRIMCA AI** છું, શ્રીમડ રાજચંદ્ર ઇન્સ્ટિટ્યુટ ઓફ મેનેજમેન્ટ એન્ડ કોમ્પ્યુટર એપ્લિકેશન (SRIMCA), ઉકા તરસાડિયા યુનિવર્સિટી માટેનો સ્માર્ટ કેમ્પસ આસિસ્ટન્ટ."
            )
        elif lang == 'hi':
            return (
                "मैं **SRIMCA AI** हूँ, श्रीमद राजचंद्र इंस्टीट्यूट ऑफ मैनेजमेंट एंड कंप्यूटर एप्लीकेशन (SRIMCA), उका तरसाडिया यूनिवर्सिटी का स्मार्ट कैंपस असिस्टेंट।"
            )
        else:
            return (
                "I am **SRIMCA AI**, the intelligent campus assistant for Shrimad Rajchandra Institute of "
                "Management and Computer Application (SRIMCA), Uka Tarsadia University. I'm here to help "
                "students, faculty, and visitors with instant academic and campus information!"
            )

    # 2. What is SRIMCA / About SRIMCA / Full Form
    srimca_info_phrases = [
        'what is srimca', 'about srimca', 'full name', 'full form', 'tell me about srimca',
        'what is the full form of srimca', 'what does srimca stand for', 'define srimca',
        'srimca detail', 'srimca details', 'srimca info', 'srimca information', 'about college',
        'એસઆરઆઈએમસીએ', 'શ્રીમડ રાજચંદ્ર', 'કોલેજ વિશે', 'માહિતી', 'વિશે જણાવો',
        'एसआरआईएमसीए', 'श्रीमद राजचंद्र', 'कॉलेज के बारे में', 'जानकारी'
    ]
    if any(phrase in q for phrase in srimca_info_phrases) or (len(words) <= 2 and 'srimca' in words):
        if lang == 'gu':
            return (
                "**SRIMCA** નું પૂરું નામ **Shrimad Rajchandra Institute of Management and Computer Application** છે.\n\n"
                "• **જોડાણ:** **ઉકા તરસાડિયા યુનિવર્સિટી (UTU)**, મલીબા કેમ્પસ, બારડોલી, સુરત નો ઘટક સંસ્થાન.\n"
                "• **મંજૂરી:** **AICTE**, નવી દિલ્હી અને ગુજરાત સરકાર દ્વારા માન્ય.\n"
                "• **સ્થાપના:** MCA 2002 માં; MBA 2004 માં સ્થાપિત.\n"
                "• **ઓફર કરાતા કોર્સ:** MCA, BCA, Integrated MCA, MBA, Integrated MBA."
            )
        elif lang == 'hi':
            return (
                "**SRIMCA** का पूरा नाम **Shrimad Rajchandra Institute of Management and Computer Application** है।\n\n"
                "• **संबद्धता:** **उका तरसाडिया यूनिवर्सिटी (UTU)**, मलीबा कैंपस, बारडोली, सूरत का घटक संस्थान।\n"
                "• **मान्यता:** **AICTE**, नई दिल्ली एवं गुजरात सरकार द्वारा स्वीकृत।\n"
                "• **स्थापना:** MCA 2002 में; MBA 2004 में स्थापित।\n"
                "• **पाठ्यक्रम:** MCA, BCA, Integrated MCA, MBA, Integrated MBA।"
            )
        else:
            return (
                "**SRIMCA** stands for **Shrimad Rajchandra Institute of Management and Computer Application**.\n\n"
                "• **Affiliation:** Constituent institute of **Uka Tarsadia University (UTU)**, Maliba Campus, Bardoli, Surat.\n"
                "• **Approvals:** Approved by **AICTE**, New Delhi & Government of Gujarat.\n"
                "• **Established:** MCA established in 2002; MBA established in 2004.\n"
                "• **Programmes Offered:** MCA, BCA, Integrated MCA, MBA, Integrated MBA."
            )

    # 3. Location / Address / Campus
    location_phrases = ['where', 'location', 'address', 'located', 'place', 'campus', 'how to reach', 'map', 'city',
                        'ક્યાં', 'સરનામું', 'ક્યા આવેલું', 'ક્યાં છે', 'સ્થળ', 'કેમ્પસ',
                        'कहां', 'पता', 'कहां स्थित', 'कहाँ है', 'स्थान', 'कैंपस']
    if any(w in q for w in location_phrases):
        if lang == 'gu':
            return (
                "**SRIMCA સ્થળ અને કેમ્પસ:**\n\n"
                "• **સરનામું:** મલીબા કેમ્પસ, ગોપાલ વિદ્યાનગર, બારડોલી-મહુવા રોડ, તરસાડી, સુરત, ગુજરાત - 394350.\n"
                "• **યુનિવર્સિટી:** ઉકા તરસાડિયા યુનિવર્સિટી (UTU)\n"
                "• **પરિવહન:** સુરત, નવસારી, બારડોલી અને વ્યારાથી બસ સુવિધા ઉપલબ્ધ છે."
            )
        elif lang == 'hi':
            return (
                "**SRIMCA स्थान एवं कैंपस:**\n\n"
                "• **पता:** मलीबा कैंपस, गोपाल विद्यानगर, बारडोली-महुवा रोड, तरसाडी, सूरत, गुजरात - 394350।\n"
                "• **विश्वविद्यालय:** उका तरसाडिया यूनिवर्सिटी (UTU)\n"
                "• **परिवहन:** सूरत, नवसारी, बारडोली और व्यारा से बस सेवा उपलब्ध है।"
            )
        else:
            return (
                "**SRIMCA Location & Campus:**\n\n"
                "• **Address:** Maliba Campus, Gopal Vidyanagar, Bardoli-Mahuva Road, Tarsadi, Surat, Gujarat - 394350.\n"
                "• **University:** Uka Tarsadia University (UTU)\n"
                "• **Transportation:** Bus services available covering Surat, Navsari, Bardoli, Vyara, and surrounding areas."
            )

    # 4. University / UTU affiliation
    utu_phrases = ['university', 'utu', 'uka tarsadia', 'affiliated', 'affiliation', 'accreditation',
                   'યુનિવર્સિટી', 'ઉકા તરસાડિયા', 'विश्वविद्यालय']
    if any(w in q for w in utu_phrases):
        if lang == 'gu':
            return "SRIMCA એ **ઉકા તરસાડિયા યુનિવર્સિટી (UTU)** ની માન્ય ઘટક સંસ્થા છે. તમામ ટેકનિકલ કોર્સ **AICTE** માન્ય છે."
        elif lang == 'hi':
            return "SRIMCA **उका तरसाडिया यूनिवर्सिटी (UTU)** का प्रमुख घटक संस्थान है। सभी तकनीकी पाठ्यक्रम **AICTE** द्वारा स्वीकृत हैं।"
        else:
            return (
                "SRIMCA is a premier constituent institute of **Uka Tarsadia University (UTU)**, established under Gujarat Private Universities Act. "
                "All technical programs are approved by **AICTE**, New Delhi."
            )

    # 5. Courses & Admission
    course_phrases = ['course', 'courses', 'program', 'programmes', 'degree', 'admission', 'eligibility', 'seat', 'intake', 'bca', 'mca', 'mba',
                      'કોર્સ', 'કોર્સો', 'કોર્સીસ', 'પ્રવેશ', 'લાયકાત', 'સીટ', 'બેઠકો',
                      'कोर्स', 'पाठ्यक्रम', 'प्रवेश', 'पात्रता', 'सीटें']
    if any(w in q for w in course_phrases):
        if lang == 'gu':
            return (
                "**SRIMCA કોર્સ અને પ્રવેશ:**\n\n"
                "• **MCA (Master of Computer Applications):** 2-વર્ષનો PG ડિગ્રી કોર્સ (ઇન્ટેક: 120 સીટો).\n"
                "• **BCA (Bachelor of Computer Applications):** 3-વર્ષનો UG ડિગ્રી કોર્સ (ઇન્ટેક: 180 સીટો).\n"
                "• **Integrated MCA (BCA + MCA):** 5-વર્ષનો ડ્યુઅલ ડિગ્રી પ્રોગ્રામ.\n"
                "• **MBA (Master of Business Administration):** 2-વર્ષનો PG ડિગ્રી કોર્સ (Finance, HR, Marketing).\n"
                "• **Integrated MBA:** 5-વર્ષનો ઇન્ટિગ્રેટેડ મેનેજમેન્ટ પ્રોગ્રામ."
            )
        elif lang == 'hi':
            return (
                "**SRIMCA पाठ्यक्रम एवं प्रवेश:**\n\n"
                "• **MCA (Master of Computer Applications):** 2-वर्षीय PG डिग्री (कुल सीट: 120)।\n"
                "• **BCA (Bachelor of Computer Applications):** 3-वर्षीय UG डिग्री (कुल सीट: 180)।\n"
                "• **Integrated MCA (BCA + MCA):** 5-वर्षीय डुअल डिग्री प्रोग्राम।\n"
                "• **MBA (Master of Business Administration):** 2-वर्षीय PG डिग्री (Finance, HR, Marketing)।\n"
                "• **Integrated MBA:** 5-वर्षीय इंटीग्रेटेड मैनेजमेंट डिग्री।"
            )
        else:
            return (
                "**SRIMCA Programmes & Admissions:**\n\n"
                "• **MCA (Master of Computer Applications):** 2-Year PG Degree (Intake: 120 seats). Eligibility: Passed BCA/B.Sc/B.Com/B.A. with Mathematics at 10+2 level or Graduation level.\n"
                "• **BCA (Bachelor of Computer Applications):** 3-Year UG Degree (Intake: 180 seats). Eligibility: 12th Pass from recognized board.\n"
                "• **Integrated MCA (BCA + MCA):** 5-Year Dual Degree Program.\n"
                "• **MBA (Master of Business Administration):** 2-Year PG Degree (Specializations: Finance, HR, Marketing).\n"
                "• **Integrated MBA:** 5-Year Integrated Management Degree."
            )

    # 6. Facilities & Infrastructure
    facility_phrases = ['facility', 'facilities', 'lab', 'labs', 'library', 'canteen', 'hostel', 'sports', 'wifi', 'internet',
                        'સુવિધાઓ', 'સુવિધા', 'લેબ', 'લાયબ્રેરી', 'હોસ્ટેલ', 'કેન્ટીન',
                        'सुविधाएं', 'सुविधा', 'लैब', 'लाइब्रेरी', 'हॉस्टल', 'कैंटीन']
    if any(w in q for w in facility_phrases):
        if lang == 'gu':
            return (
                "**SRIMCA કેમ્પસ સુવિધાઓ:**\n\n"
                "• **કોમ્પ્યુટર લેબ:** હાઇ-સ્પીડ ઇન્ટરનેટ અને આધુનિક સિસ્ટમ્સ.\n"
                "• **સેન્ટ્રલ લાયબ્રેરી:** હજારો પુસ્તકો, ડિજિટલ સામયિકો અને IEEE ઇ-રિસોર્સિસ.\n"
                "• **હોસ્ટેલ અને મેસ:** સૂરક્ષિત હોસ્ટેલ અને પૌષ્ટિક ભોજન.\n"
                "• **રમત-ગમત:** ક્રિકેટ, ફૂટબોલ, વોલીબોલનું રમતનું મેદાન અને જિમ."
            )
        elif lang == 'hi':
            return (
                "**SRIMCA कैंपस सुविधाएं:**\n\n"
                "• **कंप्यूटर लैब:** हाई-स्पीड इंटरनेट और आधुनिक सिस्टम।\n"
                "• **सेंट्रल लाइब्रेरी:** हजारों पुस्तकें, डिजिटल पत्रिकाएं एवं e-learning संसाधन।\n"
                "• **हॉस्टल एवं मेस:** सुरक्षित हॉस्टल सुविधा और स्वच्छ भोजन।\n"
                "• **खेल एवं जिम:** क्रिकेट, फुटबॉल, वॉलीबॉल मैदान और आधुनिक जिम।"
            )
        else:
            return (
                "**SRIMCA Campus Facilities:**\n\n"
                "• **Computer Labs:** High-speed internet, modern desktop systems, advanced software & development tools.\n"
                "• **Central Library:** Thousands of books, international journals, IEEE digital subscription, and e-learning resources.\n"
                "• **Hostel & Mess:** Separate secure hostels for boys and girls with 24/7 security and hygienic food.\n"
                "• **Sports & Gym:** Playground for cricket, football, volleyball, indoor games, and modern gymnasium."
            )

    # 7. Placements & Career
    placement_phrases = ['placement', 'placements', 'job', 'salary', 'package', 'company', 'companies', 'recruiters',
                         'પ્લેસમેન્ટ', 'નોકરી', 'પગાર', 'કંપનીઓ',
                         'प्लेसमेंट', 'नौकरी', 'वेतन', 'कंपनी']
    if any(w in q for w in placement_phrases):
        if lang == 'gu':
            return (
                "**SRIMCA ટ્રેનિંગ અને પ્લેસમેન્ટ સેલ:**\n\n"
                "• **મુખ્ય કંપનીઓ:** TCS, Infosys, Wipro, Capgemini, L&T Infotech, Gateway Group, TatvaSoft, Crest Data Systems.\n"
                "• પ્લેસમેન્ટ પૂર્વે એપ્ટિટ્યુડ અને ટેકનિકલ તાલીમ આપવામાં આવે છે."
            )
        elif lang == 'hi':
            return (
                "**SRIMCA ट्रेनिंग एवं प्लेसमेंट सेल:**\n\n"
                "• **प्रमुख कंपनियां:** TCS, Infosys, Wipro, Capgemini, L&T Infotech, Gateway Group, TatvaSoft, Crest Data Systems।\n"
                "• प्लेसमेंट से पहले एप्टीट्यूड, इंटरव्यू और तकनीकी प्रशिक्षण दिया जाता है।"
            )
        else:
            return (
                "**SRIMCA Training & Placement Cell:**\n\n"
                "• Strong placement record with top IT and Management recruiters.\n"
                "• **Top Recruiters:** TCS, Infosys, Wipro, Capgemini, L&T Infotech, Gateway Group, TatvaSoft, Crest Data Systems.\n"
                "• Pre-placement training including aptitude tests, mock interviews, and technical workshops."
            )

    # 8. Principal & Contact
    contact_phrases = ['contact', 'phone', 'email', 'number', 'call', 'principal', 'director', 'hod',
                       'સંપર્ક', 'ફોન', 'ઈમેઈલ', 'પ્રિન્સિપાલ',
                       'संपर्क', 'फोन', 'ईमेल', 'प्रिंसिपल']
    if any(w in q for w in contact_phrases):
        if lang == 'gu':
            return (
                "**SRIMCA સંપર્ક માહિતી:**\n\n"
                "• **ઇમેઇલ:** director.srimca@utu.ac.in\n"
                "• **વેબસાઇટ:** https://srimca.edu.in / https://utu.ac.in\n"
                "• **ફોન:** +91 (02625) 290020 / 290074\n"
                "• **સરનામું:** મલીબા કેમ્પસ, ગોપાલ વિદ્યાનગર, બારડોલી-મહુવા રોડ, તરસાડી, સુરત - 394350."
            )
        elif lang == 'hi':
            return (
                "**SRIMCA संपर्क जानकारी:**\n\n"
                "• **ईमेल:** director.srimca@utu.ac.in\n"
                "• **वेबसाइट:** https://srimca.edu.in / https://utu.ac.in\n"
                "• **फोन:** +91 (02625) 290020 / 290074\n"
                "• **पता:** मलीबा कैंपस, गोपाल विद्यानगर, बारडोली-महुवा रोड, तरसाडी, सूरत - 394350।"
            )
        else:
            return (
                "**SRIMCA Contact Information:**\n\n"
                "• **Email:** director.srimca@utu.ac.in\n"
                "• **Website:** https://srimca.edu.in / https://utu.ac.in\n"
                "• **Phone:** +91 (02625) 290020 / 290074\n"
                "• **Address:** Maliba Campus, Gopal Vidyanagar, Bardoli-Mahuva Road, Tarsadi, Surat - 394350."
            )

    # 9. Mission & Vision
    if 'vision' in q or 'વિઝન' in q or 'विजन' in q:
        if lang == 'gu':
            return "**SRIMCA વિઝન:** મેનેજમેન્ટ અને કોમ્પ્યુટર શિક્ષણમાં ઉત્કૃષ્ટતાનું કેન્દ્ર બનવું અને નૈતિક મૂલ્યો ધરાવતા વ્યાવસાયિકો તૈયાર કરવા."
        elif lang == 'hi':
            return "**SRIMCA विजन:** प्रबंधन और कंप्यूटर शिक्षा में उत्कृष्टता का केंद्र बनना और नैतिक मूल्यों वाले पेशेवर तैयार करना।"
        return "**SRIMCA Vision:** To become a center of excellence in management and computer education by producing competent professionals with strong ethical values."

    if 'mission' in q or 'મિશન' in q or 'मिशन' in q:
        if lang == 'gu':
            return "**SRIMCA મિશન:** શિક્ષણ, સંશોધન, ઉદ્યોગ ભાગીદારી અને સમાજ પ્રત્યેની નૈતિક પ્રતિબદ્ધતામાં અગ્રેસર રહેવું."
        elif lang == 'hi':
            return "**SRIMCA मिशन:** शिक्षा, अनुसंधान, उद्योग साझेदारी और समाज के प्रति नैतिक प्रतिबद्धता में अग्रणी रहना।"
        return "**SRIMCA Mission:** To remain on the cutting edge of education, research, industry partnerships, and moral commitment to society."

    # 10. Keyword Search across loaded lines
    stop_words = {'what', 'is', 'are', 'the', 'a', 'an', 'of', 'for', 'in', 'on', 'at', 'to', 'do', 'does', 'can', 'you', 'i', 'tell', 'me', 'please', 'give', 'detail', 'details', 'about'}
    query_keywords = [w for w in words if w not in stop_words and len(w) > 2]

    if query_keywords:
        matching_lines = []
        for line in lines:
            line_lower = line.lower()
            match_count = sum(1 for kw in query_keywords if kw in line_lower)
            if match_count > 0:
                matching_lines.append((match_count, line))

        if matching_lines:
            matching_lines.sort(key=lambda x: x[0], reverse=True)
            top_matches = [m[1] for m in matching_lines[:4]]
            return "\n\n".join(top_matches)

    # 11. General Fallback (for non-SRIMCA / unrecognized questions)
    if lang == 'gu':
        return (
            "ક્ષમા કરશો, મારી પાસે તેની માહિતી નથી. **SRIMCA AI Assistant** તરીકે, હું SRIMCA કોલેજ સંબંધિત પ્રશ્નોના જવાબ આપવા માટે બનાવાયો છું.\n\n"
            "તમે મને નીચેના વિશે પૂછી શકો છો:\n"
            "• કોલેજ માહિતી અને પ્રવેશ (BCA, MCA, MBA)\n"
            "• વર્ગ સમયપત્રક (Timetables)\n"
            "• કેમ્પસ સુવિધાઓ, લાયબ્રેરી અને પ્લેસમેન્ટ"
        )
    elif lang == 'hi':
        return (
            "क्षमा करें, मेरे पास इसकी जानकारी नहीं है। **SRIMCA AI Assistant** के रूप में, मुझे SRIMCA कॉलेज से संबंधित प्रश्नों के उत्तर देने के लिए बनाया गया है।\n\n"
            "आप मुझसे पूछ सकते हैं:\n"
            "• कॉलेज जानकारी और प्रवेश (BCA, MCA, MBA)\n"
            "• कक्षा समय सारणी (Timetables)\n"
            "• परिसर सुविधाएं, लाइब्रेरी और प्लेसमेंट"
        )
    else:
        return (
            "I'm sorry, I don't have information on that. As **SRIMCA AI Assistant**, I am designed to answer questions related to SRIMCA college.\n\n"
            "You can ask me about:\n"
            "• College information & Admissions\n"
            "• Courses offered (BCA, MCA, MBA)\n"
            "• Class Timetables & Schedules\n"
            "• Campus Facilities, Library & Placements"
        )

