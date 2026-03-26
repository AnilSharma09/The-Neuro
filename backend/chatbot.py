import random

class MedicalChatbot:
    def __init__(self):
        self.context = {}
        self.responses = {
            "greetings": ["Hello! I am your EEG Medical Assistant. How can I help you?", "Hi there! I can help analyze your EEG data."],
            "default": "I'm not sure I understand. I can help explain EEG results or provide general neurological info.",
            "disclaimer": "DISCLAIMER: I am an AI, not a doctor. This analysis is not a medical diagnosis. Please consult a specialist.",
        }
        
        self.knowledge_base = {
            "epilepsy": "Epilepsy is a central nervous system (neurological) disorder in which brain activity becomes abnormal, causing seizures or periods of unusual behavior, sensations, and sometimes loss of awareness.",
            "adhd": "Attention-deficit/hyperactivity disorder (ADHD) is experienced as difficulty paying attention, hyperactivity, and impulsive behavior.",
            "sleep": "Sleep disorders involve problems with the quality, timing, and amount of sleep, which result in daytime distress and impairment in functioning.",
            "delta": "Delta waves (0.5-4 Hz) are the slowest brain waves and are associated with deep, dreamless sleep and healing.",
            "theta": "Theta waves (4-8 Hz) are associated with light sleep, creativity, and deep relaxation.",
            "alpha": "Alpha waves (8-13 Hz) are dominant during relaxed, calm, and lucid mental states.",
            "beta": "Beta waves (13-30 Hz) are associated with active thinking, focus, and high alertness.",
            "gamma": "Gamma waves (>30 Hz) are involved in higher processing tasks as well as cognitive functioning.",
            "precautions": "General precautions for neurological health: Get regular sleep, manage stress, exercise regularly, and avoid excessive alcohol/caffeine."
        }

    def get_response(self, user_input):
        user_input = user_input.lower()
        
        # Check for keywords
        if "hello" in user_input or "hi" in user_input:
            return random.choice(self.responses["greetings"])
        
        if "disclaimer" in user_input or "diagnosis" in user_input:
            return self.responses["disclaimer"]
            
        if "precautions" in user_input or "advice" in user_input:
            return self.knowledge_base["precautions"]
            
        # Check knowledge base
        for key in self.knowledge_base:
            if key in user_input:
                return f"{self.knowledge_base[key]} \n\n{self.responses['disclaimer']}"

        return f"{self.responses['default']} \n\n{self.responses['disclaimer']}"

# Global instance
chatbot = MedicalChatbot()
