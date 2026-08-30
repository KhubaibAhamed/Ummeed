export const LANGUAGES = [
  { code: 'en', label: 'English' },
  { code: 'hi', label: 'हिंदी' },
  { code: 'te', label: 'తెలుగు' },
];

export const translations = {
  en: {
    brandName: 'Ummeed',
    tagline: 'Talk to the field. Hear back with proof.',
    nav: { home: 'Home', about: 'About', contact: 'Contact Us' },
    hero: {
      title: 'Ummeed',
      subtitle: 'Talk to the field. Hear back with proof.',
      langLabel: 'Speak or type in',
      locationPlaceholder: 'Your area, e.g. Guntur (optional)',
      getStarted: 'Get Started',
    },
    about: {
      title: 'About Ummeed',
      body:
        "Ummeed is a farmer advisory assistant that answers your questions about crops, weather, and market prices in your own language. Every answer is grounded in real sources, and cited so you can verify it yourself.",
    },
    contact: {
      title: 'Get in Touch',
      body: 'Have feedback or need help? Reach out and our team will get back to you.',
      namePlaceholder: 'Your name',
      messagePlaceholder: 'Your message',
      send: 'Send',
    },
    footer: {
      rights: 'All rights reserved.',
    },
    chat: {
      inputPlaceholder: 'Ask about your crop, weather, or price...',
      sendAria: 'Send message',
      micStartAria: 'Start voice input',
      micStopAria: 'Stop recording and send',
      thinking: 'checking your sources...',
      listening: 'listening back...',
      micDenied:
        'Microphone access was denied. Please allow microphone access for this site in your browser settings and reload the page.',
      micUnsupported:
        'Voice input needs a secure connection (https or localhost) and a browser that supports microphone access.',
      transcribeError: "Couldn't hear that clearly — try again or type your question.",
      connectionError: 'Something went wrong reaching Ummeed. Please check your connection and try again.',
    },
  },
  hi: {
    brandName: 'उम्मीद',
    tagline: 'खेत से बात करें। प्रमाण के साथ जवाब पाएं।',
    nav: { home: 'होम', about: 'हमारे बारे में', contact: 'संपर्क करें' },
    hero: {
      title: 'उम्मीद',
      subtitle: 'खेत से बात करें। प्रमाण के साथ जवाब पाएं।',
      langLabel: 'बोलें या टाइप करें',
      locationPlaceholder: 'आपका क्षेत्र, जैसे गुंटूर (वैकल्पिक)',
      getStarted: 'शुरू करें',
    },
    about: {
      title: 'उम्मीद के बारे में',
      body:
        'उम्मीद एक किसान सलाहकार सहायक है जो आपकी फसल, मौसम और बाज़ार भाव से जुड़े सवालों के जवाब आपकी अपनी भाषा में देता है। हर जवाब असली स्रोतों पर आधारित है और उसका हवाला दिया जाता है ताकि आप खुद जांच सकें।',
    },
    contact: {
      title: 'संपर्क करें',
      body: 'कोई सुझाव है या मदद चाहिए? हमें लिखें, हमारी टीम आपसे संपर्क करेगी।',
      namePlaceholder: 'आपका नाम',
      messagePlaceholder: 'आपका संदेश',
      send: 'भेजें',
    },
    footer: {
      rights: 'सर्वाधिकार सुरक्षित।',
    },
    chat: {
      inputPlaceholder: 'अपनी फसल, मौसम या भाव के बारे में पूछें...',
      sendAria: 'संदेश भेजें',
      micStartAria: 'आवाज़ इनपुट शुरू करें',
      micStopAria: 'रिकॉर्डिंग बंद करें और भेजें',
      thinking: 'आपके स्रोत जांचे जा रहे हैं...',
      listening: 'सुना जा रहा है...',
      micDenied:
        'माइक्रोफ़ोन एक्सेस अस्वीकार कर दिया गया। कृपया अपने ब्राउज़र सेटिंग में इस साइट के लिए माइक्रोफ़ोन की अनुमति दें और पेज को फिर से लोड करें।',
      micUnsupported:
        'आवाज़ इनपुट के लिए सुरक्षित कनेक्शन (https या localhost) और माइक्रोफ़ोन सपोर्ट वाला ब्राउज़र चाहिए।',
      transcribeError: 'साफ़ सुनाई नहीं दिया — फिर से कोशिश करें या अपना सवाल टाइप करें।',
      connectionError: 'उम्मीद तक पहुँचने में समस्या हुई। कृपया अपना कनेक्शन जांचें और फिर से प्रयास करें।',
    },
  },
  te: {
    brandName: 'ఉమ్మీద్',
    tagline: 'పొలంతో మాట్లాడండి. ఆధారాలతో సమాధానం పొందండి.',
    nav: { home: 'హోమ్', about: 'మా గురించి', contact: 'సంప్రదించండి' },
    hero: {
      title: 'ఉమ్మీద్',
      subtitle: 'పొలంతో మాట్లాడండి. ఆధారాలతో సమాధానం పొందండి.',
      langLabel: 'మాట్లాడండి లేదా టైప్ చేయండి',
      locationPlaceholder: 'మీ ప్రాంతం, ఉదా. గుంటూరు (ఐచ్ఛికం)',
      getStarted: 'ప్రారంభించండి',
    },
    about: {
      title: 'ఉమ్మీద్ గురించి',
      body:
        'ఉమ్మీద్ ఒక రైతు సలహా సహాయకుడు, ఇది మీ పంట, వాతావరణం మరియు మార్కెట్ ధరల గురించి మీ ప్రశ్నలకు మీ సొంత భాషలో సమాధానం ఇస్తుంది. ప్రతి సమాధానం నిజమైన మూలాధారాలపై ఆధారపడి ఉంటుంది మరియు మీరు స్వయంగా ధృవీకరించుకోవడానికి ఉదహరించబడుతుంది.',
    },
    contact: {
      title: 'సంప్రదించండి',
      body: 'అభిప్రాయం ఉందా లేదా సహాయం కావాలా? మాకు రాయండి, మా బృందం మిమ్మల్ని సంప్రదిస్తుంది.',
      namePlaceholder: 'మీ పేరు',
      messagePlaceholder: 'మీ సందేశం',
      send: 'పంపండి',
    },
    footer: {
      rights: 'అన్ని హక్కులు ప్రత్యేకించబడ్డాయి.',
    },
    chat: {
      inputPlaceholder: 'మీ పంట, వాతావరణం లేదా ధర గురించి అడగండి...',
      sendAria: 'సందేశం పంపండి',
      micStartAria: 'వాయిస్ ఇన్‌పుట్ ప్రారంభించండి',
      micStopAria: 'రికార్డింగ్ ఆపి పంపండి',
      thinking: 'మీ మూలాధారాలను తనిఖీ చేస్తోంది...',
      listening: 'వింటోంది...',
      micDenied:
        'మైక్రోఫోన్ యాక్సెస్ నిరాకరించబడింది. దయచేసి మీ బ్రౌజర్ సెట్టింగ్‌లలో ఈ సైట్ కోసం మైక్రోఫోన్‌ను అనుమతించి, పేజీని మళ్లీ లోడ్ చేయండి.',
      micUnsupported:
        'వాయిస్ ఇన్‌పుట్‌కు సురక్షిత కనెక్షన్ (https లేదా localhost) మరియు మైక్రోఫోన్‌కు మద్దతు ఇచ్చే బ్రౌజర్ అవసరం.',
      transcribeError: 'స్పష్టంగా వినిపించలేదు — మళ్లీ ప్రయత్నించండి లేదా మీ ప్రశ్నను టైప్ చేయండి.',
      connectionError: 'ఉమ్మీద్‌ను చేరుకోవడంలో సమస్య వచ్చింది. దయచేసి మీ కనెక్షన్‌ను తనిఖీ చేసి మళ్లీ ప్రయత్నించండి.',
    },
  },
};

export function getTranslations(languageCode) {
  return translations[languageCode] || translations.en;
}
