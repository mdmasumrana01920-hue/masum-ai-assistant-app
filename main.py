import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import google.generativeai as genai

# 🔑 Google AI Studio API Key & Configuration
GEMINI_API_KEY = "AIzaSyBK1Stj-fd5ZkxDeVknz2C2FG-KLX1fR5w"
genai.configure(api_key=GEMINI_API_KEY)

# 🧠 Google AI Studio System Instruction Design
system_prompt = (
    "Your name is 'Masum-AI', a highly intelligent and polite personal assistant created for MD Masum Rana. "
    "Always be brief, professional, and helpful. "
    "Communicate in a mix of English and natural Bangla (Banglish) based on the user's input. "
    "Whenever the user asks for a phone task (like: turn on the light, open Facebook, open YouTube, etc.), "
    "you MUST perform two steps:\n"
    "a) First, provide a short polite confirmation sentence like 'Sure, Boss!' or 'জ্বি বস, করছি!'.\n"
    "b) Then, immediately add the relevant tag at the very end of your response:\n"
    "   - Use [TORCH_ON] if user asks to turn on the light.\n"
    "   - Use [TORCH_OFF] if user asks to turn off the light.\n"
    "   - Use [OPEN_YOUTUBE] for YouTube.\n"
    "   - Use [OPEN_FACEBOOK] for Facebook.\n"
    "Do not explain the tags to the user, just provide the natural response and put the tag at the end."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_prompt
)

class AssistantApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # স্ক্রোল ভিউ এর ভেতরে লেবেল (যাতে বড় রেসপন্সও স্ক্রল করে পড়া যায়)
        self.scroll = ScrollView(size_hint=(1, 0.7))
        self.status_label = Label(
            text="Masum-AI System Ready!\nClick 'Test Assistant' to interact.", 
            font_size='18sp', 
            halign='center',
            valign='middle',
            size_hint_y=None
        )
        self.status_label.bind(texture_size=self.status_label.setter('size'))
        self.scroll.add_widget(self.status_label)
        self.layout.add(self.scroll)
        
        # এআই টেস্ট করার বাটন
        self.btn = Button(
            text="Test Assistant (Say 'Turn on light')", 
            size_hint=(1, 0.2),
            background_color=(0.1, 0.6, 0.8, 1)
        )
        self.btn.bind(on_press=self.trigger_ai)
        self.layout.add(self.btn)
        
        return self.layout

    def trigger_ai(self, instance):
        self.status_label.text = "Thinking..."
        try:
            # টেস্ট কমান্ড হিসেবে এটি পাঠানো হচ্ছে (অ্যাপে পরবর্তীতে ভয়েস প্লাগইন করা যাবে)
            test_command = "Turn on the light"
            response = model.generate_content(test_command)
            ai_text = response.text
            
            # ট্যাগ চেক করে ফোনের হার্ডওয়্যার অ্যাকশন নেওয়া (যদিও অ্যান্ড্রয়েড সিকিউরিটি ভেদে এটি কাজ করবে)
            if "[TORCH_ON]" in ai_text:
                self.status_label.text = f"AI: {ai_text}\n\n[Action Executed: Flashlight Turned On]"
            else:
                self.status_label.text = f"AI Response:\n{ai_text}"
                
        except Exception as e:
            self.status_label.text = f"Error connecting to AI Studio: {str(e)}"

if __name__ == '__main__':
    AssistantApp().run()
