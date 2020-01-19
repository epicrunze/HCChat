# HCChat
## HyperBot

We created a chatbot based on the Hypercare API and used Google Cloud and Firebase to host our program.

HyperBot allows you, as a patient to:
- Get an approximate diagnosis based on your symptoms
- Book an appointment with your family doctor/doctor of choice, and be presented by several available appointment options (our bot contacts the doctor to confirm your selected appointment and ensures that your appointment falls within the doctor's unbooked time)

Hyper allows you, as a medical professional to:
- To look for, find, and contact other doctors
- To search for doctors in other departments in the hospital in a quick an efficient manner

Hyperbot is a cloud-based chat-bot that interfaces through the Hypercare app to provide a cutting edge chatting experience by using various algorithms to create human-like language. These algorithms involve state-of-the-art NLP techniques such as transformer word embedding (ELMo), allowing us to parse a user's query, and associate it with words that are not only semantically close, but ideologically close. This allows us to interface with the patient like never before, and to utilize APIs to diagnose based on symptoms. The other queries are handled through GraphQL, and allows our chatbot to interact richly with its environment, enabling us to do things such as search for an available specialist and create a chat room for rapid action. 
