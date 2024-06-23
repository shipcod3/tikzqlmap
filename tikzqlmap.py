import argparse
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import torch
from torchvision import models, transforms

tikz = '''
                                     /~\\                            
                                    |oo )                           
                                    _\\=/_                           
                    ___            /  _  \\                          
                   /() \\          //|/.\|\\\\                         
                 _|_____|_        \\\\ \\_/ ||                        
                | | === | |        \\\\|\\ /|||                        
                |_|  O  |_|        # _ _/#                        
                 ||  O  ||          | | |                          
                 ||__*__||          | | |                          
                |~ \\___/ ~|         []|[]                          
                /=\\ /=\\ /=\\         | | |                          
________________[_]_[_]_[_]________/_]_[_\\_________________________
 _   _ _              _                       
| | (_) |            | |                      
| |_ _| | __ ______ _| |_ __ ___   __ _ _ __  
| __| | |/ /|_  / _` | | '_ ` _ \\ / _` | '_ \\ 
| |_| |   <  / / (_| | | | | | | | (_| | |_) |
 \\__|_|_|\\_\\\/___\\__, |_|_| |_| |_|\\__,_| .__/ 
                   | |                 | |    
                   |_|                 |_|  
-= automatic pwet grabber exploitation and fingerprinting tool =-
'''

def wafnuke(url):
    print("Attempting to bypass web application firewall at:", url)
    # Add real WAF bypassing code here

def grab_pwet(url):
    print("Downloading and analyzing pwet images from:", url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')
    
    # Load a pre-trained ResNet model
    model = models.resnet50(pretrained=True)
    model.eval()
    
    # Define the image transformation
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    
    # Load labels
    LABELS_URL = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
    labels = requests.get(LABELS_URL).json()

    for img in images:
        img_url = img.get('src')
        if img_url:
            if not img_url.startswith('http'):
                img_url = url + img_url
            print("Analyzing image:", img_url)
            
            try:
                image_response = requests.get(img_url)
                img_data = Image.open(BytesIO(image_response.content)).convert('RGB')
                img_tensor = preprocess(img_data)
                img_tensor = img_tensor.unsqueeze(0)  # Add batch dimension
                
                with torch.no_grad():
                    output = model(img_tensor)
                _, predicted_idx = torch.max(output, 1)
                label = labels[predicted_idx.item()]
                
                print(f"Predicted label: {label}")
            except Exception as e:
                print(f"Error processing image {img_url}: {e}")

def fingerprint(url):
    print("Fingerprinting the website at:", url)
    response = requests.get(url)
    headers = response.headers
    for header, value in headers.items():
        print(f"{header}: {value}")

def crawl(url):
    print("Crawling the website recursively at:", url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        if href and href.startswith('http'):
            print("Found link:", href)

def main():
    parser = argparse.ArgumentParser(description='Automatic PWET grabber exploitation and fingerprinting tool')
    
    parser.add_argument('-w', '--wafnuke', action='store_true', help='try to bypass web application firewall')
    parser.add_argument('--grab-pwet', action='store_true', help='downloads pwet pics')
    parser.add_argument('-u', '--url', type=str, required=True, help='URL of the website')
    parser.add_argument('-f', '--finger', action='store_true', help='fingerprints the website')
    parser.add_argument('--crawl', action='store_true', help='crawls the website recursively based on the hyperlinks')
    
    args = parser.parse_args()
    
    print(tikz)
    
    if args.wafnuke:
        wafnuke(args.url)
    
    if args.grab_pwet:
        grab_pwet(args.url)
    
    if args.finger:
        fingerprint(args.url)
    
    if args.crawl:
        crawl(args.url)

if __name__ == "__main__":
    main()
