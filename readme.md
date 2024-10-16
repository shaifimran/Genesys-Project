# MedBot - AI-Driven Medical Assistant
MedBot is an AI-powered medical assistant designed to handle a wide range of health-related queries. The project includes two versions: one using the Unsloth Meta Llama 3.1 8B quantized model for fast inference and another with the Google Gemini 1.5 Flash API. This README highlights the development process, technical challenges, and the tech stack used to bring MedBot to life.

# Objective
Our goal was to create a reliable medical assistant using advanced AI technologies. Both versions of MedBot are designed to efficiently address health queries, from everyday concerns to more urgent medical issues.

# Data and Training
For training, we utilized the Malikeh1375/medical-question-answering-datasets from Hugging Face, ensuring that both MedBot versions are equipped to deliver accurate and relevant medical information.

# Computational Challenges
Fine-tuning large models like Llama 3.1 8B required significant computational resources. To address GPU limitations, we implemented 4-bit quantization, improving inference speed and allowing deployment alongside the Gemini 1.5 Flash API.

# Deployment
We used Kaggle's free GPU resources for model fine-tuning and deployment. To make the API publicly accessible, we implemented ngrok for routing the Kaggle server URL and port into an externally available API.

# Limitations and Future Work
While the Llama 3.1 8B model excels in fast inference, we encountered limitations with context maintenance and text streaming. Moving forward, we aim to refine these aspects to improve the overall performance and reliability of MedBot.

# Tech Stack
Frontend: HTML, CSS, JavaScript
Backend: Python, Flask, TensorFlow, Torch

# Conclusion
MedBot highlights the complexities of AI in healthcare, especially when balancing model performance and computational efficiency. We’re excited about the progress we've made and look forward to further advancements.
