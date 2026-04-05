import sys
from agent import AutoPPTAgent
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    if len(sys.argv) > 1:
        topic = sys.argv[1]
    else:
        topic = "Explain Machine Learning for beginners"
        
    num_slides = 5
    if len(sys.argv) > 2:
        try:
            num_slides = int(sys.argv[2])
        except ValueError:
            pass
            
    # Clean filename
    clean_topic = "".join(c if c.isalnum() else "_" for c in topic).lower()
    # Trim repetitive underscores
    import re
    clean_topic = re.sub(r'_+', '_', clean_topic).strip('_')
    
    output_filename = f"{clean_topic}.pptx"
    
    agent = AutoPPTAgent()
    agent.generate_ppt(topic, num_slides, output_filename)

if __name__ == "__main__":
    main()
