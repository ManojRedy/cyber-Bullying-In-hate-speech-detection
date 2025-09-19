from detoxify import Detoxify
import pandas as pd  # For pretty printing

# Initialize the multilingual model
# This will automatically download the model weights (can take a minute the first time)
model = Detoxify('multilingual')

print("Hate Speech Detection Tool with Detoxify (Type 'quit' to exit)")
print("-------------------------------------------------------------")

while True:
    user_input = input("\nEnter a sentence to analyze: ")
    if user_input.lower() == 'quit':
        print("Goodbye!")
        break
    if user_input.strip():
        # Get results from the model
        results = model.predict(user_input)
        
        # Print the results nicely using pandas
        print(pd.DataFrame(results, index=[user_input]).round(5))
        
        # Simple rule: if toxicity score is high, flag it.
        if results['toxicity'] > 0.75:
            print("🚨 This text has been flagged as potentially harmful.")
    else:
        print("Please enter some text.")